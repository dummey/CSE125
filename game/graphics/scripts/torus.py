#!/usr/bin/env python
# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

'''Displays a rotating torus using OpenGL.

This example demonstrates:

 * Using a 3D projection on a window by overriding the default on_resize
   handler
 * Enabling multisampling if available
 * Drawing a simple 3D primitive using vertex and index arrays
 * Using a display list
 * Fixed-pipeline lighting

'''

import sys
sys.path = ["../deps"] + sys.path;

from math import pi, sin, cos

from pyglet.gl import *
from pyglet.window import key
import pyglet
import euclid

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)

keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

label = pyglet.text.Label('Hello, torus!',
                          font_name='Times New Roman',
                          font_size=12,
                          x=0, y=0, color=(0,0,0,255),
                          anchor_x='left', anchor_y='bottom')

camera_pos = [0, 0, 4]
camera_rot = [0, 0, 0]

@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

def update(dt):
    # fill types
    if keyboard[key._1]:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # solid
    if keyboard[key._2]:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # wireframe
    if keyboard[key._3]:
        glPolygonMode(GL_FRONT_AND_BACK, GL_POINT) # point
        
    global sensitivity
        
    # sensitivity controls
    if keyboard[key._4]:
        sensitivity -= 1.0 if sensitivity > 5.0 else 0.0
    if keyboard[key._5]:
        sensitivity += 1.0 if sensitivity > 5.0 else 0.0
        

    # movement
    if keyboard[key.S]:
        camera_pos[0] -= sin(camera_rot[1] / 180.0 * pi)
        camera_pos[1] += sin(camera_rot[0] / 180.0 * pi)
        camera_pos[2] += cos(camera_rot[1] / 180.0 * pi)
    if keyboard[key.W]:
        camera_pos[0] += sin(camera_rot[1] / 180.0 * pi)
        camera_pos[1] -= sin(camera_rot[0] / 180.0 * pi)
        camera_pos[2] -= cos(camera_rot[1] / 180.0 * pi)
        
    # strafe
    if keyboard[key.A]:
        camera_pos[0] += sin((camera_rot[1] - 90.0) / 180.0 * pi)
        # camera_pos[1] -= sin(camera_rot[2] / 180.0 * pi)
        camera_pos[1] -= cos((camera_rot[1] - 90.0) / 180.0 * pi)
    if keyboard[key.D]:
        camera_pos[0] += sin((camera_rot[1] + 90.0) / 180.0 * pi)
        # camera_pos[1] -= sin(camera_rot[2] / 180.0 * pi)
        camera_pos[2] -= cos((camera_rot[0] + 90.0) / 180.0 * pi)
    
    # camera
    if keyboard[key.LEFT]:
        camera_rot[1] -= 1
        if camera_rot[1] < -360:
            camera_rot[1] += 360
    if keyboard[key.RIGHT]:
        camera_rot[1] += 1
        if camera_rot[0] > 360:
            camera_rot[0] -= 360
    if keyboard[key.UP]:
        camera_rot[0] -= 1
        if camera_rot[0] < -360:
            camera_rot[0] += 360
    if keyboard[key.DOWN]:
        camera_rot[0] += 1
        if camera_rot[0] > 360:
            camera_rot[0] -= 360
    if keyboard[key.Q]:
        camera_rot[2] -= 1
        if camera_rot[2] < -360:
            camera_rot[2] += 360
    if keyboard[key.E]:
        camera_rot[2] += 1
        if camera_rot[2] > 360:
            camera_rot[2] -= 360

    label.text = "X: %d Y: %d Z: %d " % tuple(camera_pos) + "pitch: %d yaw: %d roll: %d" % tuple(camera_rot)

pyglet.clock.set_fps_limit(30)
pyglet.clock.schedule(update)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera()
    for t in torus:
      t.draw()
    to_ortho()
    label.draw()
    from_ortho()

def camera():
    glRotatef(camera_rot[0], 1.0, 0.0, 0.0);  # rotate x axis
    glRotatef(camera_rot[1], 0.0, 1.0, 0.0);  # rotate y axis
    glRotatef(camera_rot[2], 0.0, 0.0, 1.0);  # rotate z axis
    glTranslated(-camera_pos[0], -camera_pos[1], -camera_pos[2])  # translate screen to camera position

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
    # One-time GL setup
    glClearColor(1, 1, 1, 1) # rgba (white)
    glColor3f(1, 0, 0) # rgb (red)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
    # but this is not the case on Linux or Mac, so remember to always
    # include it.
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # Define a simple function to create ctypes arrays of floats:
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

class Torus(object):
    def __init__(self, radius, inner_radius, slices, inner_slices):
        # Create the vertex and normal arrays.
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

        # Create ctypes arrays of the lists
        vertices = (GLfloat * len(vertices))(*vertices)
        normals = (GLfloat * len(normals))(*normals)

        # Create a list of triangle indices.
        indices = []
        for i in range(slices - 1):
            for j in range(inner_slices - 1):
                p = i * inner_slices + j
                indices.extend([p, p + inner_slices, p + inner_slices + 1])
                indices.extend([p,  p + inner_slices + 1, p + 1])
        indices = (GLuint * len(indices))(*indices)

        # Compile a display list
        self.list = glGenLists(1) # create an array of lists (only one here)
        glNewList(self.list, GL_COMPILE) # only compile list, don't execute it yet

        glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT) # push context

        glEnableClientState(GL_VERTEX_ARRAY) # context can display vertexes
        glEnableClientState(GL_NORMAL_ARRAY) # context can display normals
        glVertexPointer(3, GL_FLOAT, 0, vertices) # array of vertices in 3-space, stride is 0 for non-interleaved arrays
        glNormalPointer(GL_FLOAT, 0, normals) # same as above except normals are always in 3-space
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)

        glPopClientAttrib() # pop context

        glEndList() # end list

    def draw(self):
        glCallList(self.list)

setup()
# a = Torus(1.1, 0.2, 100, 50),


torus = [
    Torus(1.1, 0.2, 100, 50),
    Torus(0.7, 0.2, 75, 40),
    Torus(0.3, 0.2, 50, 30)
]

pyglet.app.run()
