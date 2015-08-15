from euclid import Vector3, Point3
import game
from game.model import components
from game.model import collision
from game.graphics import particles
from game.graphics import shapes

class Laser(object):

    def __init__(self, position, forward, up, length, color):
        self.position = position
        self.forward = forward
        self.up = up
        self.length = length
        self.time_left = 5
        self.color = color

    @staticmethod
    def precalc(position, forward, exclude):

        length = 0
        obj_hit = None
        nxtpos = position + forward
        ray = collision.Ray(position, forward)
        elements = filter(lambda x: x.__class__.__name__ != "Laser",
                          game.manager.room.instances.itervalues())
        collided = []

        for element in elements:
            # curr_diff = (position - element.position).magnitude()
            # next_diff = (nxtpos - element.position).magnitude()
            # if curr_diff < next_diff:
            #     continue
            if element not in exclude and ray.collides(element.aabb, element.position):
                collided.append(element)

        collided.sort(key=lambda x: (position - x.position).magnitude_squared())
        if len(collided):
            length = (position - collided[0].position).magnitude()
            obj_hit = collided[0]
        else:
            length = game.manager.room.dimensions.magnitude()
        return (length, obj_hit)

    def update(self):
        self.time_left -= 1
        return self.time_left == 0

    def render(self):
        laser = shapes.Laser.get(self.length, 20)
        # laser = shapes.Laser.get(self.length, 20)
        laser.draw3(self.position, self.forward, self.up, color=self.color)

class Lasers(object):
    def __init__(self):
        self.lasers = {}

    def add_laser(self, position=None, forward=None, up=None, length=None, shot_by=None, shot_team=None):
        if shot_by != game.manager.camera.id:
            color = (1.0,0.0,0.0,0.5) if shot_team == "RED" else (0.0,0.0,1.0,0.5)
            self.lasers[shot_by] = Laser(position, forward, up, length, color=color)

    def render(self):
        for player in self.lasers.keys():
            if self.lasers[player].update():
                del self.lasers[player]
            else:
                self.lasers[player].render()

class Grappler(components.Position):
    fields = ("length",)

    def __init__(self, position, forward, up, length):
        self.length = length
        self.forward = forward
        self.position = position
        self.up = up
        self.gfx = shapes.GrapplingHook(length, 12)
        self.connection = Vector3(0.0,0.0,0.0)

    #
    def update(self, dt):
        pass

    def extend(self):
        self.gfx.extend(self.length)
        
    def retract(self):
        self.gfx.retract()

    def render(self, attached_to):
        # calculate position as spinning or retracting
        draw_right = self.up.cross(self.forward).normalize() 
        draw_position = self.position - self.up + draw_right
        if attached_to is None:
            draw_forward = self.connection - self.position
        else:
            draw_forward = attached_to - self.position
            self.connection = attached_to
            
        # print "draw_position: %s ; draw_forward: %s" % (draw_position, draw_forward)
        self.gfx.draw(draw_position, draw_forward)

