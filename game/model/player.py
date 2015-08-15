import random
from pprint import pformat
import game
from euclid import Vector3
from game import settings
from game.model import components
from game.model import collision
from game.model import weapons
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
from game.graphics import shapes
from game.resources.spawn import SpawnPoint
from game.settings import DISPLAY_BBOXES, ROCKETS, DISPLAY_PLAYER_BBOXES
from time import time

def ignore_while_dead(fn):
    from functools import wraps
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        if not self.dead: return fn(self, *args, **kwargs)
    return wrapped

#PLAYER STATES
GRABBING = 1
GRABBED = 2
JUMPING = 3

class Player(components.Movement):
    fields = ("team", "name", "health", "kills", "deaths", "state", "spec_control", "laser_mana", "laser_fire", "maxed_laser", "is_firing", "dead", "hit_by")
    debug = True

    #PLAYER STATES
    GRABBING = 1
    GRABBED = 2
    JUMPING = 3

    state = None
    spec_control = False
    grappler = None

    def __init__(self, team, name, pos = Vector3(0,0,0), forward = Vector3(0,0,0), up = Vector3(0,0,0)):
        super(Player, self).__init__(pos, forward, up)

        self.team, self.name = team, name
        self.health = settings.MAX_HEALTH
        self.kills, self.deaths = 0, 0
        self.dead = False

        self.oobb = collision.BoundingBox(-2.5, 2.5, -2.5, 2.5, -2.5, 2.5)
        self.aabb = self.oobb.transformed(self.forward, self.up)
        self.collision_reaction_default = self.collision_reaction
        self.laser_mana = 100
        self.laser_fire = False
        self.maxed_laser = False
        self.is_firing = False
        # because the server is stupid
        self.l_t = time()
        self.last_time = time()
        # hit detector
        self.hit_by = 0
        self.last_health = self.health

    def hit_by_laser(self, player):
        # print player.id
        self.hit_by = player.id
        self.health -= 2

    def render(self):
        sphere = shapes.Sphere.get(1, 12)
        cube = shapes.Cube.get(5, 12)
        color = (0, 0, 0) if self.dead else self.team.rgb
        # TODO: this shouldn't be necessary
        glDisable(GL_CULL_FACE)
        cube.draw_rotated(self.position, self.forward, self.up, color=color)
        tmp_color = Vector3(*color)
        tmp_color = tmp_color * Vector3(0.5, 0.5, 0.5) + Vector3(0.5, 0.5, 0.5)
        sphere.draw(self.position + self.forward * 3, self.forward, color=tmp_color)
        glEnable(GL_CULL_FACE)

        if DISPLAY_BBOXES:
            # bbox = shapes.BBox.get(self.oobb)
            # bbox.draw(self.position)
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)

        # torus.draw(self.position + 3*self.forward, self.forward)

        # cube.draw_compound(Vector3(0, 0, 0), self.position, self.forward)
        # torus.draw_compound(Vector3(0, 0, -3), self.position, self.forward)

    @ignore_while_dead
    def handle_keypress(self, kind, data):
        from game.resources.elements import FastRocket

        mult = 2 if kind == "keypress" else 0
        if kind == "keypress" and data == key.SLASH:
            self.spec_control = not self.spec_control
            print "DEBUG CONTROLS: ", self.spec_control

        if self.spec_control:
            if kind == "keypress" or kind == "keyrelease":
                if data == key.W:
                    self.velocity += self.forward * mult
                elif data == key.S:
                    self.velocity -= self.forward * mult
                elif data == key.D:
                    self.velocity += self.right * mult
                elif data == key.A:
                    self.velocity -= self.right * mult
                elif data == key.T:
                    self.velocity += self.up * mult
                elif data == key.G:
                    self.velocity -= self.up * mult
                elif data == key.F:
                    #tmp key for jumping off
                    if kind == "keypress" and self.collision_reaction == self.collision_reaction_default:
                        self.collision_reaction = self.jump
                        self.state = self.JUMPING
                    elif kind == "keyrelease" and self.collision_reaction == self.jump:
                        self.collision_reaction = self.collision_reaction_default
                        self.state = None
                    pass
                elif data == key.C:
                    #tmp key for grabbing
                    if kind == "keypress" and self.collision_reaction == self.collision_reaction_default:
                        self.oobb.inflate_box(10)
                        self.aabb = self.oobb.transformed(self.forward, self.up)
                        self.collision_reaction = self.grab
                        self.state = self.GRABBING
                    elif kind == "keyrelease" and self.collision_reaction == self.grab:
                        self.oobb.inflate_box(-10)
                        self.aabb = self.oobb.transformed(self.forward, self.up)
                        self.collision_reaction = self.collision_reaction_default
                        self.state = None
                    pass
                elif data == key.R:
                    if kind == "keypress":
                        # print self.rotation_point
                        if self.rotation_point is None:
                            print("begin rotation")
                            self.rotation_point = Vector3(0,0,0)
                        else:
                            print("end rotation")
                            self.rotation_point = None
                elif data == key.Z:
                    # Spawn explosions here!
                    pass
                elif data == key.X:
                    if kind == "keypress" and ROCKETS:
                        # insert overheat check here
                        game.manager.room.add_instance(FastRocket,
                                                       position=self.position+(self.forward * 5),
                                                       forward=self.forward)

                elif data == key.SPACE and self.debug:
                    self.velocity = Vector3(0,0,0)
                elif data == key.L:
                    self.spawn()
        else:
            if kind == "keypress" or kind == "keyrelease":
                if data == key.W:
                    if kind == "keypress" and self.collision_reaction == self.collision_reaction_default:
                        self.collision_reaction = self.collision_reaction_default
                        self.state = None
                        if not self.velocity.magnitude():
                            self.jump(None, None)
                        else:
                            self.collision_reaction = self.jump
                            self.state = self.JUMPING
                    elif kind == "keyrelease" and self.collision_reaction == self.jump:
                        self.collision_reaction = self.collision_reaction_default
                        self.state = None
                elif data == key.S:
                    if kind == "keypress" and self.collision_reaction == self.collision_reaction_default:
                        self.collision_reaction = self.grab
                        self.state = self.GRABBING
                    elif kind == "keyrelease" and self.collision_reaction == self.grab:
                        self.collision_reaction = self.collision_reaction_default
                        self.state = None
                elif data == key.T:
                    self.velocity += self.up * mult
                elif data == key.G:
                    self.velocity -= self.up * mult
                elif data == key.R:
                    if self.rotation_point is None and kind == "keypress":
                        dist, target = weapons.Laser.precalc(self.position, self.forward, [self])


                        self.rotation_point = (self.forward * dist) + self.position

                        self.collision_reaction = self.grab
                        self.state = self.GRABBING
                    else:
                        self.collision_reaction = self.collision_reaction_default
                        self.state = None
                        self.rotation_point = None
                        self.reeling_in = False
                elif data == key.Z:
                    # Spawn explosions here!
                    pass
                elif data == key.X:
                    if kind == "keypress" and ROCKETS:
                        pass
                        # insert overheat check here
                        # game.manager.room.add_instance(Rocket,
                        #         position=self.position+(Vector3(self.forward.x,
                        #         self.forward.y, self.forward.z) * 10),
                        #         forward=self.forward)
                elif data == key.F:
                    if kind == "keypress":
                        self.reeling_in = True
                    elif kind == "keyrelease":
                        self.reeling_in = False
                elif data == key.L:
                    self.spawn()
                elif data == key.P:
                    self.health = 0
                elif data == key.O:
                    self.position = Vector3(2048, 2048, 2048)

        if kind == "orientation":
            if self.forward != data["forward"] or self.up != data["up"]:
                self.forward = data["forward"]
                self.up = data["up"]
                self.orient()
                self.aabb = self.oobb.transformed(self.forward, self.up)

    @ignore_while_dead
    def handle_mouse(self, kind, data):
        if data == mouse.LEFT: # fire laser
            if kind == "mousepress" and not self.maxed_laser:# and self.laser_mana > 0:
                self.laser_fire = True
            elif kind == "mouserelease":
                self.laser_fire = False
        if data == mouse.RIGHT: #grappling hook
            if self.rotation_point is None and kind == "mousepress":
                dist, target = weapons.Laser.precalc(self.position, self.forward, [self])
                self.rotation_point = (self.forward * dist) + self.position
                self.collision_reaction = self.grab
                self.state = self.GRABBING
            else:
                self.collision_reaction = self.collision_reaction_default
                self.state = None
                self.rotation_point = None
                self.reeling_in = False

    def update(self, dt):
        super(Player, self).update(dt)
        t = time()
        if not self.maxed_laser:
            if self.laser_fire and (t-self.l_t >=0.3):
                #if ((t - self.l_t) >= 5):
                self.l_t = t
                if self.laser_mana > 0:
                    self.laser_mana -= 15 #4 #2
                else:
                    self.laser_fire = False
                    self.maxed_laser = True

            else:
                self.laser_mana = min(self.laser_mana + 0.75, 100)
        else:
            self.laser_mana = min(self.laser_mana + 1, 100)
            if self.laser_mana == 100:
                self.maxed_laser = False

        if self.health <= 0 and not self.dead:
            self.dead = True
            self.deaths += 1
            clock.schedule_once(self.spawn, 5)

    def grab(self, other, direction):
        self.rotation_point = None
        self.velocity = Vector3(0,0,0)

    def jump(self, other, direction):
        self.velocity += self.forward * 3

    def spawn(self, dt=None, set_health=True):
        point = self._determine_spawn(self.team)
        if point is not None: #will return None if all the gates have been destroyed
            self.position, self.forward, self.up = point.position + point.forward * 5, point.forward, point.up
            self.velocity = Vector3(0,0,0)
            if set_health:
                self.health, self.dead = 100, False
        else:
            clock.schedule_once(self.spawn, 5)

    @staticmethod
    def _determine_spawn(team):
            points = list(game.manager.room.class_set(SpawnPoint))
            point = None
            while points:
                point = random.choice(points)
                points.remove(point)
                if point.for_team(team) and point.can_spawn():
                    break
                else:
                    point = None
            return point
    
    def outside_room(self, room):
        self.spawn(set_health=False)

