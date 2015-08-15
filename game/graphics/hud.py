import pyglet
import utils
import game
import os
from pyglet.gl import *

def load_centered_sprite(filename, x = 0, y = 0):
    img = pyglet.image.load(filename)
    img.anchor_x=img.width / 2
    img.anchor_y=img.height / 2
    ret = pyglet.sprite.Sprite(img, x=x, y=y)
    
    return ret

class Hud(object):

    def __init__(self):
        self.x = game.manager.window.width
        self.y = game.manager.window.height
        self.hudItems = []
        self.hudItems.append(Reticle(self))
        self.hudItems.append(Health(self))
        self.hudItems.append(Weapon(self))
        self.hudItems.append(Player_State(self))
        self.hudItems.append(System_Message(self))
        self.hudItems.append(Notice(self))
        self.hudItems.append(Gate_State(self))
        self.hudItems.append(Hit_Indicator(self))

    def update(self, player):
        for hudItems in self.hudItems:
            hudItems.update(player)
            
    def window_resize(self,width,height):
        self.x = game.manager.window.width
        self.y = game.manager.window.height
        for hudItems in self.hudItems:
            hudItems.window_resize(self.x,self.y)

    def draw(self):
        utils.to_ortho()
        for hudItem in self.hudItems:
            hudItem.draw()
        utils.from_ortho()
        
            
    def flash(self):
        utils.to_ortho()
        
        utils.from_ortho()
    
class Hud_Item(object):

    def __init__(self):
        pass

class Reticle(Hud_Item):

    def __init__(self, parent):
        img = pyglet.image.load('../images/reticle4.png')
        img.anchor_x=img.width / 2
        img.anchor_y=img.height / 2
        self.ret = pyglet.sprite.Sprite(img, x=parent.x/2, y=parent.y/2)
        self.hit_ret = pyglet.sprite.Sprite(img, x=parent.x/2, y=parent.y/2)
        self.hit_ret.scale = 1.3
        self.hitting = False
        #self.ret.color = (255,255,0)

    def update(self, player):
        if len(game.manager.hits) > 0:
            self.hit_display()
            del game.manager.hits[:]

    def hit_display(self):
        game.manager.unschedule(self._turnoff)
        self.hitting = True
        game.manager.schedule(self._turnoff, 1.0/30.0)

    def _turnoff(self, *args):
        self.hitting = False

    def window_resize(self,width,height):
        self.ret.x = width/2
        self.ret.y = height/2
        self.hit_ret.x = width/2
        self.hit_ret.y = height/2
        
    def draw(self):
        if self.hitting:
            self.hit_ret.draw()
        else:
            self.ret.draw()

class Health(Hud_Item):

    def __init__(self, parent):
        #self.label = pyglet.text.Label("Health", anchor_x="center", anchor_y="center", x = 65, y = 22)
        self.health = pyglet.text.Label("100", font_size=24, anchor_x="center", anchor_y="center", x = 65, y = 60)
        self.img0 = pyglet.image.load('../images/bar0.png')
        self.img25 = pyglet.image.load('../images/bar25.png')
        self.img50 = pyglet.image.load('../images/bar50.png')
        self.img75 = pyglet.image.load('../images/bar75.png')
        self.imgfull = pyglet.image.load('../images/barfull.png')
        imgbar = pyglet.image.load('../images/bar.png')
        imgbar.anchor_x=imgbar.width / 2
        imgbar.anchor_y=imgbar.height / 2
        self.healthbar = pyglet.sprite.Sprite(imgbar, x = 65, y = 22)

    def window_resize(self,width,height):
        pass


    def update(self, player):
        hlth = game.manager.camera.health
        self.health = pyglet.text.Label("%s"%int(hlth), font_size=24, anchor_x="center", anchor_y="center", x = 65, y = 60)

        if hlth <= 0:
            img = self.img0
        elif hlth <= 25:
            img = self.img25
        elif hlth <= 50:
            img = self.img50
        elif hlth <= 75:
            img = self.img75
        else:
            img = self.imgfull

        img.anchor_x=img.width / 2
        img.anchor_y=img.height / 2
        self.healthbar = pyglet.sprite.Sprite(img, x = 65, y = 22)


    def draw(self):
        self.health.draw()
        self.healthbar.draw()


