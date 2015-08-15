from euclid import Vector3
from game.model import components
from game.model import collision
from game.graphics import shapes
from game.settings import DISPLAY_BBOXES
import game
import pyglet

class Wall(components.Position):
    def __init__(self, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self.size = 500
        x = y = self.size / 2
        self.oobb = collision.BoundingBox(-x-50, x+50, -y-50, y+50, 0, -100)
        self.aabb = self.oobb.transformed(self.forward, self.up)
        self.color = (0.1, 0, 0.06)
        texture_image = pyglet.image.load('../images/star_background.jpg')
        # self.texture = texture_image.get_texture()
        self.texture = pyglet.image.TileableTexture.create_for_image(texture_image)

    def render(self):
        shape = shapes.Plane.get(self.size, self.size, 64, 64)
        shape.draw(self.position, self.forward, color=self.color, texture=self.texture)

        if DISPLAY_BBOXES:
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)