class Camera(Player):
    # The "maximum" mouse delta
    # _look_dist = Pair(manager.window.screen.width / 2,
    #                   manager.window.screen.height / 2)
    # _look_dist = Pair(1024 / 2, 768 / 2) # currently not used
    sensitivity = 100.0
    camera_speed = 2.0
    last_position = Vector3(0.0,0.0,0.0)
    mod = False
    def unpack(self, data):
        fields = filter(lambda x: x not in ["forward", "up"], data)
        for field in fields:
            # if field not in ["position"]:
            #     print field
            setattr(self, field, data[field])

    def render(self):
        if self.rotation_point is not None:
            # print "test"
            if self.grappler is None:
                # print "building"
                self.grappler = weapons.Grappler(self.last_position, self.forward, self.up, 100)
                self.grappler.extend()
                self.grappler.render(self.rotation_point)
            else:
                # print "using"
                self.grappler.forward = self.forward
                self.grappler.position = self.last_position
                self.grappler.up = self.up
                self.grappler.extend()
                self.grappler.render(self.rotation_point)
        elif self.grappler is not None:
            self.grappler.retract()
            self.grappler.render(None)
            if self.grappler.gfx.drawing == 0:
                self.grappler = None

        
        # if (self.last_health != self.health):
        #     print self.hit_by
        
        self.last_health = self.health

        if self.laser_fire and not self.maxed_laser:
            laser_position = self.last_position - (self.up*0.73) + (self.right*0.65)
            helix_position = self.last_position - (self.up*2.73) + (self.right*2.65)
            laser = shapes.Laser.get(game.manager.room.dimensions.x, 20)
                        
            t = time()
            
            doalpha = 0.5
            if (t-self.last_time >= 0.3):
                doalpha = 1.0
                self.last_time = t
                
            docolor = (1.0,0.0,0.0,doalpha) if self.team.team_name == "RED" else (0.0,0.0,1.0,doalpha)
            
            laser.draw3(laser_position, self.forward, self.up, color=docolor)
            game.manager.room.laser_helix.draw(helix_position, 200, self.position, self.forward, self.up, self.right, self.team.team_name)

    def place_camera(self):
        self.lookat = self.position + self.forward
        # print "camera forward: %s : camera up: %s" % (self.forward, self.up)
        # print self.last_position
        self.last_position = self.position
        gluLookAt(self.position.x, self.position.y, self.position.z,
                  self.lookat.x, self.lookat.y, self.lookat.z,
                  self.up.x, self.up.y, self.up.z)

    @ignore_while_dead
    def on_mouse_motion(self, x, y, dx, dy):
        """Update the client camera based on mouse motion.

        Use a triangle to represent the max offset and the current offset in
        order to find the angle to rotate by.
        """
        self.mod = True
        if dx:
            tempright = self.right * dx / self.sensitivity
            if abs(tempright) > 0.15:
                tempright = tempright.normalize() * 0.15
            self.forward = (self.forward + tempright).normalized()
            self.right = self.forward.cross(self.up).normalized()

        if dy:
            tempup = self.up * dy / self.sensitivity
            if abs(tempup) > 0.15:
                tempup = tempup.normalize() * 0.15
            self.forward = (self.forward + tempup).normalized()
            self.up = self.right.cross(self.forward).normalized()

    @ignore_while_dead
    def on_mouse_drag(self, x, y, dx, dy, button, modifier):
        """Update the client camera based on mouse motion.

        Use a triangle to represent the max offset and the current offset in
        order to find the angle to rotate by.
        """
        self.mod = True
        if dx:
            tempright = self.right * dx / self.sensitivity
            self.forward = (self.forward + tempright).normalized()
            self.right = self.forward.cross(self.up).normalized()

        if dy:
            tempup = self.up * dy / self.sensitivity
            self.forward = (self.forward + tempup).normalized()
            self.up = self.right.cross(self.forward).normalized()

    @ignore_while_dead
    def check_orientation_keys(self, keyboard):
        if keyboard[key.LEFT]:
            tempright = self.right * 5.0 / self.sensitivity
            self.forward = (self.forward - tempright).normalized()
            self.right = self.forward.cross(self.up).normalized()
            self.mod=True
        if keyboard[key.RIGHT]:
            tempright = self.right * 5.0 / self.sensitivity
            self.forward = (self.forward + tempright).normalized()
            self.right = self.forward.cross(self.up).normalized()
            self.mod=True
        if keyboard[key.UP]:
            tempup = self.up * 5.0 / self.sensitivity
            self.forward = (self.forward + tempup).normalized()
            self.up = self.right.cross(self.forward).normalized()
            self.mod=True
        if keyboard[key.DOWN]:
            tempup = self.up * 5.0 / self.sensitivity
            self.forward = (self.forward - tempup).normalized()
            self.up = self.right.cross(self.forward).normalized()
            self.mod=True

        if self.spec_control:
            if keyboard[key.Q]:
                tempright = self.right * 2.0 / self.sensitivity
                self.up = (self.up - tempright).normalized()
                self.right = self.forward.cross(self.up).normalized()
                self.mod=True
            if keyboard[key.E]:
                tempright = self.right * 2.0 / self.sensitivity
                self.up = (self.up + tempright).normalized()
                self.right = self.forward.cross(self.up).normalized()
                self.mod=True
        elif not self.spec_control:
            if keyboard[key.A]:
                tempright = self.right * 2.0 / self.sensitivity
                self.up = (self.up - tempright).normalized()
                self.right = self.forward.cross(self.up).normalized()
                self.mod=True
            if keyboard[key.D]:
                tempright = self.right * 2.0 / self.sensitivity
                self.up = (self.up + tempright).normalized()
                self.right = self.forward.cross(self.up).normalized()
                self.mod=True
        return self.mod