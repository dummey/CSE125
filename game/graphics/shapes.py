import sys
sys.path = ["../deps"] + sys.path

from math import pi, sin, cos, acos, atan2, asin
from itertools import izip_longest
import time
from euclid import *

import pyglet
from pyglet.gl import *
from pyglet.graphics import vertex_list_indexed, vertex_list

import game

def vec(*args):
    return (GLfloat * len(args))(*args)

class Primitive(object):
    """
    Base class for 3D objects.  Subclasses must overwrite _geometry().
    To access, use the memoized method get().  Render using draw().
    """
    def __init__(self, *args, **kwargs):
        self.vertex_list = self._geometry(*args, **kwargs)

    def _geometry(self):
        return NotImplementedError

    @classmethod
    def get(cls, *args, **kwargs):
        cache_kwargs = kwargs.copy()
        cache_kwargs["cls"] = cls.__name__
        if (str(args), str(cache_kwargs)) in game.manager.graphics_cache:
            # print "get = from cache: %s %s" % (str(args), str(cache_kwargs))
            return game.manager.graphics_cache[(str(args), str(cache_kwargs))]
        else:
            # print "get = create: %s %s" % (str(args), str(cache_kwargs))
            temp = cls(*args, **kwargs)
            game.manager.graphics_cache[(str(args), str(cache_kwargs))] = temp
            return temp

    def _create_vertex_list(self, vertices, normals, indices):
        return vertex_list_indexed(len(vertices)//3,
                                   indices,
                                   ('v3f/static', vertices),
                                   ('n3f/static', normals))

    def _create_vertex_list_textured(self, vertices, normals, textures, indices):
        return vertex_list_indexed(len(vertices)//3,
                                   indices,
                                   ('v3f/static', vertices),
                                   ('n3f/static', normals),
                                   ('t3f/static', textures))

    def draw_at(self, x, y, z, x_rot, y_rot, z_rot, color=(0.5, 0.5, 0.5)):
        glColor3f(*color)
        glPushMatrix()
        glTranslated(x, y, z)
        glRotatef(x_rot, 1, 0, 0)
        glRotatef(y_rot, 0, 1, 0)
        glRotatef(z_rot, 0, 0, 1)
        self.vertex_list.draw(GL_TRIANGLES)
        glPopMatrix()

    def draw(self, position, forward, color=(0.5, 0.5, 0.5), texture=None):
        glColor3f(*color)
        glPushMatrix()

        view_forward = forward.normalize()

        if abs(view_forward.x) == 1:
            view_right = view_forward.cross(Vector3(0,1,0)).normalize()
            view_up = view_forward.cross(view_right).normalize()
        else:
            view_up = view_forward.cross(Vector3(1,0,0)).normalize()
            view_right = view_forward.cross(view_up).normalize()

        viewmatrix = vec(view_right.x, view_right.y, view_right.z, 0.0,
                        view_up.x, view_up.y, view_up.z, 0.0,
                        view_forward.x, view_forward.y, view_forward.z, 0.0,
                        position.x, position.y, position.z, 1.0)

        glMultMatrixf(viewmatrix)

        if texture is not None:
            glEnable(texture.target)
            glBindTexture(texture.target, texture.id)

        self.vertex_list.draw(GL_TRIANGLES)

        if texture is not None:
            glDisable(texture.target)

        glPopMatrix()

    def draw_transparent(self, position, forward, color=(0.5, 0.5, 0.5, 0.5)):
        glColor4f(*color)
        glPushMatrix()
        view_forward = forward.normalize()

        if abs(view_forward.x) == 1:
            view_right = view_forward.cross(Vector3(0,1,0)).normalize()
            view_up = view_forward.cross(view_right).normalize()
        else:
            view_up = view_forward.cross(Vector3(1,0,0)).normalize()
            view_right = view_forward.cross(view_up).normalize()

        viewmatrix = vec(view_right.x, view_right.y, view_right.z, 0.0,
                        view_up.x, view_up.y, view_up.z, 0.0,
                        view_forward.x, view_forward.y, view_forward.z, 0.0,
                        position.x, position.y, position.z, 1.0)

        glMultMatrixf(viewmatrix)

        glEnable(GL_BLEND)
        # glDisable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        glBlendFunc(GL_ONE,GL_ONE_MINUS_SRC_ALPHA)

        self.vertex_list.draw(GL_TRIANGLES)

        glCullFace(GL_BACK)
        # glEnable(GL_CULL_FACE)
        glDisable(GL_BLEND)
        glPopMatrix()

    def draw_rotated(self, position, forward, up, color=(0.5, 0.5, 0.5)):
        glColor3f(*color)
        glPushMatrix()
        view_forward = forward.normalize()
        view_up = up.normalize()
        view_right = up.cross(forward).normalize()

        viewmatrix = vec(view_right.x, view_right.y, view_right.z, 0.0,
                        view_up.x, view_up.y, view_up.z, 0.0,
                        view_forward.x, view_forward.y, view_forward.z, 0.0,
                        position.x, position.y, position.z, 1.0)

        glMultMatrixf(viewmatrix)
        self.vertex_list.draw(GL_TRIANGLES)
        glPopMatrix()


    def draw_compound(self, position_offset, parent_position, parent_forward, color=(0.5, 0.5, 0.5)):
        glColor3f(*color)

        glPushMatrix()

        # transform to compound object space
        glTranslated(parent_position.x, parent_position.y, parent_position.z)
        parent_forward.normalize()
        rot_angle = acos(parent_forward.dot(Vector3(0, 0, 1)))*(180/pi)
        if abs(rot_angle) > 1:
            rot_axis = parent_forward.cross(Vector3(0, 0, 1)).normalized()
            glRotatef(rot_angle, rot_axis.x, rot_axis.y, rot_axis.z)

        # transform to individual element's location
        glTranslated(position_offset.x, position_offset.y, position_offset.z)
        self.vertex_list.draw(GL_TRIANGLES)
        glPopMatrix()

