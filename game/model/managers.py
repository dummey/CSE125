import pyglet, sys, copy, random, time
from threading import Semaphore
from euclid import Vector3
from game.resources.rooms import default_room
from game.model.player import Camera, Player
from game.model.weapons import Laser
from game.settings import *
from game.network.server import Server as NetServer
from game.network.client import Client as NetClient
from game.graphics.hud import Hud
from game.sounds.sound import Sound
from game.graphics.utils import setup_opengl, begin_draw
from pyglet.gl import *
from pyglet.window import key
from game.graphics.shapes import Cube
from game.resources.elements import *
import time
import game

class Team(object):
    gates = []
    
    def __init__(self, team_name, rgb):
        self.team_name = team_name
        self.rgb = rgb
        self.num_players = 0
        self.gates = []
    
    def __str__(self):
        return "{0} team".format(self.team_name)
    __repr__ = __str__

    def still_has_gates(self):
        alive_gates = 0
        if len(self.gates) > 0:
            for gate in self.gates:
                if gate.spawnable is True:
                    alive_gates += 1
            return True if alive_gates > 0 else False
        else:
            return True

class Teams(object):
    num_teams = 2
    teams = {}

    def __init__(self):
        self.teams["RED"] = Team("RED", (0.5, 0, 0))
        self.teams["BLUE"] = Team("BLUE", (0, 0, 0.5))

    def least_players(self):
        least_num_players = 100
        least_num_team = None
        for team in self.teams.values():
            if team.num_players <= least_num_players:
                least_num_players = team.num_players
                least_num_team = team

        return least_num_team

    def dead_teams(self):
        dead_teams = []
        for team in self.teams.values():
            if team.still_has_gates() is False:
                dead_teams.append(team)
        return dead_teams

class Manager(object):
    is_server = False
    network = None
    room = None
    teams = None
    game_state = None
    schedule_dict = None
    sched_sem = None

    def __init__(self):
        game.manager = self
        self.room = default_room()
        self.schedule_dict = {}
        self.sched_sem = Semaphore(1)
        self.loading = True
        self.very_first = True

    def update(self, dt):
        raise NotImplementedError

    def schedule(self, func, seconds):
        self.sched_sem.acquire()

        self.schedule_dict[func] = time.time() + seconds

        self.sched_sem.release()

    def unschedule(self, func):
        self.sched_sem.acquire()

        if func in self.schedule_dict:
            del self.schedule_dict[func]

        self.sched_sem.release()

    def get_scheduled_tasks(self):
        self.sched_sem.acquire()
        to_return = []
        current_time = time.time()
        for func, t in self.schedule_dict.items():
            if t < current_time:
                to_return.append(func)

        for func in to_return:
            if func in self.schedule_dict:
                del self.schedule_dict[func]

        self.sched_sem.release()
        return to_return

    def cleanup(self):
        self.network.shutdown()

