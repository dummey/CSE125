import sys
sys.path = ["../../deps"] + sys.path

from euclid import *
from itertools import product

class BoundingBox(object):
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        """
        Create a new bounding box.
        Represented internally by two points.
        """

        self.p0 = Point3(xmin, ymin, zmin)
        self.p1 = Point3(xmax, ymax, zmax)

    def __repr__(self):
        """
        Compact string representation of bounding box.
        """

        return "p0: (%s, %s, %s)" % (self.p0.x, self.p0.y, self.p0.z) + " " + \
               "p1: (%s, %s, %s)" % (self.p1.x, self.p1.y, self.p1.z)

    def positioned(self, position):
        p0 = self.p0 + position
        p1 = self.p1 + position
        return BoundingBox(p0.x, p1.x, p0.y, p1.y, p0.z, p1.z)

    def inflate_box(self, amount):
        infation = Vector3(amount, amount, amount)
        self.p0 -= infation
        self.p1 += infation

    def points(self):
        """
        Return a list of this bounding box's 8 points.
        """

        cartesian = list(product([self.p0, self.p1], repeat=3))
        return [Point3(x[0][0], x[1][1], x[2][2]) for x in cartesian]

    def transformed(self, forward, up):
        """
        Return the axis-aligned version of this object-oriented bounding box.
        """

        # set up transformation vectors
        forward.normalize()
        up.normalize()
        right = up.cross(forward).normalize()

        # create transformation matrix
        transform = Matrix4()
        transform[:] = [right.x,   right.y,   right.z,   0.0,
                        up.x,      up.y,      up.z,      0.0,
                        forward.x, forward.y, forward.z, 0.0,
                        0.0,       0.0,       0.0,       0.0]

        # transform points
        points = [transform*p for p in self.points()]

        # get new bounding box
        xmin = min([p.x for p in points])
        xmax = max([p.x for p in points])
        ymin = min([p.y for p in points])
        ymax = max([p.y for p in points])
        zmin = min([p.z for p in points])
        zmax = max([p.z for p in points])
        return BoundingBox(xmin, xmax, ymin, ymax, zmin, zmax)

    def subdivided(self):
        """
        Return a list of this object-oriented bounding box's 8 subdivisions.
        """

        pass

    def collides(self, other, self_position, other_position, collision_direction=None):
        """
        Return collision direction vector if there is a collision, else False.
        """

        # can't collide with self
        if other is self:
            return False

        if other is None:
            return False

        # calculate other bounding box's relative position and distance
        position = other_position - self_position
        distance = Vector3(abs(position.x), abs(position.y), abs(position.z))

        # bounding box isn't necessarily symmetric so compare carefully
        if position.x > 0:
            x_test = self.p1.x - other.p0.x
        else:
            x_test = other.p1.x - self.p0.x

        if position.y > 0:
            y_test = self.p1.y - other.p0.y
        else:
            y_test = other.p1.y - self.p0.y

        if position.z > 0:
            z_test = self.p1.z - other.p0.z
        else:
            z_test = other.p1.z - self.p0.z

        # test for collision
        if distance.x < x_test and distance.y < y_test and distance.z < z_test:
            # print "collision detected!"
            direction = Vector3()

            # calculate collision direction
            if collision_direction is not None:
                direction = collision_direction.normalize()
            else:
                if distance.x >= distance.y and distance.x >= distance.z:
                    if position.x > 0:
                        direction.x = -1
                    else:
                        direction.x = 1
                if distance.y >= distance.x and distance.y >= distance.z:
                    if position.y > 0:
                        direction.y = -1
                    else:
                        direction.y = 1
                if distance.z >= distance.x and distance.z >= distance.y:
                    if position.z > 0:
                        direction.z = -1
                    else:
                        direction.z = 1

            return direction
        else:
            return False

