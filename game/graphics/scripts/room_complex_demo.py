import sys
sys.path = ["../../../deps", "../../../"] + sys.path

from math import pi, sin, cos

from pyglet.gl import *
from pyglet.window import key
import pyglet
from threading import Thread

from euclid import *
from game.graphics.shapes import *
from game.model.components import *
from game.graphics.particles import Explosions
from game.resources.elements import Laser
from game.settings import *

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)

from game.model.player import Camera


keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)
window.set_exclusive_mouse(True)
window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
fullscreen = False

fps_display = pyglet.clock.ClockDisplay() # see programming guide pg 48

mouse_dxdy = [0, 0]
sensitivity = 100.0
camera_speed = 3.0
room_size = 512
camera_pos = Vector3(0, 0, room_size/2)
camera_rot = Quaternion()

right   = Vector3(1, 0, 0)
up      = Vector3(0, 1, 0)
forward = Vector3(0, 0, -1)

testcam = Camera("Team Butts", "Butt", camera_pos, forward, 0)


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(CAMERA_PERSPECTIVE, width / float(height), .1, 2000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

def update(dt):

    # fill type
    if keyboard[key._1]:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # solid
    if keyboard[key._2]:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # wireframe
    if keyboard[key._3]:
        glPolygonMode(GL_FRONT_AND_BACK, GL_POINT) # point

    global camera_pos
    global camera_rot

    global forward
    global up
    global right

    # print right, up, forward

    # Noclip movement forward/back
    if keyboard[key.S]:
        camera_pos = camera_pos - forward * camera_speed
    if keyboard[key.W]:
        camera_pos = camera_pos + forward * camera_speed

    # camera
    if keyboard[key.LEFT]:
        tempright = right * 5.0 / sensitivity
        forward = (forward - tempright).normalized()
        right = forward.cross(up).normalized()
    if keyboard[key.RIGHT]:
        tempright = right * 5.0 / sensitivity
        forward = (forward + tempright).normalized()
        right = forward.cross(up).normalized()
    if keyboard[key.UP]:
        tempup = up * 5.0 / sensitivity
        forward = (forward + tempup).normalized()
        up = right.cross(forward).normalized()
    if keyboard[key.DOWN]:
        tempup = up * 5.0 / sensitivity
        forward = (forward - tempup).normalized()
        up = right.cross(forward).normalized()
    # Noclip camera roll
    if keyboard[key.Q]:
        tempright = right * -5.0 / sensitivity
        up = (up + tempright).normalized()
        right = forward.cross(up).normalized()
    if keyboard[key.E]:
        tempright = right * -5.0 / sensitivity
        up = (up - tempright).normalized()
        right = forward.cross(up).normalized()
    # Noclip camera strafe
    if keyboard[key.A]:
        camera_pos = camera_pos - right * camera_speed *.5
    if keyboard[key.D]:
        camera_pos = camera_pos + right * camera_speed *.5
    # Noclip camera up/down
    if keyboard[key.R]:
        camera_pos = camera_pos + up * camera_speed *.5
    if keyboard[key.F]:
        camera_pos = camera_pos - up * camera_speed *.5
    if keyboard[key.SPACE]:
        l = Laser(position=camera_pos, forward=forward)
        l.right = right
        toDraw.append(l)
        pass



    # Quit the game.
    if keyboard[key.ESCAPE]:
        sys.exit()

    # fullscreen
    if keyboard[key._6]:
        window.set_fullscreen()

pyglet.clock.set_fps_limit(60)
pyglet.clock.schedule(update)

@window.event
def on_mouse_motion(x, y, dx, dy):
    global camera_rot

    testcam.on_mouse_motion(x, y, dx, dy)

    global right
    global up
    global forward

    # look right/left
    if (dx != 0):
        tempright = right * dx / sensitivity
        forward = (forward + tempright).normalized()
        right = forward.cross(up).normalized()

    # look up/down
    if (dy != 0):
        tempup = up * dy / sensitivity
        forward = (forward + tempup).normalized()
        up = right.cross(forward).normalized()

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera()

    lighting()

    # walls
    # glColor3f(0.5, 0, 0.3) # Purple
    wall.draw_at(0, 0, -room_size/2, 0, 0, 0, color=(0.05, 0, 0.03)) # front
    wall.draw_at(0, 0,  room_size/2, 0, 0, 0, color=(0.05, 0, 0.03)) # behind
    wall.draw_at( room_size/2, 0, 0, 0, 90, 0, color=(0.05, 0, 0.03)) # right
    wall.draw_at(-room_size/2, 0, 0, 0, 90, 0, color=(0.05, 0, 0.03)) # left
    wall.draw_at(0, -room_size/2, 0, 90, 0, 0, color=(0.05, 0, 0.03)) # below
    # wall.draw_at(0,  room_size/2, 0, 90, 0, 0) # top

    # cubes
    cube.draw_at( 190, -190,  190, 0, 0, 0, color=(0.05, 0, 0.03))
    cube.draw_at( 190, -190, -190, 0, 0, 0, color=(0.05, 0, 0.03))
    cube.draw_at(-190, -190,  190, 0, 0, 0, color=(0.05, 0, 0.03))
    cube.draw_at(-190, -190, -190, 0, 0, 0, color=(0.05, 0, 0.03))
    # glColor3f(0, 1.0, 0) # green

    bigCube.draw_at( 100, 0, 0, 0, 0, 0, color=(0, 0.5, 0))
    bigCube.draw_at(-100, 0, 0, 0, 0, 0, color=(0, 0.5, 0))
    bigCube.draw_at(0,  100, 0, 0, 0, 0, color=(0, 0.5, 0))
    bigCube.draw_at(0, -100, 0, 90, 0, 0, color=(0, 0.5, 0))
    bigCube.draw_at(0, 0,  100, 0, 0, 0, color=(0, 0.5, 0))
    bigCube.draw_at(0, 0, -100, 0, 0, 0, color=(0, 0.5, 0))

    # sphere
    # glColor4f(0, 0, 0.5, 1.0) # blue
    sphere.draw_at(0, 0, 0, 0, 0, 0, color=(0, 0, 0.5))

    lightCube.draw_at(0, 500, 0, 0, 0, 0, color=(1, 0, 0))

    explosions.draw(camera_pos, up)

    for el in toDraw:
        el.render()

    man.render()

    to_ortho()
    fps_display.draw()
    from_ortho()



def camera():
    # setting perspective (maximum viewing distance)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(CAMERA_PERSPECTIVE, window.width/float(window.height), .1, 2000.)
    glMatrixMode(GL_MODELVIEW)

    lookat = Vector3()
    lookat = camera_pos + forward
    gluLookAt(camera_pos.x, camera_pos.y, camera_pos.z, lookat.x, lookat.y, lookat.z, up.x, up.y, up.z)

def lighting():
    def vec(*args):
        return (GLfloat * len(args))(*args)

    glLightfv(GL_LIGHT0, GL_POSITION, vec(190, -190,  190, 1)) # xyz homogenous
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, vec(-1, 1, -1))
    glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, vec(0.0))
    glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, vec(45.0))

    glLightfv(GL_LIGHT1, GL_POSITION, vec(190, 190,  -190, 1)) # xyz homogenous
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, vec(-1, -1, 1))
    glLightfv(GL_LIGHT1, GL_SPOT_EXPONENT, vec(0.0))
    glLightfv(GL_LIGHT1, GL_SPOT_CUTOFF, vec(45.0))

    glLightfv(GL_LIGHT2, GL_POSITION, vec(-190, 190,  190, 1)) # xyz homogenous
    glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, vec(1, -1, -1))
    glLightfv(GL_LIGHT2, GL_SPOT_EXPONENT, vec(0.0))
    glLightfv(GL_LIGHT2, GL_SPOT_CUTOFF, vec(45.0))

    glLightfv(GL_LIGHT3, GL_POSITION, vec(190, 190,  190, 1)) # xyz homogenous
    glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, vec(-1, -1, -1))
    glLightfv(GL_LIGHT3, GL_SPOT_EXPONENT, vec(0.0))
    glLightfv(GL_LIGHT3, GL_SPOT_CUTOFF, vec(45.0))

    glLightfv(GL_LIGHT4, GL_POSITION, vec(0, 500,  0, 1)) # xyz homogenous
    glLightfv(GL_LIGHT4, GL_SPOT_DIRECTION, vec(0, -1, 0))
    glLightfv(GL_LIGHT4, GL_SPOT_EXPONENT, vec(0.0))
    glLightfv(GL_LIGHT4, GL_SPOT_CUTOFF, vec(45.0))