class Server(Manager):
    is_server = True

    def __init__(self, port=8000, run_local=False):
        super(Server, self).__init__()

        self.teams = Teams()
        self.game_state = "game_running"

        self.network = NetServer(port, run_local=run_local, callbacks={
            "new_client":   self.register_client,
            "keypress":     self.handle_event,
            "keyrelease":   self.handle_event,
            "mousepress":   self.handle_event,
            "mouserelease": self.handle_event,
            "orientation":  self.handle_event
        })
        self.buffer = []
        self.last_explosion = time.time()
        self.last_laser = time.time()
        self.last_puff = time.time()
        pyglet.clock.schedule_interval(self.update, 1.0 / GAME_SPEED)
        pyglet.app.run()

    # callbacks
    def register_client(self, client_id, tag, data):
        print "server registered client with id %s" % client_id

        # client has already connected and has a client_id

        # add new player object
        pos = Vector3(0,100,100)
        fwd = Vector3(0,0,-1)
        vel = Vector3(0,0,0)

        player_team=self.teams.least_players()
        spawn_point = Player._determine_spawn(player_team)
        player_team.num_players += 1

        newRoom = copy.copy(self.room)
        newRoom.elements = copy.copy(self.room.elements)
        newRoom.classes = copy.copy(self.room.classes)
        newRoom.instances = copy.copy(self.room.instances)
        newRoom.players = copy.copy(self.room.players)
        newRoom.balistics = copy.copy(self.room.balistics)

        new_player = newRoom.add_player(client_id, team=player_team, name="", pos = spawn_point.position + spawn_point.forward * 5, forward = spawn_point.forward)

        self.room = newRoom

        # send "welcome package" to client
        self.network.sendUpdate(client_id, "player_init", {
            "persistent_cache": self.room._persistent_cache,
            "player_room_id": new_player.id

        })
        data = {}
        data["game_state"] = "game_start"
        self.network.broadcastUpdate("game_event", data)

    def handle_event(self, client_id, tag, data):
        self.buffer.append((tag, client_id, data))

    # main update loop
    def update(self, dt):
        """Update the current room, then send the data to all the clients."""

        # for puffs for weird collissions
        # passing
        
        functions = self.get_scheduled_tasks()
        for func in functions:
            func()

        #manage game state
        dead_teams = self.teams.dead_teams()     
        if len(dead_teams) > 0:
            self.change_game_state("game_over", dead_teams)
        else:
            if self.game_state == "game_over":
                self.change_game_state("game_start")
            elif self.game_state == "game_start":
                self.change_game_state("game_running")

        # flush buffer, run updates
        current_buffer = self.buffer
        self.buffer = []

        for update in current_buffer:
            kind, client_id, data = update
            if client_id in self.room.players:
                p = self.room.players[client_id]

                if kind in ["keypress", "keyrelease", "orientation"]:
                    # Hey, don't like how this is written?
                    # then /you/ figure out how to add instances to the room
                    # from within player!
                    if kind == "keypress" and data == key.Z and ROCKETS:
                        pos = p.position + (p.forward * 5)
                        vel = p.velocity + (p.forward * 5)
                        r = self.room.add_instance(Rocket,
                                               position=pos,
                                               forward=p.forward,
                                               velocity=vel)
                    p.handle_keypress(kind, data)
                if kind in ["mousepress", "mouserelease"]:
                    p.handle_mouse(kind, data)
            else:
                print "client with id %s is not in our player list yet"%client_id

        # recursively update room and do collision detection
        self.room.update(dt)

        # send out updates
        # print self.room.pack()
        self.network.broadcastUpdate("packed_room", self.room.pack())

    def explosion(self, position):
        t = time.time()
        if t - self.last_explosion < .3:
            return
        else:
            self.last_explosion = t
        data = {"pos":position}
        self.network.broadcastUpdate("explosion", data)

    def puff(self, position, fire_vector, up_vector):
        t = time.time()
        if t - self.last_puff < .5:
            return
        else:
            self.last_puff = t
        # self.sound(position, "knock")
        data = {"pos":position,"fire":fire_vector,"up":up_vector}
        self.network.broadcastUpdate("puff", data)
        

    def laser(self, **kwargs):
        t = time.time()
        if t - self.last_laser < .3:
            return
        else:
            self.last_laser = t

        self.network.broadcastUpdate("laser", kwargs)

    def sound(self, position, sound_name):

        print "hey, we aren't using the sound broadcasts anymore"
        pass
        # data = {}
        # data["sound_source"] = position
        # data["sound_type"]= "explosion"
        # self.network.broadcastUpdate("sound_play", data)


    #Game States: game_running, game_over
    def change_game_state(self, state, team = None): 
        if self.game_state is not state:
            #hand state change
            if state == "game_over":
                self.room.reset_room(delay = 1)
            
            #send data to client
            self.game_state = state
            data = {}
            data["game_state"] = state
            data["team"] = team
            self.network.broadcastUpdate("game_event", data)