class Cylinder(Primitive):
    def _geometry(self, radius, length, slices):
        # create the vertex and normal arrays
        vertices = []
        normals = []

        u_step = 2 * pi / (length - 1)
        v_step = 2 * pi / (slices - 1)
        u = 0.
        co = 0
        for i in range(int(length)):
            cos_u = cos(u)
            sin_u = sin(u)
            v = 0.
            for j in range(slices):
                cos_v = cos(v)
                sin_v = sin(v)

                d = (radius * cos_v)
                x = d * cos_u
                z = co
                y = radius * sin_v

                nx = cos_u * cos_v
                ny = sin_u * cos_v
                nz = sin_v

                vertices.extend([x, y, z])
                normals.extend([nx, ny, nz])
                v += v_step
            # u += u_step
            co += 1

        # create a list of triangle indices
        indices = []
        for i in range(int(length) - 1):
            for j in range(slices - 1):
                p = i * slices + j
                indices.extend([p, p + slices, p + slices + 1])
                indices.extend([p, p + slices + 1, p + 1])

        return self._create_vertex_list(vertices, normals, indices)

class Laser(Cylinder):
    def __init__(self, length, slices):
        self.vertex_list = self._geometry(0.08, length, slices)

    def draw(self, position, forward, color=(0.5, 0.5, 0.5, 0.5)):
        # print "draw"
        glColor4f(*color)
        glPushMatrix()

        # position = camera_pos-(up*0.73)+(right*0.65)

        view_forward = forward.normalize()

        if abs(view_forward.x) == 1:
            view_right = view_forward.cross(Vector3(0,1,0)).normalize()
            view_up = view_forward.cross(view_right).normalize()
        else:
            view_up = view_forward.cross(Vector3(1,0,0)).normalize()
            view_right = view_forward.cross(view_up).normalize()

        viewmatrix = vec(view_right.x, view_right.y, view_right.z, 0.0,
                        view_up.x, view_up.y, view_up.z, 0.0,
                        view_forward.x, view_forward.y, view_forward.z, 0.0,
                        position.x, position.y, position.z, 1.0)

        glMultMatrixf(viewmatrix)

        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        # glEnable(GL_CULL_FACE)

        self.vertex_list.draw(GL_TRIANGLES)

        # glDisable(GL_CULL_FACE)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glPopMatrix()

    def draw2(self, position, forward, color=(0.5, 0.5, 0.5, 0.5)):
        glColor4f(*color)

        glPushMatrix()

        glTranslated(position.x, position.y, position.z)
        forward.normalize()
        rot_angle = acos(forward.dot(Vector3(0, 0, 1)))*(180/pi)
        if abs(rot_angle) > 1:
            rot_axis = forward.cross(Vector3(0, 0, 1)).normalized()
            glRotatef(-rot_angle, rot_axis.x, rot_axis.y, rot_axis.z)

        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        self.vertex_list.draw(GL_TRIANGLES)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

        glPopMatrix()

    def draw3(self, position, forward, up, color=(0.5, 0.5, 0.5, 0.5)):
        glColor4f(*color)
        glPushMatrix()
        view_forward = forward.normalize()
        view_up = up.normalize()
        view_right = up.cross(forward).normalize()

        viewmatrix = vec(view_right.x, view_right.y, view_right.z, 0.0,
                        view_up.x, view_up.y, view_up.z, 0.0,
                        view_forward.x, view_forward.y, view_forward.z, 0.0,
                        position.x, position.y, position.z, 1.0)

        glMultMatrixf(viewmatrix)
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        self.vertex_list.draw(GL_TRIANGLES)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glPopMatrix()