class Weapon(Hud_Item):

    def __init__(self, parent):
        self.label_y = 50
        self.bar_y = 20
        self.label = pyglet.text.Label("LAZOR", anchor_x="center", anchor_y="center", x = parent.x - 50, y = self.label_y)
        self.parent = parent

        img = pyglet.image.load('../images/barheat2.png')
        img.anchor_x=img.width / 2
        img.anchor_y=img.height / 2
        self.heatbar = pyglet.sprite.Sprite(img, x = parent.x - 70, y = self.bar_y)

        img2 = pyglet.image.load('../images/barheatfill2.png')
        img2.anchor_x=img.width / 2
        img2.anchor_y=img.height / 2

        self.heatbarfill = pyglet.sprite.Sprite(img2, x = self.parent.x-23, y = self.bar_y)
        # self.pink = pyglet.image.load('../images/barheatfill2.png')
        # self.wid = self.pink.width
        self.halfGlow = pyglet.image.load('../images/barheatfill5.png')
        self.glowBar = pyglet.image.load('../images/barheatfill4.png')
        self.fullheat = pyglet.image.load('../images/barheatfill2.png')
        
        self.barFills = []
        for x in range(100):
            self.barFills.append(self.fullheat.get_region(0,0,x,self.fullheat.height))
        
    def update(self, player):
        # game.manager.camera.laser_mana
        ammo = int(game.manager.camera.laser_mana)
        # self.heatbar.x = self.parent.x-70
        
        if(ammo >= 7):
            new_width = 101 - ammo
            img =self.barFills[(101-ammo)]
            img.anchor_x=0#self.wid #/ 2
            img.anchor_y=img.height / 2

            self.heatbarfill = pyglet.sprite.Sprite(img, x = self.parent.x-(new_width)-23, y=self.bar_y)

        elif(ammo >= 4):
            img = self.halfGlow
            img.anchor_x=img.width / 2
            img.anchor_y=img.height / 2
            self.heatbarfill = pyglet.sprite.Sprite(img, x = self.parent.x-70, y=self.bar_y)
            xVal = 575

        else:
            img = self.glowBar
            img.anchor_x = img.width / 2
            img.anchor_y = img.height / 2
            self.heatbarfill = pyglet.sprite.Sprite(img, x = self.parent.x-70, y = self.bar_y) 
            xVal = 575

    def draw(self):
        self.label.draw()
        self.heatbar.draw()
        self.heatbarfill.draw()

    def window_resize(self,width,height):
        self.parent.x = width
        self.parent.y = height
        self.heatbar.x = width - 70
        self.label.x = width - 50

'''

    def draw(self):
                
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        self.label.draw()
        self.heatbar.draw()
        self.img2.blit(self.parent.x - 20 + int(game.manager.camera.laser_mana), 50, width=100-int(game.manager.camera.laser_mana))
    #    self.heatbarfill.blit(self.parent.x - 20 + int(game.manager.camera.laser_mana), 50, width=100-int(game.manager.camera.laser_mana))

        ammo = int(game.manager.camera.laser_mana)
        if ammo < 8:
            ammo = 8
        subimg = self.img2.get_region(x = 0, y = 0, width = 101 - ammo, height = 40)
        subimg.anchor_y = subimg.height / 2
        subimg.anchor_x = subimg.width
        subimg.blit(self.parent.x - 23, 50, width = 101 - ammo)

'''
class Player_State(Hud_Item):

    def __init__(self, parent):
        img = pyglet.image.load('../images/bluehand.png')
        img.anchor_x=img.width / 2
        img.anchor_y=img.height / 2
        self.grabbing = pyglet.sprite.Sprite(img, x=parent.x/2, y=parent.y/2 - 150)
        img = pyglet.image.load('../images/fist2.png')
        img.anchor_x=img.width / 2
        img.anchor_y=img.height / 2
        self.grabbed = pyglet.sprite.Sprite(img, x=parent.x/2, y=parent.y/2 - 150)
        self.state = None

    def update(self, player):
        if player.state == player.GRABBING:
            if player.velocity.x == 0 and player.velocity.y == 0 and player.velocity.z == 0:
                self.state = self.grabbed
            else:
                self.state = self.grabbing
        elif player.state == player.JUMPING:
            self.state = None
        else:
            self.state = None
    
    def window_resize(self,width,height):
        self.grabbing.x = width / 2
        self.grabbing.y = height / 2  - 150
        self.grabbed.x = width / 2
        self.grabbed.y = height / 2 - 150

    def draw(self):
        if self.state is not None:
            self.state.draw()

