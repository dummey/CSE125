import sys
sys.path = ["../../../deps", "../../../", "../"] + sys.path

from math import pi, sin, cos

from pyglet.gl import *
from pyglet.window import key
import pyglet

from euclid import *
from shapes import *


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
window.set_size(1024,768)
fullscreen = False

fps_display = pyglet.clock.ClockDisplay() # see programming guide pg 48

mouse_dxdy = [0, 0]
sensitivity = 100.0
camera_pos = Vector3(0, 0, 200)
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
    gluPerspective(60., width / float(height), .1, 1000.)
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

    # movement
    if keyboard[key.S]:
        # camera_pos = camera_pos - forward
        testcam.on_key_press(key.S, 1)
    if keyboard[key.W]:
        # camera_pos = camera_pos + forward
        testcam.on_key_press(key.W, 1)

    # camera
    if keyboard[key.LEFT]:
        # tempright = right * 5.0 / sensitivity
        # forward = (forward - tempright).normalized()
        # right = forward.cross(up).normalized()
        testcam.on_key_press(key.LEFT, 1)
    if keyboard[key.RIGHT]:
        # tempright = right * 5.0 / sensitivity
        # forward = (forward + tempright).normalized()
        # right = forward.cross(up).normalized()
        testcam.on_key_press(key.RIGHT, 1)
    if keyboard[key.UP]:
        # tempup = up * 5.0 / sensitivity
        # forward = (forward + tempup).normalized()
        # up = right.cross(forward).normalized()
        testcam.on_key_press(key.UP, 1)
    if keyboard[key.DOWN]:
        # tempup = up * 5.0 / sensitivity
        # forward = (forward - tempup).normalized()
        # up = right.cross(forward).normalized()
        testcam.on_key_press(key.DOWN, 1)
    if keyboard[key.A]:
        # tempright = right * 5.0 / sensitivity
        # up = (up + tempright).normalized()
        # right = forward.cross(up).normalized()
        testcam.on_key_press(key.A, 1)
    if keyboard[key.D]:
        # tempright = right * 5.0 / sensitivity
        # up = (up - tempright).normalized()
        # right = forward.cross(up).normalized()
        testcam.on_key_press(key.D, 1)

    # Quit the game.
    if keyboard[key.ESCAPE]:
        sys.exit()

    # fullscreen
    if keyboard[key.F]:
        window.set_fullscreen()

pyglet.clock.set_fps_limit(60)
pyglet.clock.schedule(update)

@window.event
def on_mouse_motion(x, y, dx, dy):
    global camera_rot

    testcam.on_mouse_motion(x, y, dx, dy)

    # global right
    # global up
    # global forward
    #
    # # look right/left
    # if (dx != 0):
    #     tempright = right * dx / sensitivity
    #     forward = (forward + tempright).normalized()
    #     right = forward.cross(up).normalized()
    #
    # # look up/down
    # if (dy != 0):
    #     tempup = up * dy / sensitivity
    #     forward = (forward + tempup).normalized()
    #     up = right.cross(forward).normalized()

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera()
    # walls
    wall.draw_at(0, 0, -200, 0, 0, 0) # front
    wall.draw_at(0, 0,  200, 0, 0, 0) # behind
    wall.draw_at( 200, 0, 0, 0, 90, 0) # right
    wall.draw_at(-200, 0, 0, 0, 90, 0) # left
    wall.draw_at(0, -200, 0, 90, 0, 0) # below
    # cubes
    cube.draw_at( 180, -180,  180, 0, 0, 0)
    cube.draw_at( 180, -180, -180, 0, 0, 0)
    cube.draw_at(-180, -180,  180, 0, 0, 0)
    cube.draw_at(-180, -180, -180, 0, 0, 0)
    # sphere
    sphere.draw_at(0, 0, 0, 0, 0, 0)
    to_ortho()
    fps_display.draw()
    from_ortho()

def camera():
    # angle, axis = camera_rot.get_angle_axis()
    # glRotatef(angle*180/pi, axis.x, axis.y, axis.z)
    # glTranslated(-camera_pos.x, -camera_pos.y, -camera_pos.z)  # translate screen to camera position
    # lookat = Vector3()
    # lookat = testcam.position + testcam.forward
    # # print(testcam.up)
    # # print(testcam.position)
    # # print(lookat)
    # gluLookAt (testcam.position.x, testcam.position.y, testcam.position.z, lookat.x, lookat.y, lookat.z, testcam.up.x, testcam.up.y, testcam.up.z)
    # testpos = Vector3(0,0,200)
    # testlook = Vector3(0,0,199)
    # testup = Vector3(0,1,0)
    # gluLookAt(camera_pos.x, camera_pos.y, camera_pos.z, lookat.x, lookat.y, lookat.z, up.x, up.y, up.z)
    testcam.place_camera()

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
    glColor3f(1, 0, 0) # rgb (red)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    def vec(*args):
        return (GLfloat * len(args))(*args)

    glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, .5, 1, 0)) # xyz homogenous
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1)) # rgba (blue)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (white)

    glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
    glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0, 0.3, 1)) # rgba (purple)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1)) # rgba (white)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50) # [0-128] with 0 being most shiny


setup()
wall = Plane(400, 400, 200, 200)
sphere = Sphere(75, 12)
cube = Cube(40, 12)

pyglet.app.run()