class Client(Manager):
    camera = None
    hud = None
    graphics_cache = {}
    initialized = False
    game_state_messages = []
    player_state_alive = False
    player_state_hit = 0
    hits = []

    def __init__(self, **kwargs):
        super(Client, self).__init__()
        self.listener = pyglet.media.listener

        # create window
        try:
            # try and create a window with multisampling (antialiasing)
            config = Config(sample_buffers=1, samples=4,
                depth_size=16, double_buffer=True)
            self.window = pyglet.window.Window(resizable=True, config=config,
                width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        except pyglet.window.NoSuchConfigException:
            # fall back to no multisampling for old hardware
            print "window configuration failed"
            self.window = pyglet.window.Window(resizable=True,
                width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

        # register window events
        self.window.set_exclusive_mouse(True)
        self.on_draw = self.window.event(self.on_draw)
        self.on_key_press = self.window.event(self.on_key_press)
        self.on_key_release = self.window.event(self.on_key_release)
        self.on_mouse_press = self.window.event(self.on_mouse_press)
        self.on_mouse_release = self.window.event(self.on_mouse_release)
        self.on_resize = self.window.event(self.on_resize)
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keyboard)

        # init graphics
        setup_opengl()

        # init misc?
        if self.hud is None:
            self.hud = Hud()
        #if self.sound is None:
        self.sound = Sound()

        # self.fps = FPSDisplay()
        # self.room.elements.append(self.fps)
        # self.fps_display = pyglet.clock.ClockDisplay() # see programming guide pg 48

        # network must be last to avoid race condition with the initialization callback
        self.network = NetClient(callbacks={
            "player_init": self.init_callback,
            "packed_room": self.packed_room_callback,
            "sound_play": self.sound_play_callback,
            "explosion": self.explosion_callback,
            "laser": self.laser_callback,
            "puff" : self.puff_callback,
            "game_event": self.game_event
        }, **kwargs)

        # start game
        pyglet.clock.set_fps_limit(60)
        pyglet.clock.schedule(self.update)
        pyglet.app.run()

    # callbacks
    def init_callback(self, tag, data):
        cache = data["persistent_cache"]
        player_room_id = data["player_room_id"]

        # if room is not default_room, initialize it here

        # first, switch this client's player object to a camera object
        cache[player_room_id] = (Camera.__name__, cache[player_room_id][1])

        # unpack persistent cache and set camera
        self.room.unpack_add(data["persistent_cache"])
        self.camera = self.room.instances[player_room_id]
        self.camera.on_mouse_motion = self.window.event(self.camera.on_mouse_motion)
        self.camera.on_mouse_drag = self.window.event(self.camera.on_mouse_drag)

        self.last_pposition = Vector3(0.0,0.0,0.0)

        # start game
        self.initialized = True

    def packed_room_callback(self, tag, data):
        newRoom = copy.copy(self.room)
        newRoom.elements = copy.copy(self.room.elements)
        newRoom.classes = copy.copy(self.room.classes)
        newRoom.instances = copy.copy(self.room.instances)
        newRoom.players = copy.copy(self.room.players)
        newRoom.balistics = copy.copy(self.room.balistics)
        newRoom.unpack(data)
        self.room=newRoom

    def sound_play_callback(self, tag, data):
        sound_source = data["sound_source"]
        sound_type = data["sound_type"]
        self.sound.play_sound(sound_type,sound_source)

    def explosion_callback(self, tag, data):
        data["sound_source"] = data["pos"]
        data["sound_type"] = "explosion"
        self.sound_play_callback("sound", data)
        self.room.explosions.new_explosion(data["pos"])

    def laser_callback(self, tag, data):
        # print "laser_callback: %s" % data
        
        if "hits" in data:
            if data["hits"] is not None and data["hits"] != self.camera.id:
                self.hits.append(data["hits"])
            del data["hits"]
            
        data["shot_team"] = self.room.instances[data["shot_by"]].team.team_name
        self.room.lasers.add_laser(**data)
    
    def puff_callback(self, tag, data):
        color = (1.0,0.0,0.0) if (self.camera.team.team_name is not None and self.camera.team.team_name == "RED") else (0.0,0.0,1.0)
        if data["pos"] == self.last_pposition:
            pass
        else:
            self.last_pposition = data["pos"]
            self.room.puffs.new_puff(data["pos"], color=color, fire_vector=data["fire"], right_vector=data["up"])
            data["sound_source"] = data["pos"]
            data["sound_type"] = "knock"
            self.sound_play_callback("sound",data)
    
    def game_event(self, tag, data):
        self.game_state = data["game_state"]
        if data["game_state"] == "game_start":
            team_message = "You have joined team " + self.camera.team.team_name
            self.game_state_messages.append(team_message)
        if data["game_state"] == "game_over":
            end_message = ("All of " + data["team"][0].team_name + "'s gates have been destroyed.")
            self.game_state_messages.append(end_message)
            
    def player_event(self, data):
        pass

    # window events
    def on_key_press(self, symbol, modifiers):
        # self.camera.check_orientation_keys(symbol)
        if symbol == key.ESCAPE:
            #sys.exit()
            pass
        else:
            self.network.send("keypress", symbol)

    def on_key_release(self, symbol, modifiers):
        self.network.send("keyrelease", symbol)

    def on_mouse_press(self, x, y, button, modifiers):
        self.network.send("mousepress", button)

    def on_mouse_release(self, x, y, button, modifiers):
        self.network.send("mouserelease", button)
    
    def on_resize(self, width, height):
        self.hud.window_resize(width, height)
    
    # main update loop
    def update(self, dt):
        if self.initialized:
            # print self.camera.hit_by
            self.player_state_hit = 0
            if (self.camera.health < self.camera.last_health):
                try:
                    attacker = self.room.instances[self.camera.hit_by].position
                except:
                    attacker = Vector3(0.0,0.0,0.0)
                attack_vector = (attacker - self.camera.position).normalize()
                attack_angle = self.camera.forward.angle(attack_vector)
                
                if attack_angle >= 2.0:
                    self.player_state_hit = 4
                elif attack_angle >= 1.0:
                    self.player_state_hit = 2 if (self.camera.right.angle(attack_vector) < 1.5) else 3
                else:
                    self.player_state_hit = 1
            
            if self.camera.dead is True and self.player_state_alive is True:
                self.player_state_alive = False
                self.game_state_messages.append("You have died, respawning.")
            elif self.camera.dead is False and self.player_state_alive is False:
                self.player_state_alive = True
                
            functions = self.get_scheduled_tasks()
            for func in functions:
                func()

            self.camera.check_orientation_keys(self.keyboard)
            if self.camera.mod:
                self.network.send("orientation", {
                    "forward": self.camera.forward,
                    "up":      self.camera.up
                })
                self.camera.mod = False
            self.hud.update(self.camera)
            pos = self.camera.position
            self.listener.position = (pos[0]/100,pos[1]/100,pos[2]/100)
            self.listener.up_orientation = self.camera.up
            self.listener.forward_orientation = self.camera.forward


    def on_draw(self):
        # if self.very_first:
        #     load_img = pyglet.image.load('../images/loadingpage.png')#loadingpage.png')
        #     load_img.anchor_x = load_img.width / 2
        #     load_img.anchor_y = load_img.height / 2
        #     self.arg = pyglet.sprite.Sprite(load_img, x = 300, y = 250)
        #     self.arg.draw()
        #     self.very_first = False
        #     
        # elif self.loading:    
        #     time.sleep(5)
        #     self.loading = False
            
        if self.initialized:
            begin_draw()
            self.camera.place_camera()
            self.room.render()
            self.hud.draw()

