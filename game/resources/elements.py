import pyglet
from euclid import Vector3
from game import settings
from game.model import components
from game.model import collision, player
from game.graphics import shapes
from game.graphics.particles import Explosion
from game.graphics import utils
from game.resources.wall import Wall
from game.settings import DISPLAY_BBOXES

# room.unpack_add() uses getattr and will crash without this
from game.model.player import Camera, Player
from game.model.weapons import Laser


class ColorObject(components.Position):
    def __init__(self, *args, **kwargs):
        if "color" in kwargs:
            self.color = kwargs["color"]
            del kwargs["color"]
        else:
            self.color = (0.5, 0.5, 0.5)
        super(ColorObject, self).__init__(*args, **kwargs)

class TorusTest(ColorObject):
    def __init__(self, *args, **kwargs):
        super(TorusTest, self).__init__(*args, **kwargs)
        self.radius = 5
        self.inner_radius = 0.5
        self.slices = 100
        self.inner_slices = 50
        x = y = self.radius + self.inner_radius
        z = self.inner_radius
        self.oobb = collision.BoundingBox(-x, x, -y, y, -z, z)
        self.aabb = self.oobb.transformed(self.forward, self.up)

    def render(self):
        shape = shapes.Torus.get(self.radius,
                                 self.inner_radius,
                                 self.slices,
                                 self.inner_slices)
        shape.draw(self.position, self.forward, color=self.color)

        if DISPLAY_BBOXES:
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)

class SphereTest(ColorObject):
    def __init__(self, *args, **kwargs):
        super(SphereTest, self).__init__(*args, **kwargs)
        self.radius = 20
        self.slices = 12
        x = y = z = self.radius
        self.oobb = collision.BoundingBox(-x, x, -y, y, -z, z)
        self.aabb = self.oobb.transformed(self.forward, self.up)

    def render(self):
        sphere = shapes.Sphere.get(self.radius, self.slices)
        sphere.draw(self.position, self.forward, color=self.color)

        if DISPLAY_BBOXES:
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)

class BouncySphere(components.Movement):
    def __init__(self, *args, **kwargs):
        super(BouncySphere, self).__init__(*args, **kwargs)
        self.radius = 20
        self.slices = 12
        x = y = z = self.radius
        self.oobb = collision.BoundingBox(-x, x, -y, y, -z, z)
        self.aabb = self.oobb.transformed(self.forward, self.up)

    def render(self):
        sphere = shapes.Sphere.get(self.radius, self.slices)
        sphere.draw(self.position, self.forward)

        if DISPLAY_BBOXES:
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)

class CubeTest(ColorObject):
    def __init__(self, *args, **kwargs):
        super(CubeTest, self).__init__(*args, **kwargs)
        self.side = 20
        self.slices = 1
        x = y = z = self.side / 2
        self.oobb = collision.BoundingBox(-x, x, -y, y, -z, z)
        self.aabb = self.oobb.transformed(self.forward, self.up)

    def render(self):
        cube = shapes.Cube.get(self.side, self.slices)
        cube.draw(self.position, self.forward, color=self.color)

        if DISPLAY_BBOXES:
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)

class FPSDisplay(components.Element):
    def render(self):
        fps_display = pyglet.clock.ClockDisplay()
        utils.to_ortho()
        fps_display.draw()
        utils.from_ortho()

class Rocket(components.Movement):
    def __init__(self, *args, **kwargs):
        super(Rocket, self).__init__(*args, **kwargs)
        #self.velocity = (0,0,0)
        self.radius = 1
        self.slices = 12
        x = y = z = self.radius
        self.oobb = collision.BoundingBox(-x, x, -y, y, -z, z)
        self.aabb = self.oobb.transformed(self.forward, self.up)


    def render(self):
        sphere1 = shapes.Sphere.get(1, 10)
        sphere1.draw_rotated(self.position, self.forward, self.right, color=(1,0,0))

    def collision_check(self, other):
        if super(Rocket, self).collision_check(other):
            if isinstance(other, player.Player):
                other.health -= 10
            return "boom"

class FastRocket(Rocket):
    def collision_check(self, other):
        pos = Vector3(self.position.x, self.position.y, self.position.z)
        self.position = self.position + self.forward
        for i in range(900):
            self.position = self.position + self.forward
            ret = super(Rocket, self).collision_check(other)
            # print "ret is %s"%ret
            if ret == True or ret == "boom":
                if isinstance(other, player.Player):
                    other.health -= 10
                return "boom"
        self.position = pos
        return "no boom"

# class Laser(components.Position):
#     # def __init__(self, *args, **kwargs):
#     #     super(Laser, self).__init(*args, **kwargs)
#     #     self.oobb = None
#     #     self.aabb = None
#
#     def render(self):
#         rec = shapes.Block.get(100, 1, 1, 1, 1, 5)
#         rec.draw_rotated(self.position, self.forward, self.right, color=(1,0,0))

class PowerUp(components.Movement):
    collidable = False

    def __init__(self, *args, **kwargs):
        super(PowerUp, self).__init__(*args, **kwargs)
        self.radius = 20
        self.slices = 12
        self.color = (0.0, 1.0, 0.0, 0.5)
        x = y = z = self.radius
        self.oobb = collision.BoundingBox(-x, x, -y, y, -z, z)
        self.aabb = self.oobb.transformed(self.forward, self.up)

    def collision_reaction(self, other, direction):
        if isinstance(other, player.Player):
            if other.health < settings.MAX_HEALTH:
                other.health += 0.1

    def render(self):
        sphere = shapes.Sphere.get(self.radius, self.slices)
        sphere.draw_transparent(self.position, self.forward, color=self.color)

        if DISPLAY_BBOXES:
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)

class Cliff(ColorObject):
    def __init__(self, *args, **kwargs):
        super(Cliff, self).__init__(*args, **kwargs)
        self.side = 25
        self.oobb = collision.BoundingBox(-self.side/2, self.side/2, -self.side/2, self.side/2, -self.side/2, self.side/2)
        self.aabb = self.oobb.transformed(self.forward, self.up)
        self.color = (0.0, 0.5, 0.06)

    def render(self):
        shape = shapes.Block.get(self.side, self.side, self.side, 1, 1, 1)
        shape.draw(self.position, self.forward, color=self.color)

        if DISPLAY_BBOXES:
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)

class XWing(ColorObject):
    def __init__(self, *args, **kwargs):
        super(XWing, self).__init__(*args, **kwargs)
        self.side = 25
        self.oobb = collision.BoundingBox(-self.side/2, self.side/2, -self.side/2, self.side/2, -self.side/2, self.side/2)
        self.aabb = self.oobb.transformed(self.forward, self.up)
        self.color = (1.0, 1.0, 1.0)
        self.texture = pyglet.image.load('../models/xwing.jpg').get_texture()

    def render(self):
        shape = shapes.Model.get("../models/xwing.txt", scale_factor=1.0/333.0)
        shape.draw(self.position, self.forward, color=self.color, texture=self.texture)

        if DISPLAY_BBOXES:
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)