class GrapplingHook(object):
    def __init__(self, length, slices):
        self.blocks = []

        self.max_length = length/2
        self.roped = length/2

        for i in range(self.roped):
            self.blocks.append(Cylinder.get(0.05,2,4))

        self.block_draw = 0
        self.block_step = 1
        self.drawing = 0
        self.hand = Sphere.get(0.5,5)
        self.finger = Torus.get(0.5,0.4,10,6)

    def draw(self, position, forward, color=(0.5, 0.0, 0.5)):
        if self.drawing:
            # glDisable(GL_LIGHTING)

            # print "drawing grappling hook"

            # Hacky for addition, but it works.
            if (self.block_draw+self.block_step <= self.roped):
                self.block_draw += self.block_step


            for i in range(self.block_draw):
                self.blocks[i].draw(position+(forward*(i)),forward,color)

            self.hand.draw(position+(forward*self.block_draw),forward,color)
            self.finger.draw(position+(forward*(self.block_draw)),forward,color)
            # glEnable(GL_LIGHTING)

            if (self.block_draw <= 0) and (self.block_step < 0):
                self.drawing = 0
        else:
            self.block_draw = 0
            self.block_step = 1

    def start_draw(self):
        self.drawing = 1

    def extend(self, length):
        if length <= self.max_length:
            self.roped = length
        else:
            self.roped = self.max_length

        self.block_step = 3
        self.drawing = 1

    def retract(self):
        # print "testing ret"
        self.block_step = -3


class Torus(Primitive):
    def _geometry(self, radius, inner_radius, slices, inner_slices):
        # create the vertex and normal arrays
        vertices = []
        normals = []

        u_step = 2 * pi / (slices - 1)
        v_step = 2 * pi / (inner_slices - 1)
        u = 0.
        for i in range(slices):
            cos_u = cos(u)
            sin_u = sin(u)
            v = 0.
            for j in range(inner_slices):
                cos_v = cos(v)
                sin_v = sin(v)

                d = (radius + inner_radius * cos_v)
                x = d * cos_u
                y = d * sin_u
                z = inner_radius * sin_v

                nx = cos_u * cos_v
                ny = sin_u * cos_v
                nz = sin_v

                vertices.extend([x, y, z])
                normals.extend([nx, ny, nz])
                v += v_step
            u += u_step

        # create a list of triangle indices
        indices = []
        for i in range(slices - 1):
            for j in range(inner_slices - 1):
                p = i * inner_slices + j
                indices.extend([p, p + inner_slices, p + inner_slices + 1])
                indices.extend([p, p + inner_slices + 1, p + 1])

        return self._create_vertex_list(vertices, normals, indices)