class Ray(object):
    """
    Python port of C code from the paper "Fast Ray/Axis-Aligned Bounding Box
    Overlap Tests using Ray Slopes" by Martin Eisemann, Thorsten Grosch,
    Stefan Mueller, and Marcus Magnor (Computer Graphics Lab, TU Braunschweig).
    """

    def __init__(self, position, direction):
        """
        Creates a new ray for the purpose of collision detection.
        We precompute ray slopes and other invariants.
        """

        def inv(n):
            try:
                return 1.0/n
            except ZeroDivisionError:
                return float("inf")

        self.p = position
        self.d = direction

        self.s_yx = direction.x * inv(direction.y)
        self.s_xy = direction.y * inv(direction.x)
        self.s_zy = direction.y * inv(direction.z)
        self.s_yz = direction.z * inv(direction.y)
        # self.s_xz = direction.x * inv(direction.z)
        # self.s_zx = direction.z * inv(direction.x)
        self.s_xz = direction.z * inv(direction.x)
        self.s_zx = direction.x * inv(direction.z)

        self.c_xy = position.y - self.s_xy * position.x
        self.c_yx = position.x - self.s_yx * position.y
        self.c_zy = position.y - self.s_zy * position.z
        self.c_yz = position.z - self.s_yz * position.y
        self.c_xz = position.z - self.s_xz * position.x
        self.c_zx = position.x - self.s_zx * position.z

        self.ray_type = "".join(map(lambda x: x < 0 and "M" or x > 0 and "P" or "O", direction))

    def __repr__(self):
        """
        Simple string representation of ray (mostly for debugging).
        """

        return "pos: (%s, %s, %s)" % (self.p.x, self.p.y, self.p.z) + " " + \
               "dir: (%s, %s, %s)" % (self.d.x, self.d.y, self.d.z) + " " + \
               "ray_type: %s" % self.ray_type

    def collides(self, bbox, bbox_position):
        """
        Return true if ray collides with the axis-aligned bounding box.
        """

        box = bbox.positioned(bbox_position)

        # print "\nray.collides"
        # print self
        # print box
        return getattr(self, "_collides_%s" % self.ray_type)(box)

    def _collides_MMM(self, bbox):
        if (self.p.x < bbox.p0.x) or (self.p.y < bbox.p0.y) or (self.p.z < bbox.p0.z) or \
           (self.s_xy * bbox.p0.x - bbox.p1.y + self.c_xy > 0) or \
           (self.s_yx * bbox.p0.y - bbox.p1.x + self.c_yx > 0) or \
           (self.s_zy * bbox.p0.z - bbox.p1.y + self.c_zy > 0) or \
           (self.s_yz * bbox.p0.y - bbox.p1.z + self.c_yz > 0) or \
           (self.s_xz * bbox.p0.x - bbox.p1.z + self.c_xz > 0) or \
           (self.s_zx * bbox.p0.z - bbox.p1.x + self.c_zx > 0):
            return False
        else:
            return True

    def _collides_MMP(self, bbox):
        if (self.p.x < bbox.p0.x) or (self.p.y < bbox.p0.y) or (self.p.z > bbox.p1.z) or \
           (self.s_xy * bbox.p0.x - bbox.p1.y + self.c_xy > 0) or \
           (self.s_yx * bbox.p0.y - bbox.p1.x + self.c_yx > 0) or \
           (self.s_zy * bbox.p1.z - bbox.p1.y + self.c_zy > 0) or \
           (self.s_yz * bbox.p0.y - bbox.p0.z + self.c_yz < 0) or \
           (self.s_xz * bbox.p0.x - bbox.p0.z + self.c_xz < 0) or \
           (self.s_zx * bbox.p1.z - bbox.p1.x + self.c_zx > 0):
            return False
        else:
            return True

    def _collides_MPM(self, bbox):
        if (self.p.x < bbox.p0.x) or (self.p.y > bbox.p1.y) or (self.p.z < bbox.p0.z) or \
           (self.s_xy * bbox.p0.x - bbox.p0.y + self.c_xy < 0) or \
           (self.s_yx * bbox.p1.y - bbox.p1.x + self.c_yx > 0) or \
           (self.s_zy * bbox.p0.z - bbox.p0.y + self.c_zy < 0) or \
           (self.s_yz * bbox.p1.y - bbox.p1.z + self.c_yz > 0) or \
           (self.s_xz * bbox.p0.x - bbox.p1.z + self.c_xz > 0) or \
           (self.s_zx * bbox.p0.z - bbox.p1.x + self.c_zx > 0):
            return False
        else:
            return True

    def _collides_MPP(self, bbox):
        if (self.p.x < bbox.p0.x) or (self.p.y > bbox.p1.y) or (self.p.z > bbox.p1.z) or \
           (self.s_xy * bbox.p0.x - bbox.p0.y + self.c_xy < 0) or \
           (self.s_yx * bbox.p1.y - bbox.p1.x + self.c_yx > 0) or \
           (self.s_zy * bbox.p1.z - bbox.p0.y + self.c_zy < 0) or \
           (self.s_yz * bbox.p1.y - bbox.p0.z + self.c_yz < 0) or \
           (self.s_xz * bbox.p0.x - bbox.p0.z + self.c_xz < 0) or \
           (self.s_zx * bbox.p1.z - bbox.p1.x + self.c_zx > 0):
            return False
        else:
            return True

    def _collides_PMM(self, bbox):
        if (self.p.x > bbox.p1.x) or (self.p.y < bbox.p0.y) or (self.p.z < bbox.p0.z) or \
           (self.s_xy * bbox.p1.x - bbox.p1.y + self.c_xy > 0) or \
           (self.s_yx * bbox.p0.y - bbox.p0.x + self.c_yx < 0) or \
           (self.s_zy * bbox.p0.z - bbox.p1.y + self.c_zy > 0) or \
           (self.s_yz * bbox.p0.y - bbox.p1.z + self.c_yz > 0) or \
           (self.s_xz * bbox.p1.x - bbox.p1.z + self.c_xz > 0) or \
           (self.s_zx * bbox.p0.z - bbox.p0.x + self.c_zx < 0):
            return False
        else:
            return True

    def _collides_PMP(self, bbox):
        if (self.p.x > bbox.p1.x) or (self.p.y < bbox.p0.y) or (self.p.z > bbox.p1.z) or \
           (self.s_xy * bbox.p1.x - bbox.p1.y + self.c_xy > 0) or \
           (self.s_yx * bbox.p0.y - bbox.p0.x + self.c_yx < 0) or \
           (self.s_zy * bbox.p1.z - bbox.p1.y + self.c_zy > 0) or \
           (self.s_yz * bbox.p0.y - bbox.p0.z + self.c_yz < 0) or \
           (self.s_xz * bbox.p1.x - bbox.p0.z + self.c_xz < 0) or \
           (self.s_zx * bbox.p1.z - bbox.p0.x + self.c_zx < 0):
            return False
        else:
            return True

    def _collides_PPM(self, bbox):
        if (self.p.x > bbox.p1.x) or (self.p.y > bbox.p1.y) or (self.p.z < bbox.p0.z) or \
           (self.s_xy * bbox.p1.x - bbox.p0.y + self.c_xy < 0) or \
           (self.s_yx * bbox.p1.y - bbox.p0.x + self.c_yx < 0) or \
           (self.s_zy * bbox.p0.z - bbox.p0.y + self.c_zy < 0) or \
           (self.s_yz * bbox.p1.y - bbox.p1.z + self.c_yz > 0) or \
           (self.s_xz * bbox.p1.x - bbox.p1.z + self.c_xz > 0) or \
           (self.s_zx * bbox.p0.z - bbox.p0.x + self.c_zx < 0):
            return False
        else:
            return True

    def _collides_PPP(self, bbox):
        if (self.p.x > bbox.p1.x) or (self.p.y > bbox.p1.y) or (self.p.z > bbox.p1.z) or \
           (self.s_xy * bbox.p1.x - bbox.p0.y + self.c_xy < 0) or \
           (self.s_yx * bbox.p1.y - bbox.p0.x + self.c_yx < 0) or \
           (self.s_zy * bbox.p1.z - bbox.p0.y + self.c_zy < 0) or \
           (self.s_yz * bbox.p1.y - bbox.p0.z + self.c_yz < 0) or \
           (self.s_xz * bbox.p1.x - bbox.p0.z + self.c_xz < 0) or \
           (self.s_zx * bbox.p1.z - bbox.p0.x + self.c_zx < 0):
            return False
        else:
            return True

    def _collides_OMM(self, bbox):
        if (self.p.x < bbox.p0.x) or (self.p.x > bbox.p1.x) or \
           (self.p.y < bbox.p0.y) or (self.p.z < bbox.p0.z) or \
           (self.s_zy * bbox.p0.z - bbox.p1.y + self.c_zy > 0) or \
           (self.s_yz * bbox.p0.y - bbox.p1.z + self.c_yz > 0):
            return False
        else:
            return True

    def _collides_OMP(self, bbox):
        if (self.p.x < bbox.p0.x) or (self.p.x > bbox.p1.x) or \
           (self.p.y < bbox.p0.y) or (self.p.z > bbox.p1.z) or \
           (self.s_zy * bbox.p1.z - bbox.p1.y + self.c_zy > 0) or \
           (self.s_yz * bbox.p0.y - bbox.p0.z + self.c_yz < 0):
            return False
        else:
            return True

    def _collides_OPM(self, bbox):
        if (self.p.x < bbox.p0.x) or (self.p.x > bbox.p1.x) or \
           (self.p.y > bbox.p1.y) or (self.p.z < bbox.p0.z) or \
           (self.s_zy * bbox.p0.z - bbox.p0.y + self.c_zy < 0) or \
           (self.s_yz * bbox.p1.y - bbox.p1.z + self.c_yz > 0):
            return False
        else:
            return True

    def _collides_OPP(self, bbox):
        if (self.p.x < bbox.p0.x) or (self.p.x > bbox.p1.x) or \
           (self.p.y > bbox.p1.y) or (self.p.z > bbox.p1.z) or \
           (self.s_zy * bbox.p1.z - bbox.p0.y + self.c_zy < 0) or \
           (self.s_yz * bbox.p1.y - bbox.p0.z + self.c_yz < 0):
            return False
        else:
            return True

    def _collides_MOM(self, bbox):
        if (self.p.y < bbox.p0.y) or (self.p.y > bbox.p1.y) or \
           (self.p.x < bbox.p0.x) or (self.p.z < bbox.p0.z) or \
           (self.s_xz * bbox.p0.x - bbox.p1.z + self.c_xz > 0) or \
           (self.s_zx * bbox.p0.z - bbox.p1.x + self.c_zx > 0):
            return False
        else:
            return True

    def _collides_MOP(self, bbox):
        if (self.p.y < bbox.p0.y) or (self.p.y > bbox.p1.y) or \
           (self.p.x < bbox.p0.x) or (self.p.z > bbox.p1.z) or \
           (self.s_xz * bbox.p0.x - bbox.p0.z + self.c_xz < 0) or \
           (self.s_zx * bbox.p1.z - bbox.p1.x + self.c_zx > 0):
            return False
        else:
            return True

    def _collides_POM(self, bbox):
        if (self.p.y < bbox.p0.y) or (self.p.y > bbox.p1.y) or \
           (self.p.x > bbox.p1.x) or (self.p.z < bbox.p0.z) or \
           (self.s_xz * bbox.p1.x - bbox.p1.z + self.c_xz > 0) or \
           (self.s_zx * bbox.p0.z - bbox.p0.x + self.c_zx < 0):
            return False
        else:
            return True

    def _collides_POP(self, bbox):
        if (self.p.y < bbox.p0.y) or (self.p.y > bbox.p1.y) or \
           (self.p.x > bbox.p1.x) or (self.p.z > bbox.p1.z) or \
           (self.s_xz * bbox.p1.x - bbox.p0.z + self.c_xz < 0) or \
           (self.s_zx * bbox.p1.z - bbox.p0.x + self.c_zx < 0):
            return False
        else:
            return True

    def _collides_MMO(self, bbox):
        if (self.p.z < bbox.p0.z) or (self.p.z > bbox.p1.z) or \
           (self.p.x < bbox.p0.x) or (self.p.y < bbox.p0.y) or \
           (self.s_xy * bbox.p0.x - bbox.p1.y + self.c_xy > 0) or \
           (self.s_yx * bbox.p0.y - bbox.p1.x + self.c_yx > 0):
            return False
        else:
            return True

    def _collides_MPO(self, bbox):
        if (self.p.z < bbox.p0.z) or (self.p.z > bbox.p1.z) or \
           (self.p.x < bbox.p0.x) or (self.p.y > bbox.p1.y) or \
           (self.s_xy * bbox.p0.x - bbox.p0.y + self.c_xy < 0) or \
           (self.s_yx * bbox.p1.y - bbox.p1.x + self.c_yx > 0):
            return False
        else:
            return True

    def _collides_PMO(self, bbox):
        if (self.p.z < bbox.p0.z) or (self.p.z > bbox.p1.z) or \
           (self.p.x > bbox.p1.x) or (self.p.y < bbox.p0.y) or \
           (self.s_xy * bbox.p1.x - bbox.p1.y + self.c_xy > 0) or \
           (self.s_yx * bbox.p0.y - bbox.p0.x + self.c_yx < 0):
            return False
        else:
            return True

    def _collides_PPO(self, bbox):
        if (self.p.z < bbox.p0.z) or (self.p.z > bbox.p1.z) or \
           (self.p.x > bbox.p1.x) or (self.p.y > bbox.p1.y) or \
           (self.s_xy * bbox.p1.x - bbox.p0.y + self.c_xy < 0) or \
           (self.s_yx * bbox.p1.y - bbox.p0.x + self.c_yx < 0):
            return False
        else:
            return True

    def _collides_MOO(self, bbox):
        if (self.p.x < bbox.p0.x) or \
           (self.p.y < bbox.p0.y) or (self.p.y > bbox.p1.y) or \
           (self.p.z < bbox.p0.z) or (self.p.z > bbox.p1.z):
            return False
        else:
            return True

    def _collides_POO(self, bbox):
        if (self.p.x > bbox.p1.x) or \
           (self.p.y < bbox.p0.y) or (self.p.y > bbox.p1.y) or \
           (self.p.z < bbox.p0.z) or (self.p.z > bbox.p1.z):
            return False
        else:
            return True

    def _collides_OMO(self, bbox):
        if (self.p.y < bbox.p0.y) or \
           (self.p.x < bbox.p0.x) or (self.p.x > bbox.p1.x) or \
           (self.p.z < bbox.p0.z) or (self.p.z > bbox.p1.z):
            return False
        else:
            return True

    def _collides_OPO(self, bbox):
        if (self.p.y > bbox.p1.y) or \
           (self.p.x < bbox.p0.x) or (self.p.x > bbox.p1.x) or \
           (self.p.z < bbox.p0.z) or (self.p.z > bbox.p1.z):
            return False
        else:
            return True

    def _collides_OOM(self, bbox):
        if (self.p.z < bbox.p0.z) or \
           (self.p.x < bbox.p0.x) or (self.p.x > bbox.p1.x) or \
           (self.p.y < bbox.p0.y) or (self.p.y > bbox.p1.y):
            return False
        else:
            return True

    def _collides_OOP(self, bbox):
        if (self.p.z > bbox.p1.z) or \
           (self.p.x < bbox.p0.x) or (self.p.x > bbox.p1.x) or \
           (self.p.y < bbox.p0.y) or (self.p.y > bbox.p1.y):
            return False
        else:
            return True

    def _collides_OOO(self, bbox):
        return False

if __name__ == "__main__":
    bbox = BoundingBox(-10, 10, -10, 10, -10, 10)
    print bbox
    print bbox.transformed(Vector3(1, 0, -1), Vector3(0, 1, 0))
    ray = Ray(Vector3(0, 0, 0), Vector3(1, 1, 1))
    print ray
    print getattr(ray, "_collides_%s" % ray.ray_type)