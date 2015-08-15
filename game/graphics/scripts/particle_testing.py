import sys
sys.path = ["../../../deps", "../../../"] + sys.path

from math import pi, sin, cos
from random import *

from pyglet.gl import *
from pyglet.window import key, mouse
import pyglet
import random
import copy

from euclid import *
from game.graphics.shapes import *
from game.model.components import *
from game.graphics.particles import Particle, Explosion, Explosions, Laser_Glow, Puff
# from game.graphics.shader import Shader


try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config, vsync=True)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)

from game.model.player import Camera


keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)
window.set_exclusive_mouse(True)
window.set_size(1024,768)
fullscreen = False

firin_mah_laza = 0

fps_display = pyglet.clock.ClockDisplay() # see programming guide pg 48
fps_test = pyglet.clock.Clock()

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
    gluPerspective(30., width / float(height), .1, 1000.)
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
    global firin_mah_laza

    # print right, up, forward

    # Noclip movement forward/back
    if keyboard[key.S]:
        camera_pos = camera_pos - forward * camera_speed
    if keyboard[key.W]:
        camera_pos = camera_pos + forward * camera_speed
    firin_mah_laza = 0
    if keyboard[key.Z]:
        firin_mah_laza = 1
        # print "test"
        shootat = camera_pos + (forward * 100)
        explosions.new_explosion(shootat, (0.0,1.0,0.0), 20, 1.0, 0.03, 200)

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
def on_mouse_press(x, y, button, modifiers):
    global firin_mah_laza

    # if button & mouse.RIGHT:
    #     testGrapple.extend(2000)
    # 
    # if button & mouse.LEFT:
    #     testGrapple.retract()

@window.event
def on_mouse_release(x, y, button, modifiers):
    global firin_mah_laza

    if button & mouse.LEFT:
        firin_mah_laza = 0

testint = 0.01
@window.event
def on_draw():
    global testint
    global forward
    global camera_pos
    global up
    global explosion
    global e
    global firin_mah_laza

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera()

    lighting()

    # walls
    # glColor3f(0.5, 0, 0.3) # Purple
    wall.draw(Vector3(0,0,-room_size/2),Vector3(0,0,1),Vector3(0.0,0.0,0.0))
    wall.draw(Vector3(0,0,room_size/2), Vector3(0,0,-1),Vector3(0.0,0.0,0.0))
    wall.draw(Vector3(room_size/2,0,0),Vector3(1,0,0),Vector3(0.0,0.0,0.0))
    wall.draw(Vector3(-room_size/2,0,0),Vector3(-1,0,0),Vector3(0.0,0.0,0.0))
    wall.draw(Vector3(0, -room_size/2, 0), Vector3(0,1,0),Vector3(0.0,0.0,0.0))
    wall.draw(Vector3(0, room_size/2, 0), Vector3(0,-1,0),Vector3(0.0,0.0,0.0))

    # cubes
    cube.draw(Vector3(0,0,0),Vector3(0,0,1),Vector3(1.0,1.0,1.0))
    # cube.draw_at( 190, -190,  190, 0, 0, 0)
    # cube.draw_at( 190, -190, -190, 0, 0, 0)
    # cube.draw_at(-190, -190,  190, 0, 0, 0)
    # cube.draw_at(-190, -190, -190, 0, 0, 0)
    # glColor3f(0, 1.0, 0) # green
    # man2.draw(Vector3(-190.0,-120.0,0.0),Vector3(0.0,0.0,1.0))
    # bigCube.draw_at( 100, 0, 0, 0, 0, 0)
    # bigCube.draw_at(-190, -150, 0, 0, 0, 0)
    # bigCube.draw_at(0,  100, 0, 0, 0, 0)
    # bigCube.draw_at(0, -100, 0, 90, 0, 0)
    # bigCube.draw_at(0, 0,  100, 0, 0, 0)
    # bigCube.draw_at(0, 0, -100, 0, 0, 0)

    # sphere
    # glColor4f(0, 0, 0.5, 1.0) # blue
    # sphere.draw_at(0, 0, 0, 0, 0, 0)
    # laser = Laser(200, 20)
    # testLaser.draw3(camera_pos, forward, up, color=(0.0, 1.0, 0.0, 0.5))

    if firin_mah_laza:
        # testLaser.draw(camera_pos-(up*0.73)+(right*0.65),forward,(1.0,0.0,0.0,0.5))
        # testLaser.draw2(camera_pos, forward, (1.0,0.0,0.0,0.5))
        # testLaser.draw3(camera_pos, forward, up, (1.0,0.0,0.0,0.5))
        # testLaser.draw4(camera_pos, forward, up, (1.0,0.0,0.0,0.5))
        testGlow.draw(camera_pos-(up*2.73)+(right*2.65), 200, camera_pos, forward, up, right)
        testPuff.draw(camera_pos, up)
        pass

    # testGrapple.draw(camera_pos-(up*0.73)-(right*0.65),forward,(1.0,0.0,1.0))

    # lightCube.draw_at(0, 500, 0, 0, 0, 0)

    # man.render()
    if False:
        testGlow.draw(camera_pos-(up*2.73)+(right*2.65), 200, camera_pos, forward, up, right)
    # explosions.draw(camera_pos, up)

    to_ortho()
    fps_display.draw()
    from_ortho()