class Gate_State(Hud_Item):
    def __init__(self, parent):
        self.width = parent.x
        self.height = parent.y
        self.label = pyglet.text.Label("Gates Remaining", anchor_x="center", anchor_y="center", x = parent.x/2, y = parent.y - 20, font_size = 10)
        self.white_circle = load_centered_sprite("../images/white-circle.png")
        self.red_circles = [self.white_circle]
        self.red_circles.append(load_centered_sprite("../images/red-circle_1.png"))
        self.red_circles.append(load_centered_sprite("../images/red-circle_2.png"))
        self.red_circles.append(load_centered_sprite("../images/red-circle_3.png"))
        self.red_circles.append(load_centered_sprite("../images/red-circle_4.png"))
        self.blue_circles = [self.white_circle]
        self.blue_circles.append(load_centered_sprite("../images/blue-circle_1.png"))
        self.blue_circles.append(load_centered_sprite("../images/blue-circle_2.png"))
        self.blue_circles.append(load_centered_sprite("../images/blue-circle_3.png"))
        self.blue_circles.append(load_centered_sprite("../images/blue-circle_4.png"))
        self.red_gates = []
        self.blue_gates = []
    
    def update(self, player):
        spawn_gates = game.manager.room.class_set(game.resources.spawn.SpawnPoint)
        
        self.blue_gates = []
        self.red_gates = []
        for spawn_gate in spawn_gates:
            if spawn_gate.for_team(None, "RED"):
                self.red_gates.append(spawn_gate)
            elif spawn_gate.for_team(None, "BLUE"): 
                self.blue_gates.append(spawn_gate)
        # self.label.text = "Red Gates: " + str(len(red_gates)) + " | " + "Blue Gates: " + str(len(blue_gates)) 
        # self.label.text = "poop"
    
    def window_resize(self, width, height):
        self.height = height
        self.width = width
        self.label.x = width / 2
        self.label.y = height - 20
    
    def draw(self):
        center_screen = self.width / 2
        self.label.draw()
        #draw blue gates
        blue_offset = 100
        for gate in self.blue_gates:
            num_down = gate.down_gates
            self.blue_circles[4 - num_down].x = center_screen - blue_offset
            self.blue_circles[4 - num_down].y = self.height - 20
            self.blue_circles[4 - num_down].draw()
            blue_offset += 25
        #draw red gates
        red_offset = 100
        for gate in self.red_gates:
            num_down = gate.down_gates
            self.red_circles[4 - num_down].x = center_screen + red_offset
            self.red_circles[4 - num_down].y = self.height - 20
            self.red_circles[4 - num_down].draw()
            red_offset += 25

class Hit_Indicator(Hud_Item):
    def __init__(self, parent):
        self.drawable = False
        self.draw_at = []
        self.drawn_length = []
        self.hit_indicator = load_centered_sprite("../images/hudalert.png")
        self.height = parent.y
        self.width = parent.x
        
    def update(self, player):
        if game.manager.player_state_hit != 0:
            self.draw_at.append(game.manager.player_state_hit)
            self.drawn_length.append(1.0)

    def draw(self):
        delindex = []
        for c in range(len(self.draw_at)):
            self.hit_indicator.opactiy = (self.drawn_length[c] * 255)
            self.drawn_length[c] -= 0.1
            if self.draw_at[c] == 1:
                self.hit_indicator.x = self.width/2
                self.hit_indicator.y = self.height/2 + 100
                self.hit_indicator.rotation = 0
            elif self.draw_at[c] == 2:
                self.hit_indicator.x = self.width/2 + 100
                self.hit_indicator.y = self.height/2 
                self.hit_indicator.rotation = 90
            elif self.draw_at[c] == 3:
                self.hit_indicator.x = self.width/2 - 100
                self.hit_indicator.y = self.height/2 
                self.hit_indicator.rotation = 270
            else:
                self.hit_indicator.x = self.width/2
                self.hit_indicator.y = self.height/2 - 100
                self.hit_indicator.rotation = 180
            self.hit_indicator.draw()
            
            if self.drawn_length[c] <= 0.0:
                delindex.insert(0,c)
        for d in delindex:
            self.draw_at.pop(d)
            self.drawn_length.pop(d)
            
    def window_resize(self, width, height):
        self.height = height
        self.width = width

class Notice(Hud_Item):

    def __init__(self, parent):
        self.drawable = False
        self._last_state = None
        self.label = pyglet.text.Label("Hello", anchor_x="center", anchor_y="center", x = parent.x/2, y = parent.y/2 + 40, font_size = 20, bold = True)
        self.message_queue = []

    def update(self, player):            
        if len(game.manager.game_state_messages) > 0:
            self.message_queue.extend(game.manager.game_state_messages)
            del game.manager.game_state_messages[:]
            
        if self.drawable is False and len(self.message_queue) > 0:
            self.display(self.message_queue.pop())

    def display(self, message, duration = 4):
        game.manager.unschedule(self._turnoff)
        self.label.text = message
        self.drawable = True
        game.manager.schedule(self._turnoff, duration)

    def _turnoff(self, *args):
        self.label.text = ""
        self.drawable = False
        
    def window_resize(self,width,height):
        pass

    def draw(self):
        if self.drawable:
            self.label.draw()

class System_Message(Hud_Item):
    def __init__(self, parent):
        self.parent = parent
        self.fps = pyglet.text.Label("FPS Counter", font_size=10, anchor_x="left", anchor_y="top", x = 20, y = parent.y - 10)
        self.serverfps = pyglet.text.Label("Server FPS Counter", font_size=10, anchor_x="left", anchor_y="top", x = 20, y = parent.y - 25)
        

    def update(self, player):
        self.fps.y = self.parent.y - 10
        self.fps.text = "FPS: %d" % pyglet.clock.get_fps()
        self.serverfps.y = self.parent.y - 25
        self.serverfps.text = "ServerFPS: %3d"% game.manager.network.connection.speed

    def window_resize(self,width,height):
        pass

    def draw(self):
        self.fps.draw()
        self.serverfps.draw()