class Block(Primitive):
    def _geometry(self, width, height, depth, width_slices, height_slices, depth_slices, texture_size=None):
        vertices = []
        normals = []

        # lowest to highest, start at top left on all faces and go column by column
        widths = [float(width)/float(width_slices)*i-float(width)/2 for i in range(width_slices+1)]
        heights = [float(height)/float(height_slices)*i-float(height)/2 for i in range(height_slices+1)]
        depths = [float(depth)/float(depth_slices)*i-float(depth)/2 for i in range(depth_slices+1)]

        indices = []
        current = 0

        def add_indices(x, y):
            for w in range(x):
                for h in range(y):
                    indices.extend([current+w*(y+1)+h, current+w*(y+1)+h+1, current+(w+1)*(y+1)+h+1])
                    indices.extend([current+w*(y+1)+h, current+(w+1)*(y+1)+h+1, current+(w+1)*(y+1)+h])

        # front
        for w in widths:
            for h in heights[::-1]:
                vertices.extend([h, w, depths[-1]])
        normals.extend([0, 0, 1]*len(widths)*len(heights))
        add_indices(width_slices, height_slices)
        current += (width_slices+1)*(height_slices+1)

        # back
        for w in widths:
            for h in heights:
                vertices.extend([h, w, depths[0]])
        normals.extend([0, 0, -1]*len(widths)*len(heights))
        add_indices(width_slices, height_slices)
        current += (width_slices+1)*(height_slices+1)

        # top
        for w in widths:
            for d in depths:
                vertices.extend([d, heights[-1], w])
        normals.extend([0, 1, 0]*len(widths)*len(depths))
        add_indices(width_slices, depth_slices)
        current += (width_slices+1)*(depth_slices+1)

        # bottom
        for w in widths:
            for d in depths[::-1]:
                vertices.extend([d, heights[0], w])
        normals.extend([0, -1, 0]*len(widths)*len(depths))
        add_indices(width_slices, depth_slices)
        current += (width_slices+1)*(depth_slices+1)

        # right
        for d in depths:
            for h in heights:
                vertices.extend([widths[-1], d, h])
        normals.extend([1, 0, 0]*len(depths)*len(heights))
        add_indices(depth_slices, height_slices)
        current += (depth_slices+1)*(height_slices+1)

        # left
        for d in depths:
            for h in heights[::-1]:
                vertices.extend([widths[0], d, h])
        normals.extend([-1, 0, 0]*len(depths)*len(heights))
        add_indices(depth_slices, height_slices)

        return self._create_vertex_list(vertices, normals, indices)

class Cube(Block):
    def __init__(self, side, slices):
        self.vertex_list = self._geometry(side, side, side, slices, slices, slices)

class Plane(Block):
    def __init__(self, width, height, width_slices, height_slices):
        self.vertex_list = self._geometry(width, height, 0.01, width_slices, height_slices, 1)

class Sphere(Primitive):
    def _geometry(self, radius, slices):
        vertices = []
        normals = []
        diamonds = [[], [], [], []]

        current = 0

        for i in range(2*slices+1):
            real_i = slices - abs(i-slices)
            theta = i*(pi/2/slices)
            sin_theta = sin(theta)
            cos_theta = cos(theta)

            to_add = max(4*real_i, 1)
            for j in range(to_add):
                phi = real_i > 0 and j*(pi/2/real_i) or 0

                nx = sin_theta*cos(phi)
                ny = sin_theta*sin(phi)
                nz = cos_theta
                normals.extend([nx, ny, nz])

                x = radius*nx
                y = radius*ny
                z = radius*nz
                vertices.extend([x, y, z])

            added = range(current, current+to_add)
            added.append(added[0])
            for e, d in enumerate(diamonds):
                d.append(added[e*real_i:(e+1)*real_i+1])

            current += to_add

        indices = []

        for diamond in diamonds:
            for row in range(0, slices):
                r = range(len(diamond[row]))
                for point in r:
                    indices.extend([diamond[row][point], diamond[row+1][point], diamond[row+1][point+1]])
                for pair in zip(r, r[1:]):
                    indices.extend([diamond[row][pair[1]], diamond[row][pair[0]], diamond[row+1][pair[1]]])
            for row in range(slices+1, len(diamond)):
                r = range(len(diamond[row]))
                for point in r:
                    indices.extend([diamond[row][point], diamond[row-1][point+1], diamond[row-1][point]])
                for pair in zip(r, r[1:]):
                    indices.extend([diamond[row][pair[0]], diamond[row][pair[1]], diamond[row-1][pair[1]]])

        return self._create_vertex_list(vertices, normals, indices)

