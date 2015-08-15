import pyglet
from pyglet.gl import *
import game
from euclid import Vector3
from game.settings import *
from BeautifulSoup import BeautifulStoneSoup

# camera_pos   = Vector3(0, 0, 0)
# up      = Vector3(0, 1, 0)
# forward = Vector3(0, 0, -1)
# def camera():
#     global up
#     global forward
#     global camera_pos
#     lookat = Vector3()
#     lookat = camera_pos + forward
#     gluLookAt(camera_pos.x, camera_pos.y, camera_pos.z, lookat.x, lookat.y, lookat.z, up.x, up.y, up.z)

def vec(*args):
    return (GLfloat * len(args))(*args)

def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


def to_ortho():
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, game.manager.window.width, 0 , game.manager.window.height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def from_ortho():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)

def setup_opengl():
    glClearColor(1, 1, 1, 1) # rgba (white)
    glColor3f(1, 0, 0) # rgb (red)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHT1)

    # Texture initializations
    glShadeModel(GL_SMOOTH)
    glClearDepth(1.0)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_DST_ALPHA)

    # Low specular light to reduce/remove shinyness
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(0.1, 0.1, 0.1, 1)) # rgba (blue)
    # High Diffusal light for very apparent/obvious shading
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))    # rgba (white)

    # No need for multiple light sources... yet.
    # glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
    # glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
    # glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

    # glColorMaterial allows the actual objects to determine their lighting colors
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0.5, 0.5, 1.0)) # rgba (white)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1)) # rgba (white)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50) # [0-128] with 0 being most shiny
    
    #################

    # Fog settings
    
    # glFogi(GL_FOG_MODE, GL_EXP)
    # glFogfv(GL_FOG_COLOR, vec(0.5, 0.5, 0.5, 0.5))
    # glFogf(GL_FOG_DENSITY, 0.01)
    # # glHint(GL_FOG_HINT, GL_DONT_CARE)
    # glFogf(GL_FOG_START, 0.0)
    # glFogf(GL_FOG_END, 1.0)

def begin_draw():
    # on_resize(game.manager.window.width, game.manager.window.height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Setup projection matrix for draw
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(CAMERA_PERSPECTIVE, game.manager.window.width/float(game.manager.window.height), .1, 2000.)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()

    # place lighting relative to world coordinates for constant light placement
    # Placing a light source 500 units above the box (alpha == 1: position, alpha == 0: directional)
    glLightfv(GL_LIGHT0, GL_POSITION, vec(0, 500, 0, 1)) # xyz homogenous

    # Spotlight effects (not fully working yet)
    # glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, vec(0, -1, 0))
    # glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, vec(50.0))
    # glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, vec(85.0))

def load_collada(file):
    data = {}
    f = open("../duck.dae")
    xml = BeautifulStoneSoup(f)
    
    geometry = xml.library_geometries
    geometry = geometry.findAll("float_array")
    
    data["vertices"] = geometry[0].contents[0].split(' ')
    data["normal"] = geometry[1].contents[0].split(' ')
    data["indices"] = xml.polylist.p.contents[0].split(' ')

    return data
    