def to_ortho():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window.width, 0 , window.height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def from_ortho():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def setup():
    glClearColor(1, 1, 1, 1) # rgba (white)
    glColor3f(0.5, 0, 0.3) # rgb (red)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_FOG)

    def vec(*args):
        return (GLfloat * len(args))(*args)

    glEnable(GL_LIGHTING)

    # glEnable(GL_TEXTURE_2D)
    glShadeModel(GL_SMOOTH)
    # glClearColor(0.5, 0.5, 0.5, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_DST_ALPHA)

    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)
    glLightfv(GL_LIGHT1, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)
    glLightfv(GL_LIGHT2, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)
    glLightfv(GL_LIGHT3, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)

    glLightfv(GL_LIGHT4, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    glLightfv(GL_LIGHT4, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)

    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glEnable(GL_LIGHT4)

    glFogi(GL_FOG_MODE, GL_EXP)
    glFogfv(GL_FOG_COLOR, vec(0.5, 0.5, 0.5, 0.5))
    glFogf(GL_FOG_DENSITY, 0.01)
    # glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogf(GL_FOG_START, 0.0)
    glFogf(GL_FOG_END, 1.0)

    glShadeModel(GL_SMOOTH)

    # glColorMaterial allows the actual objects to determine their lighting colors
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0.5, 0.5, 1.0)) # rgba (purple)
    glMaterialfv(GL_FRONT, GL_SPECULAR, vec(1, 1, 1, 1)) # rgba (white)
    glMaterialf(GL_FRONT, GL_SHININESS, 50) # [0-128] with 0 being most shiny