class Model(Primitive):
    def _grouper(self, n, iterable, fillvalue=None):
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)

    def _geometry(self, model_file, scale_factor=1.0):
        with open(model_file) as f:
            lines = f.readlines()
            raw_vertices = list(self._grouper(3, [float(x)*scale_factor for x in lines[0].split(" ")]))
            raw_normals  = list(self._grouper(3, [float(x) for x in lines[1].split(" ")]))
            raw_textures = list(self._grouper(3, [float(x) for x in lines[2].split(" ")]))
            raw_indices  = self._grouper(3, [int(x) for x in lines[3].split(" ")])

            temp_vertices = []
            indices = []

            for i in raw_indices:
                v = (raw_vertices[i[0]], raw_normals[i[1]], raw_textures[i[2]])
                if v in temp_vertices:
                    indices.append(temp_vertices.index(v))
                else:
                    temp_vertices.append(v)
                    indices.append(len(temp_vertices)-1)

            vertices = []
            normals = []
            textures = []

            for v in temp_vertices:
                vertices.extend(v[0])
                normals.extend(v[1])
                textures.extend(v[2])

            return self._create_vertex_list_textured(vertices, normals, textures, indices)

class ObjectGroup(object):
    """
    Used to create and manage multiple objects and shapes
    in space for consistent rotations and draws. Has relative
    positions for all shapes included
    """
    def __init__(self):
        self.objects = []
        self.positions = []

    def add(self, inObject, position):
        self.objects.append(inObject)
        self.positions.append(position)

    def draw(self, position, forward):
        """ calculate positions and forwards for all grouped objects"""

        for ob,po in zip(self.objects,self.positions):
            draw_position = position + po
            ob.draw(draw_position, forward)
        # glColor3f(*self.color)
        # glPushMatrix()
        #
        # view_forward = forward.normalize()
        #
        # if abs(view_forward.x) == 1:
        #     view_right = view_forward.cross(Vector3(0,1,0)).normalize()
        #     view_up = view_forward.cross(view_right).normalize()
        # else:
        #     view_up = view_forward.cross(Vector3(1,0,0)).normalize()
        #     view_right = view_forward.cross(view_up).normalize()
        #
        # viewmatrix = vec(view_right.x, view_right.y, view_right.z, 0.0,
        #                 view_up.x, view_up.y, view_up.z, 0.0,
        #                 view_forward.x, view_forward.y, view_forward.z, 0.0,
        #                 position.x, position.y, position.z, 1.0)
        #
        # glMultMatrixf(viewmatrix)

class BBox(Primitive):
    def _geometry(self, bbox):
        points = bbox.points()
        vertices = []
        normals = []

        for p in points:
            vertices.extend([p.x, p.y, p.z])
            p.normalize()
            normals.extend([p.x, p.y, p.z])

        indices = [0, 1, 1, 3, 3, 2, 2, 0,
                   4, 5, 5, 7, 7, 6, 6, 4,
                   0, 4, 1, 5, 2, 6, 3, 7]

        return self._create_vertex_list(vertices, normals, indices)

    def draw(self, position, color=(1.0, 1.0, 1.0)):
        glColor3f(*color)
        glPushMatrix()
        glTranslated(position.x, position.y, position.z)
        self.vertex_list.draw(GL_LINES)
        glPopMatrix()

