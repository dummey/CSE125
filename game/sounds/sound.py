import pyglet
import game
import os
from time import time
from threading import Thread

class Sound(object):

    def __init__(self):
        # self.player = pyglet.media.Player()
        self.boom = pyglet.media.load('../sounds/boom.wav',streaming=False)
        self.ohno = pyglet.media.load('../sounds/ohno.wav',streaming=False)
        self.knock = pyglet.media.load('../sounds/knock.wav',streaming=False)
        self.recent = "default"
        self.last_time = time()
        self.player = pyglet.media.Player()
        
        #self.music()
        
        
    def music(self):
        background_player = pyglet.media.Player()
        get_music = False
        
        if os.path.exists('../sounds/hollywood.wav'):
            music1 = pyglet.media.load('../sounds/hollywood.wav',streaming=False)
            background_player.queue(music1)
        if os.path.exists('../sounds/myohmy.wav'):
            music2 = pyglet.media.load('../sounds/myohmy.wav',streaming=False)
            background_player.queue(music2)        
        if os.path.exists('../sounds/fluffy.wav'):
            music3 = pyglet.media.load('../sounds/fluffy.wav',streaming=False) 
            background_player.queue(music3)
        else:
            get_music = True
            t = Thread(target=game.network.utils.download_files)
            t.start()
            
        # # music = pyglet.resource.media('ohno.wav',streaming=False)
        # music1 = pyglet.media.load('../sounds/hollywood.wav',streaming=False)
        # music2 = pyglet.media.load('../sounds/myohmy.wav',streaming=False)
        # music3 = pyglet.media.load('../sounds/fluffy.wav',streaming=False)
        # music1.play()
        # background_player = pyglet.media.Player()
        # background_player.queue(music)
        
        if not get_music:
            background_player.volume = 0.3
            background_player.play()

        
    def play_sound(self, sound_type, position):
        t = time()
        if t - self.last_time < .3:
            return
        else:
            self.last_time = t
        player = pyglet.media.Player()
        player.position = (position[0]/100,position[1]/100,position[2]/100)
        if( sound_type == "explosion" ):
            player.queue(self.boom)
        elif( sound_type == "knock"):
            player.queue(self.knock)
        else:
            player.queue(self.ohno)

        player.play()