setup()
wall = Plane(room_size, room_size, 64, 64)
sphere = Sphere(35, 12)
cube = Cube(20, 12)
bigCube = Cube(40, 12)
lightCube = Cube(5, 8)
toDraw = []

class PersonModel(Movement):
    def __init__(self, x, y, z, rotx, roty, rotz, color=(1.0,0.0,0.0)):
        self.man_pos = (x, y, z, rotx, roty, rotz)
        self.color = color

    def render(self):
        man_head = Sphere(1.7, 12)
        man_body = Block(4.5, 7, 2, 12, 12, 12)
        man_limb = Block(1.5, 5, 1.5, 12, 12, 12)
        man_head.draw_at(0 + self.man_pos[0], 0 + self.man_pos[1], 0 + self.man_pos[2],
            0 + self.man_pos[3], 0 + self.man_pos[4], 0 + self.man_pos[5])
        #  Body
        man_body.draw_at(0 + self.man_pos[0], 5 + self.man_pos[1], 0 + self.man_pos[2],
            0 + self.man_pos[3], 0 + self.man_pos[4], 0 + self.man_pos[5])
        # right arm
        man_limb.draw_at(3 + self.man_pos[0], 5 + self.man_pos[1], 0 + self.man_pos[2],
            0 + self.man_pos[3], 0 + self.man_pos[4], -20 + self.man_pos[5])
        # left Arm
        man_limb.draw_at(-3 + self.man_pos[0], 5 + self.man_pos[1], 0 + self.man_pos[2],
            0 + self.man_pos[3], 0 + self.man_pos[4], 20 + self.man_pos[5])
        # Feets
        man_limb.draw_at(2 + self.man_pos[0], 10 + self.man_pos[1], 0 + self.man_pos[2],
            0 + self.man_pos[3], 0 + self.man_pos[4], -17 + self.man_pos[5])
        # left Arm
        man_limb.draw_at(-2 + self.man_pos[0], 10 + self.man_pos[1], 0 + self.man_pos[2],
            0 + self.man_pos[3], 0 + self.man_pos[4], 17 + self.man_pos[5])


man = PersonModel(0, 0, 150, 0, 0, 0)

t = Thread(target=pyglet.app.run)
t.start()
# print "thread started"
explosions = Explosions(10)
explosions.new_explosion(Vector3(0,0,0), (1.0,1.0,1.0), 50, 1.0, 0.01, 200)

pyglet.app.run()