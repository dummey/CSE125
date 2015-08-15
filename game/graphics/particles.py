import sys, os, inspect
top_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.join(os.getcwd() ,inspect.getfile(inspect.currentframe())))))

# Mess with for scripting
# sys.path = [top_path] + sys.path

from math import pi, sin, cos, acos
import time
from euclid import *

import pyglet
from pyglet.gl import *
from pyglet.graphics import vertex_list_indexed, vertex_list
from pyglet import image

from game import manager

import random

def vec(*args):
    return (GLfloat * len(args))(*args)

class Particle(object):
    """
    Base class for particles.
    Once instantiated, render using draw().
    All particle textures are determined by the effect that uses them (streamlines speed)   
    """
    active = False
    def __init__(self, *args, **kwargs):
        accept = ("position", "velocity", "acceleration", "life", "fade", "color")
     
        for arg in accept:
              setattr(self, arg, kwargs.get(arg))

        self.active = True

    def draw(self, look_vector, up_vector):
        # Draw The Particle Using Our RGB Values, Fade The Particle Based On It's Life
        if self.active:
            glColor4f(self.color[0], self.color[1], self.color[2], self.life)
      
            glPushMatrix()
            
            # Do billboarding here
            # temp_look = look_vector - self.position
            temp_look = look_vector - self.position

            billboard_right = up_vector.cross(temp_look).normalized()
            billboard_up = temp_look.cross(billboard_right).normalized()
            billboard_look = billboard_right.cross(billboard_up).normalized()
            
            viewmatrix = vec(billboard_right.x, billboard_right.y, billboard_right.z, 0.0,
                            billboard_up.x, billboard_up.y, billboard_up.z, 0.0,
                            billboard_look.x, billboard_look.y, billboard_look.z, 0.0,
                            self.position.x, self.position.y, self.position.z, 1.0)
                            
            glMultMatrixf(viewmatrix)

            glBegin(GL_TRIANGLE_STRIP)
                        
            # Front facing 2 dimensional texture
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1.0, -1.0,  0.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f( 1.0, -1.0,  0.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f( -1.0,  1.0,  0.0)
            glTexCoord2f(1.0, 1.0)
            glVertex3f( 1.0,  1.0,  0.0)
            
            glEnd()
                        
            glPopMatrix()
            
            self.update()
            
    
    def draw_laser(self, part_pos, camera_pos, up_vector):
        # Draw The Particle Using Our RGB Values, Fade The Particle Based On It's Life
        if self.active:
            glColor4f(self.color[0], self.color[1], self.color[2], self.life)
      
            glPushMatrix()
            
            # Do billboarding here
            # temp_look = look_vector - self.position
            temp_look = camera_pos - part_pos

            billboard_right = up_vector.cross(temp_look).normalized()
            billboard_up = temp_look.cross(billboard_right).normalized()
            billboard_look = billboard_right.cross(billboard_up).normalized()
            
            viewmatrix = vec(billboard_right.x, billboard_right.y, billboard_right.z, 0.0,
                            billboard_up.x, billboard_up.y, billboard_up.z, 0.0,
                            billboard_look.x, billboard_look.y, billboard_look.z, 0.0,
                            part_pos.x, part_pos.y, part_pos.z, 1.0)
                            
            glMultMatrixf(viewmatrix)

            glBegin(GL_TRIANGLE_STRIP)
                        
            # Front facing 2 dimensional texture
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1.0, -1.0,  0.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f( 1.0, -1.0,  0.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f( -1.0,  1.0,  0.0)
            glTexCoord2f(1.0, 1.0)
            glVertex3f( 1.0,  1.0,  0.0)
            
            glEnd()
                        
            glPopMatrix()
    
    def update(self):
        # update positional and velocity information
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.life = self.life - self.fade
            
        if self.life <= 0.0:
            self.active = False
                
    def reset(self, *args, **kwargs):
        accept = ("position", "velocity", "acceleration", "life", "fade", "color")
        
        for arg in accept:
            setattr(self, arg, kwargs.get(arg))
              
        self.active = True
     
class Effect(object):
    active = False
    def __init__(self, *args, **kwargs):
        accept = ("position", "color", "density", "life", "fade", "size")
        
        for arg in accept:
              setattr(self, arg, kwargs.get(arg))
        
        self.active = True
        self.particles = []
        
        if self.density == None:
            self.density = 100
        
        global top_path
        
        # Load in particle bmp (location of particle bmp is hazy right now)
        pic = image.load(top_path+"/game/graphics/Particle.bmp")
        # pic = image.load("Particle.bmp")
        self.texture = pic.get_texture()
        ix = pic.width
        iy = pic.height
        rawimage = pic.get_image_data()
        format = 'RGBA'
        pitch = rawimage.width * len(format)
        # Gets image data for setting the image data below
        myimage = rawimage.get_data(format, pitch)

        # Pyglet sets the texture for use later
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        # Sets up image data and texture parameters (can be played with later)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, myimage) 
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                
        # init particles in reset_particles()
        self.reset_particles()
    
    def reset_particles(self):
        return NotImplementedError
    
    def reset(self):
        return NotImplementedError
                
    def draw(self, look_vector, up_vector):
        if self.active == True:
            # full lighting for particles, independant of environment lighting            
            glDisable(GL_LIGHTING)
            glDisable(GL_DEPTH_TEST)
            # glDepthMask(GL_FALSE)
            
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            # glBlendFunc(GL_ONE, GL_ONE)
            glBlendFunc(GL_SRC_ALPHA,GL_ONE)
            glHint(GL_POINT_SMOOTH_HINT,GL_NICEST)
            glEnable(GL_BLEND)
            
            """Turn these on only if Fog is on"""
            # glDisable(GL_FOG)
            
            # enable and set texture to particle
            glEnable(GL_TEXTURE_2D)
            glBindTexture(self.texture.target, self.texture.id)
            
            # draw, pardner!
            for num in range(self.density):
                self.particles[num].draw(look_vector, up_vector)
            
            # turn off the crap we dun' need no mo'
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)
            
            """Turn these on only if Fog is on"""
            # glEnable(GL_FOG)
                        
            glEnable(GL_LIGHTING)
            glEnable(GL_DEPTH_TEST)
            # glDepthMask(GL_TRUE)
            
            self.life = self.life - self.fade
        
            if self.life <= 0.0:
                self.active = False
            
    def delete(self):
        for p in self.particles:
            del p
    
        del self.particles
        del self
        

class Laser_Glow(Effect):
    """
    Laser helix particle effect.
    Instantiates and resets particles."""    
    def reset_particles(self):
        self.particle_positions = [(0.5,0.0),(0.5,0.5),(0.0,0.5),(-0.5,0.5),(-0.5,0.0),(-0.5,-0.5),(0.0,-0.5),(0.5,-0.5)]
        self.p_red = Particle(position=Vector3(0.0,0.0,0.0), velocity=Vector3(0.0,0.0,0.0), acceleration=Vector3(0.0,0.0,0.0), life=1.0, fade=0.0, color=(1.0,0.0,0.0))
        self.p_blu = Particle(position=Vector3(0.0,0.0,0.0), velocity=Vector3(0.0,0.0,0.0), acceleration=Vector3(0.0,0.0,0.0), life=1.0, fade=0.0, color=(0.0,0.0,1.0))
        self.rotation_speed = 3
        self.rotating = 0
        
        
    def reset(self, *args, **kwargs):
        pass
        
        # print "reset_laser_glow"
        
    def draw(self, laser_position, laser_length, camera_pos, look_vector, up_vector, right_vector, team):
        length = laser_length / 40
        
        forward_step = 12 # may be changed
        
        # full lighting for particles, independant of environment lighting            
        glDisable(GL_LIGHTING)
        # glDisable(GL_DEPTH_TEST)
        # glDepthMask(GL_FALSE)
        
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glBlendFunc(GL_ONE, GL_ONE)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        glHint(GL_POINT_SMOOTH_HINT,GL_NICEST)
        glEnable(GL_BLEND)
        
        """Turn these on only if Fog is on"""
        # glDisable(GL_FOG)
        
        # enable and set texture to particle
        glEnable(GL_TEXTURE_2D)
        glBindTexture(self.texture.target, self.texture.id)
        
        # print self.texture.id, self.texture.target
        # print self.p_red, self.p_blu
        
        # DO THE DRAW
        for i in range(length):
            for par in self.particle_positions:
                p_pos = (up_vector*par[0])+(right_vector*par[1])
                p_pos.normalize()
                p_pos = p_pos + laser_position+(look_vector*forward_step)
                
                
                p = self.p_red if team == "RED" else self.p_blu
                
                p.draw_laser(p_pos, camera_pos, up_vector)
                
                forward_step += 12
                
        # turn off the crap we dun' need no mo'
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

        """Turn these on only if Fog is on"""
        # glEnable(GL_FOG)

        glEnable(GL_LIGHTING)
        # glEnable(GL_DEPTH_TEST)
        # glDepthMask(GL_TRUE)
        
        self.rotating += 1
        if (self.rotating == self.rotation_speed):
            self.rotating = 0
            self.particle_positions.insert(0,self.particle_positions.pop())
        

class Explosion(Effect):
    """
    Explosion particle effect. Instantiates (and resets) particles
    and then uses their inherent draw effects.
    """
    def reset_particles(self):
        """
        Sets all particles to random velocities and accelerations
        based off initial explosion position. Reset_particles resets
        to position, allowing an explosion to be reused multiple times
        """
        # firsttime = time.time()
        self.particles = []
        
        sensitivity = 1000.0 / self.size
        
        for num in range(self.density):
            self.particles.append(Particle(position=Vector3(0.0,0.0,0.0), velocity=Vector3(0.0,0.0,0.0), acceleration=Vector3(0.0,0.0,0.0), life=1.0, fade=0.0, color=(0.0,0.0,0.0)))
        
    def pp_reset(self):
        sensitivity = 1000.0 / self.size
        
        for num in range(self.density):
            velx = random.uniform(-1.0,1.0) / sensitivity
            vely = random.uniform(-1.0,1.0) / sensitivity
            velz = random.uniform(-1.0,1.0) / sensitivity
            velocity = Vector3(velx, vely, velz)
            accx = random.uniform(-1.0,1.0) / sensitivity
            accy = random.uniform(-1.0,1.0) / sensitivity
            accz = random.uniform(-1.0,1.0) / sensitivity
            acceleration = Vector3(accx, accy, accz)
            # self.particles.append(Particle(position=self.position, velocity=velocity, acceleration=acceleration, life=self.life, fade=self.fade, color=self.color))
            self.particles[num].reset(position=self.position, velocity=velocity, acceleration=acceleration, life=self.life, fade=self.fade, color=self.color)
        
    def reset(self, *args, **kwargs):
        accept = ("position", "color", "density", "life", "fade", "size")

        for arg in accept:
              setattr(self, arg, kwargs.get(arg))
              
        self.active = True
        self.pp_reset()
        # self.reset_particles()

class Puff(Effect):
    """
    Puff particle effect. Drawn for jumps and
    landings
    """
    def reset_particles(self):
        """
        Sets all particles to random velocities and accelerations
        based off initial explosion position. Reset_particles resets
        to position, allowing an explosion to be reused multiple times
        """
        # firsttime = time.time()
        self.particles = []
        
        sensitivity = 1000.0 / self.size
        
        for num in range(self.density):
            self.particles.append(Particle(position=Vector3(0.0,0.0,0.0), velocity=Vector3(0.0,0.0,0.0), acceleration=Vector3(0.0,0.0,0.0), life=1.0, fade=0.0, color=(0.0,0.0,0.0)))
        
    def pp_reset(self, fire_vector, right_vector):
        sensitivity = 1000.0 / self.size
        
        for num in range(self.density):
            velr = (random.uniform(-1.0,1.0) / sensitivity) * right_vector
            velu = (random.uniform(-1.0,1.0) / sensitivity) * (fire_vector.cross(right_vector).normalize())
            velf = (random.uniform(0.0,1.0) / sensitivity) * fire_vector
            velocity = velf + velr + velu
            # velocity = (fire_vector * (random.uniform(0.0,1.0) / sensitivity))
            # print velocity
            accr = (random.uniform(-1.0,1.0) / sensitivity) * right_vector
            accu = (random.uniform(-1.0,1.0) / sensitivity) * (fire_vector.cross(right_vector).normalize())
            accf = (random.uniform(0.0,1.0) / sensitivity) * fire_vector
            # accz = random.uniform(-1.0,1.0) / sensitivity
            acceleration = accf + accr + accu
            
            # print velocity, acceleration
            # self.particles.append(Particle(position=self.position, velocity=velocity, acceleration=acceleration, life=self.life, fade=self.fade, color=self.color))
            self.particles[num].reset(position=self.position, velocity=velocity, acceleration=acceleration, life=self.life, fade=self.fade, color=self.color)
        
    def reset(self, *args, **kwargs):
        accept = ("position", "color", "density", "life", "fade", "size")

        for arg in accept:
              setattr(self, arg, kwargs.get(arg))
        
        
        fire_vector = kwargs["fire_vector"]
        right_vector = kwargs["right_vector"]
        # print fire_vector
        
        self.active = True
        self.pp_reset(fire_vector, right_vector)
        # self.reset_particles()
        
class H_Well(Effect):
    """
    Healing Well Particle Effect (inward)
    """
    def reset_particles(self):
        """
        Sets all particles to random velocities and accelerations
        based off initial explosion position. Reset_particles resets
        to position, allowing an explosion to be reused multiple times
        """
        # firsttime = time.time()
        self.particles = []
        
        sensitivity = 1000.0 / self.size
        
        self.draw_from = 0
        self.last_time = time.time()
        
        for num in range(self.density):
            self.particles.append(Particle(position=Vector3(0.0,0.0,0.0), velocity=Vector3(0.0,0.0,0.0), acceleration=Vector3(0.0,0.0,0.0), life=1.0, fade=0.0, color=(0.0,0.0,0.0)))
            
        self.posn = Vector3(*self.position)
    
    #
    def draw(self, camera_pos, up_vector):
        # full lighting for particles, independant of environment lighting            
        glDisable(GL_LIGHTING)
        # glDisable(GL_DEPTH_TEST)
        # glDepthMask(GL_FALSE)
        
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glBlendFunc(GL_ONE, GL_ONE)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        glHint(GL_POINT_SMOOTH_HINT,GL_NICEST)
        glEnable(GL_BLEND)
        
        """Turn these on only if Fog is on"""
        # glDisable(GL_FOG)
        
        # enable and set texture to particle
        glEnable(GL_TEXTURE_2D)
        glBindTexture(self.texture.target, self.texture.id)
        
        # DO THE DRAW
        for p in self.particles:
            p.draw(camera_pos, up_vector)
                
        # turn off the crap we dun' need no mo'
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

        """Turn these on only if Fog is on"""
        # glEnable(GL_FOG)

        glEnable(GL_LIGHTING)
        # glEnable(GL_DEPTH_TEST)
        # glDepthMask(GL_TRUE)
        
        #reset some particles for constant effect
        t = time.time()
        if (t-self.last_time >= 0.5):
            self.last_time = t
            self.pp_reset()
    
    def pp_reset(self):
        sensitivity = 1000.0 / self.size
        
        
        
        for num in range(20):
            index = self.draw_from + num
            
            velr = (random.uniform(-1.0,1.0) / sensitivity)
            velu = (random.uniform(-1.0,1.0) / sensitivity)
            velf = (random.uniform(-1.0,1.0) / sensitivity)
            pstart = self.posn + (Vector3(velf, velr, velu).normalize() * self.size)
            # velocity = (fire_vector * (random.uniform(0.0,1.0) / sensitivity))
            # print velocity
            # accz = random.uniform(-1.0,1.0) / sensitivity
            
            velocity = (self.posn - pstart).normalize()
                        
            # print velocity, acceleration
            # self.particles.append(Particle(position=self.position, velocity=velocity, acceleration=acceleration, life=self.life, fade=self.fade, color=self.color))
            self.particles[index].reset(position=pstart, velocity=velocity, acceleration=Vector3(0.0,0.0,0.0), life=self.life, fade=self.fade, color=self.color)
            
            if (index+20 > self.density):
                self.draw_from = 0
        self.draw_from += 20

        
    def reset(self, *args, **kwargs):
        accept = ("position", "color", "density", "life", "fade", "size")

        for arg in accept:
              setattr(self, arg, kwargs.get(arg))
        
        # print fire_vector
        
        self.active = True
        self.pp_reset()
        # self.reset_particles()

class Explosions(object):
    """
    The list of explosions defined by MAX_EXPLOSIONS
    that allows us to create a certain amount and not
    blahblahbreak the renderer.
    """
    def __init__(self, max_explosions, rate_limit=False):
        self.rate_limit = rate_limit
        self._MAX_EXPLOSIONS = max_explosions
        self._MAX_PARTICLES = 20
        self.explosions = []
        self.active = []
        self.last_active = 0
        self.total_active = 0
        self.last_time = time.time()
        # Initialize our list of explosions
        for e in range(self._MAX_EXPLOSIONS):
            self.explosions.append(Explosion(position=Vector3(0,0,0), color=(1.0,1.0,1.0), density=self._MAX_PARTICLES, life=1.0, fade=0.00, size=1))
            self.active.append(False)
    
    def draw(self, camera_pos, up_vector):
        for e in range(self._MAX_EXPLOSIONS):
            # if explosion is on
            if self.active[e] == True:                
                self.explosions[e].draw(camera_pos, up_vector)
                
                # if it just finished, turn it all off
                if self.explosions[e].active == False:
                    self.active[e] = False
                    self.total_active -= 1
                    self.last_active = e
                    
    def new_explosion(self, position=Vector3(0,0,0), color=(1.0,0.0,0.0), density=10, life=1.0, fade=0.05, size=100): 
        if self.rate_limit:
            t = time.time()
            if t - self.last_time < .3:
                return
            else:
                self.last_time = t
        if self.total_active >= self._MAX_EXPLOSIONS:
            return

        # Find an open explosion, and reset it
        for e in range(self._MAX_EXPLOSIONS):
            if self.active[e] == False:
                self.last_active = e
                self.total_active += 1
                self.active[e] = True
                self.explosions[e].reset(position=position, color=color, density=density, life=life, fade=fade, size=size)
                return
                
class Puffs(object):
    """
    The list of puffs defined by MAX_PUFFS
    that allows us to create a certain amount and not
    blahblahbreak the renderer.
    """
    def __init__(self, max_puffs, rate_limit=False):
        self.rate_limit = rate_limit
        self._MAX_PUFFS = max_puffs
        self._MAX_PARTICLES = 10
        self.puffs = []
        self.active = []
        self.last_active = 0
        self.total_active = 0
        self.last_time = time.time()
        # Initialize our list of explosions
        for e in range(self._MAX_PUFFS):
            self.puffs.append(Puff(position=Vector3(0,0,0), color=(1.0,1.0,1.0), density=self._MAX_PARTICLES, life=1.0, fade=0.00, size=1))
            self.active.append(False)
    
    def draw(self, camera_pos, up_vector):
        for e in range(self._MAX_PUFFS):
            # if explosion is on
            if self.active[e] == True:                
                self.puffs[e].draw(camera_pos, up_vector)
                
                # if it just finished, turn it all off
                if self.puffs[e].active == False:
                    self.active[e] = False
                    self.total_active -= 1
                    self.last_active = e
                    
    def new_puff(self, position=Vector3(0,0,0), color=(1.0,0.0,0.0), density=10, life=1.0, fade=0.05, size=100, fire_vector=Vector3(0.0,0.0,1.0), right_vector=(1.0,0.0,0.0)): 
        if self.rate_limit:
            t = time.time()
            if t - self.last_time < .3:
                return
            else:
                self.last_time = t
        if self.total_active >= self._MAX_PUFFS:
            return

        # Find an open explosion, and reset it
        for e in range(self._MAX_PUFFS):
            if self.active[e] == False:
                self.last_active = e
                self.total_active += 1
                self.active[e] = True
                self.puffs[e].reset(position=position, color=color, density=density, life=life, fade=fade, size=size, fire_vector=fire_vector, right_vector=right_vector)
                return