def camera():
    # setting perspective (maximum viewing distance)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, 1024.0/768.0, 1, 2000)
    glMatrixMode(GL_MODELVIEW)

    lookat = Vector3()
    lookat = camera_pos + forward
    gluLookAt(camera_pos.x, camera_pos.y, camera_pos.z, lookat.x, lookat.y, lookat.z, up.x, up.y, up.z)

def lighting():
    def vec(*args):
        return (GLfloat * len(args))(*args)

    glLightfv(GL_LIGHT0, GL_POSITION, vec(0, 0,  250, 1)) # xyz homogenous
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, vec(-1, 1, -1))
    glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, vec(0.0))
    glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, vec(45.0))

    glLightfv(GL_LIGHT1, GL_POSITION, vec(0, 0,  -250, 1)) # xyz homogenous
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

    glLightfv(GL_LIGHT4, GL_POSITION, vec(0, 0, 50, 1)) # xyz homogenous
    glLightfv(GL_LIGHT4, GL_SPOT_DIRECTION, vec(0, 0, -1))
    glLightfv(GL_LIGHT4, GL_SPOT_EXPONENT, vec(0.0))
    glLightfv(GL_LIGHT4, GL_SPOT_CUTOFF, vec(45.0))


def to_ortho():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window.width, 0 , window.height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glColor3f(1.0,1.0,1.0)
    glLoadIdentity()

def from_ortho():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def setup():
    # global shader

    glClearColor(1, 1, 1, 1) # rgba (white)
    glColor3f(0.5, 0, 0.3) # rgb (red)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_COLOR_MATERIAL)
    # glEnable(GL_FOG)

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


    # glClearColor(1, 1, 1, 1) # rgba (white)
    # glColor3f(0.5, 0, 0.3) # rgb (red)
    # glEnable(GL_DEPTH_TEST)
    # glEnable(GL_CULL_FACE)
    # glEnable(GL_COLOR_MATERIAL)
    # glEnable(GL_FOG)
    # # glEnable(GL_BLEND)
    #
    # def vec(*args):
    #     return (GLfloat * len(args))(*args)
    #
    # glEnable(GL_LIGHTING)
    #
    #
    # glShadeModel(GL_SMOOTH)
    # glClearDepth(1.0)
    # glDepthFunc(GL_LEQUAL)
    # glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    #
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_DST_ALPHA)
    # # glEnable(GL_BLEND)
    #
    # glLightfv(GL_LIGHT0, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)
    # glLightfv(GL_LIGHT1, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    # glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)
    # glLightfv(GL_LIGHT2, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    # glLightfv(GL_LIGHT2, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)
    # glLightfv(GL_LIGHT3, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    # glLightfv(GL_LIGHT3, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)
    #
    # glLightfv(GL_LIGHT4, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (low white)
    # glLightfv(GL_LIGHT4, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (bright white)
    #
    # glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHT1)
    # # glEnable(GL_LIGHT2)
    # #     glEnable(GL_LIGHT3)
    # #     glEnable(GL_LIGHT4)
    #
    # glFogi(GL_FOG_MODE, GL_EXP)
    # glFogfv(GL_FOG_COLOR, vec(0.5, 0.5, 0.5, 0.5))
    # glFogf(GL_FOG_DENSITY, 0.01)
    # glHint(GL_FOG_HINT, GL_DONT_CARE)
    # glFogf(GL_FOG_START, 0.0)
    # glFogf(GL_FOG_END, 1.0)
    #
    # # glShadeModel(GL_SMOOTH)
    #
    # # glColorMaterial allows the actual objects to determine their lighting colors
    # glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    # glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0.5, 0.5, 1.0)) # rgba (purple)
    # glMaterialfv(GL_FRONT, GL_SPECULAR, vec(1, 1, 1, 1)) # rgba (white)
    # glMaterialf(GL_FRONT, GL_SHININESS, 50) # [0-128] with 0 being most shiny



setup()
wall = Plane(room_size, room_size, 64, 64)
sphere = Sphere(35, 12)
cube = Cube(20, 12)
bigCube = Cube(40, 12)
lightCube = Cube(5, 8)
testCylinder = Cylinder(0.1,500,20)
# testLaser = Laser(5000,20)
# testGrapple = GrapplingHook(200,20)
testGlow = Laser_Glow()
testPuff = Puff(position=Vector3(0.0,0.0,0.0), color=(0.0,1.0,0.0), density=10, life=1.0, fade=0.03, size=50, fire_vector=Vector3(0.0,0.0,1.0))
testPuff.reset(position=Vector3(0.0,0.0,100.0), color=(0.0,1.0,0.0), density=10, life=1.0, fade=0.03, size=50, fire_vector=Vector3(0.0,0.0,1.0), right_vector=Vector3(1.0,0.0,0.0))

# man2 = ObjectGroup()
# man2.add(Sphere(1.7, 12, color=(0.0,0.0,150.0)), Vector3(0,3,0))
# e = []
# explosion = Explosion(position=Vector3(0,0,0), color=(1.0,1.0,1.0), density=100, life=1.0, fade=0.01, size=50)
explosions = Explosions(10)
# explosions.new_explosion(Vector3(0,0,0), (1.0,1.0,1.0), 100, 1.0, 0.01, 100)


pyglet.app.run()
