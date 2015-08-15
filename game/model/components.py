from euclid import Point3, Vector3, Matrix4
from copy import copy
from math import cos, sin, sqrt
from game import settings
from game.graphics import shapes
from game.model import collision
from pprint import pformat
import game

class PackFieldsMetaclass(type):
    def __new__(mcs, cls, bases, attrs):
        fields = set(attrs.get("fields", ()))
        for base in bases:
            try:
                fields.update(base.fields)
            except AttributeError:
                pass
        for field in fields.copy():
            if field.startswith("-"):
                fields.remove(field)
                fields.remove(field[1:])
        attrs["fields"] = tuple(fields)
        _fields_previous = {}
        for field in fields:
            _fields_previous[field] = None
        attrs["_fields_previous"] = _fields_previous
        return type.__new__(mcs, cls, bases, attrs)


class Element(object):
    """All objects in a room are elements."""

    __metaclass__ = PackFieldsMetaclass

    id = -1

    fields = () # names of variables to pack
    _fields_previous = {}

    def __init__(self):
        self._fields_previous = self._fields_previous.copy()

    def is_local(self):
        return self.id < 0

    def update(self, dt):
        pass

    def pack(self):
        data = {}
        for field in self.fields:
            f_data = getattr(self, field)
            if f_data != self._fields_previous[field]:
                data[field] = f_data
                self._fields_previous[field] = copy(f_data) # update previous value before start of next pack
        return data if data else None # only send if some fields changed

    def unpack(self, data):
        for field in data:
            if field in self.fields: # don't allow arbitrary attributes
                setattr(self, field, data[field])

    def render(self):
        pass

class Position(Element):
    """The element is a static prop."""

    fields = ("position", "forward", "up", "aabb")

    position = Point3()
    forward = Vector3(0,0,-1)
    right = Vector3()
    up = Vector3()
    lookat = Vector3()

    oobb = None
    aabb = None

    collidable = True
    
    alterable = False

    def __init__(self, position=None, forward=None, up=None):
        super(Position, self).__init__()
        if position: self.position = position
        if forward: self.forward = forward
        upcross = up and up or Vector3(0, 1, 0)

        self.right = self.forward.cross(upcross).normalized()
        self.up = -self.forward.cross(self.right).normalized()

        # self.right   = Vector3(1, 0, 0)
        # self.up      = Vector3(0, 1, 0)
        # self.forward = Vector3(0, 0, -1)

    def unpack(self, data):
        super(Position, self).unpack(data)
        self.orient()

    def orient(self):
        # forward and up vectors were just updated
        self.right = self.forward.cross(self.up).normalized()

    def collision_check(self, other):
        """
        Peforms collision detection check.  If a collision is detected,
        call collision_reaction to determine the appropriate collision.
        """

        direction = None
        if other.__class__.__name__ == "Laser":
            pass # ignore
        elif other.__class__.__name__ == "Wall":
            direction = self.aabb.collides(other.aabb, self.position + self.velocity, other.position,
                                           collision_direction=other.forward)
        else:
            direction = self.aabb.collides(other.aabb, self.position + self.velocity, other.position)

        if direction is not None and direction is not False:
            self.collision_reaction(other, direction)
            # print direction, other.forward
            return direction
        else:
            return False

    def collision_reaction(self, other, direction):
        
#cal manager sound

        # do puff
        
        if other.collidable is True:
            if isinstance(other, Movement):
                weight_bias = 1
                #v1f = v1i - ((m2c)/(m1 + m2))(1 + e)n
                #c = n . (v1i - v2i)
                normal = self.position - other.position
                normal = normal.normalize()
                #shitty elastic collision system
                #print other.velocity
                if normal.x:
                    self.position.x -= self.velocity.x
                    self.velocity.x = abs(self.velocity.x - other.velocity.x) * normal.x * weight_bias
                    other.position.x -= other.velocity.x
                    other.velocity.x = abs(other.velocity.x - self.velocity.x) * -1 * normal.x * weight_bias
                if normal.y:
                    self.position.y -= self.velocity.y
                    self.velocity.y = abs(self.velocity.y - other.velocity.y) * normal.y * weight_bias
                    other.position.y -= other.velocity.y
                    other.velocity.y = abs(other.velocity.y - self.velocity.y) * -1 * normal.y * weight_bias
                if normal.z:
                    self.position.z -= self.velocity.z
                    self.velocity.z = abs(self.velocity.z - other.velocity.z) * normal.z * weight_bias
                    self.position.z -= self.velocity.z
                    other.velocity.z = abs(other.velocity.z - self.velocity.z) * -1 * normal.z * weight_bias
            else:
                if direction.x:
                    self.position.x -= self.velocity.x
                    self.velocity.x = abs(self.velocity.x) * direction.x
                if direction.y:
                    self.position.y -= self.velocity.y
                    self.velocity.y = abs(self.velocity.y) * direction.y
                if direction.z:
                    self.position.z -= self.velocity.z
                    self.velocity.z = abs(self.velocity.z) * direction.z

    def hit_by_laser(self, player):
        pass
        # FYI, this code won't work because it takes place serverside...
        # if hasattr(self, "color"):
        #     import random
        #     self.color = (random.random(), random.random(), random.random())
    
    def rotate_point_rotation(self, point, axis, magnitude):
        m = Matrix4.new_rotate_axis(magnitude, axis)
        pos = Vector3(self.position.x - point.x,
                      self.position.y - point.y,
                      self.position.z - point.z)
        pos = m.transform( pos)
        return pos + point
    
    def outside_room(self, room):
        pass

class Movement(Position):
    """The element has basic physics through movement."""

    MAX_VELOCITY = settings.MAX_VELOCITY
    MAX_ACCELERATION = settings.MAX_ACCELERATION

    fields = ("velocity", "rotation_point")

    rotation_point = None
    reeling_in = False
    
    alterable = True
    
    # rotation_point = Vector3(0,0,0)

    def __init__(self, position=None, forward=None, velocity=None):
        super(Movement, self).__init__(position, forward)
        if velocity:
            self.velocity = velocity
        else:
            self.velocity = Vector3()
        self.acceleration = Vector3()

    def projected_position(self):
        return self.position + self.velocity

    def update(self, dt):
        if self.rotation_point is not None and self.position is not None:
            diff = self.position - self.rotation_point
            dist = diff.magnitude()
            diff.normalize()
            rotational_velocity = self.velocity.magnitude() / dist
            axis = (diff.cross(self.velocity))
            axis.normalize()
            newPos = self.rotate_point_rotation(self.rotation_point,
                                       axis,
                                       rotational_velocity)
            newDist = (newPos - self.rotation_point).magnitude()
            theoryDist = ((self.position + self.velocity) - self.rotation_point).magnitude()
            if newDist <= theoryDist:
                self.velocity = newPos - self.position
                if self.reeling_in:
                    self.velocity = self.velocity - (diff * 2)

        if abs(self.acceleration) > self.MAX_ACCELERATION:
            self.acceleration = self.acceleration.normalized() * self.MAX_ACCELERATION
        self.velocity += self.acceleration
        if abs(self.velocity) > self.MAX_VELOCITY:
            self.velocity = self.velocity.normalized() * self.MAX_VELOCITY
        self.position += self.velocity
        self.acceleration = Vector3()
        
        lims = []
        room = game.manager.room
        for d in room.dimensions:
            lims.append(d / 2)
        
        if self.position[0] > lims[0] or \
            self.position[0] < -lims[0] or \
            self.position[1] > lims[1] or \
            self.position[1] < -lims[1] or \
            self.position[2] > lims[2] or \
            self.position[2] < -lims[2]:
            
            self.outside_room(room)
