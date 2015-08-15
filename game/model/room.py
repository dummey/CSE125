import time, random, copy, pyglet, euclid
from game.model.player import Player
from game.model.weapons import Laser, Lasers, Grappler
from game.resources import elements, spawn, wall
from game.utils import itersubclasses
import game
from game.graphics.particles import Explosions, Laser_Glow, H_Well, Puffs
from game.graphics import shapes
from time import time
class Room(object):
    dimensions = (1024, 1024, 1024)
    elements = (
        # (Element, **kwargs),
    )
    # last_time = 0

    def __init__(self):
        """Take the list of elements in a room, and initialize them, assigning
        unique ids for reference during unpacking.
        """

        # used by both
        self.instances = {}
        self.classes = {}
        self.players = {}
        self.balistics = {}
        self._spawn_init = False
        self._next_id = 0
        self._add_cache, self._remove_cache, self._persistent_cache = {}, [], {}

        self._load_room_elements(initial = True)
        
    def reset_room(self, delay = None):
        print "resetting room", delay
        if delay is None:
            self._reset_all_elements()
        else:
            game.manager.unschedule(self._reset_all_elements)
            game.manager.schedule(self._reset_all_elements, delay)
            
    def _reset_all_elements(self, dt = None):
        pyglet.clock.unschedule(self._reset_all_elements)
        print "resetting all elements"
        self._unload_room_elements()
        self._load_room_elements()
        
    def _load_room_elements(self, dt = None, initial = False): 
        
        self.explosions = Explosions(10)
        self.puffs = Puffs(10)
        self.last_t = time()
        self.lasers = Lasers()
        self.h_well = H_Well(position=(1.0,1.0,1.0), color=(0.0,1.0,0.0), density=100, life=1.0, fade=0.02, size=40)
        self.h_well_r1 = H_Well(position=(180,-100,-160), color=(0.0,1.0,0.0), density=100, life=1.0, fade=0.02, size=40)
        self.h_well_b1 = H_Well(position=(-180,100,160), color=(0.0,1.0,0.0), density=100, life=1.0, fade=0.02, size=40)
        self.laser_helix = Laser_Glow()
        self.rLaser = shapes.Laser(self.dimensions.x, 20)
        
        #initial loading causes all objects to be populated
        if initial: 
            for element, kwargs in self.elements:
                self.add_instance(element, **kwargs)
    
            for spawn, kwargs in self.spawn_points:
                self.add_instance(spawn, **kwargs)
        else:
            #only objects that are alterable will be loaded
            for element, kwargs in self.elements:
                if element.alterable:
                    self.add_instance(element, **kwargs)
    
            for spawn, kwargs in self.spawn_points:
                if spawn.alterable:
                    self.add_instance(spawn, **kwargs)
            
        # self.laser_helix = Laser_Glow()

    def _unload_room_elements(self):
        #clear manager's knowledge of the gates
        for team in game.manager.teams.teams.values():
            team.gates = []
        
        for id in self.instances.keys():
            if isinstance(self.instances[id], Player) is True:
                self.instances[id].health = 0
            else:
                if self.instances[id].alterable is True:
                    self.remove_instance(id)

    def _assign_id(self):

        # used by server, will be out of sync on clients

        # can't pickle generator objects
        id = self._next_id
        self._next_id += 1
        return id

    def add_instance(self, element, id=None, **kwargs):
        # used by server without id argument, by client with
        e = element(**kwargs)
        e.id = self._assign_id() if id is None else id
        copy_instance = copy.copy(self.instances)
        copy_instance[e.id] = e
        self.instances = copy_instance
        self.classes.setdefault(element, {}).update({e.id: e})
        self._add_cache[e.id] = (element.__name__, kwargs)
        self._persistent_cache[e.id] = (element.__name__, kwargs)
        # print e.id, e.forward, e.up
        return e

    def add_player(self, client_id, **kwargs):
        # used by server
        p = self.add_instance(Player, **kwargs)
        self.players[client_id] = p
        return p

    def remove_instance(self, id):
        # used by both
        if self.instances.has_key(id):
            copy_instance = copy.copy(self.instances)
            e = copy_instance.pop(id)
            self.instances = copy_instance
            self.classes[e.__class__].pop(e.id)
            self._remove_cache.append(id)
            self._persistent_cache.pop(e.id)

    def update(self, dt):
        # used by server
        self.collision_detection()

        if self._spawn_init == False:
            self.init_spawns(dt)

        for element in self.instances.itervalues():
            element.update(dt)

    def init_spawns(self, dt):
        self._spawn_init = True
        
        tmp_intances = copy.copy(self.instances)
        for element in tmp_intances.itervalues():
            element.update(dt)
        self.instances.update(tmp_intances)

    def collision_detection(self):

        #this does laser collision checks
        for p in self.class_set(game.model.player.Player):
            if p.laser_fire and not p.maxed_laser:
                laser_position = p.position + 10*p.forward.normalized()
                length, obj_hit = Laser.precalc(laser_position, p.forward, [p])
                if isinstance(obj_hit, Player) or isinstance(obj_hit, spawn.SpawnTarget):
                    game.manager.laser(position=laser_position,
                                   forward=p.forward,
                                   up=p.up,
                                   length=length,
                                   shot_by=p.id,
                                   hits=obj_hit.id)
                else:
                    game.manager.laser(position=laser_position,
                                   forward=p.forward,
                                   up=p.up,
                                   length=length,
                                   shot_by=p.id,
                                   hits=None)
                                        
                if obj_hit:
                    game.manager.explosion(p.position + (length*p.forward))
                    obj_hit.hit_by_laser(p)

        # destructionList = []
        for moveable in self.class_set(game.model.components.Movement):
            # death = False
            for element in self.instances.itervalues():
                # vel_mag = moveable.velocity.magnitude()
                # box_mag = max( (moveable.aabb.p0.magnitude(), moveable.aabb.p1.magnitude()))
                # if vel_mag  > box_mag:
                #     num_iters = int(vel_mag / box_mag )
                #     # original_pos 
                #     for i in range(num_iters):
                #         calc_mag = (vel_mag / num_iters) * i
                #         
                #         pass
                
                collision_result = moveable.collision_check(element)
                # if collision_result == "boom":
                #     print "inflating the box"
                #     moveable.aabb.inflate_box(30)
                #     for el in self.instances.itervalues():
                #         collision_result = moveable.collision_check(el)
                #     destructionList.append((moveable, True))
                #     break
                # elif collision_result == "no boom":
                #     death = True
                if collision_result is not False:
                    game.manager.puff(position=moveable.position,
                                    fire_vector=collision_result,
                                    up_vector=moveable.up)
            # if death == True:
            #     destructionList.append((moveable, False))


        # for rocket, explode in destructionList:
        #     if explode:
        #         game.manager.explosion(rocket.position)
        #     self.remove_instance(rocket.id)

        # for player in self.players.itervalues():
        #     for element in self.instances.itervalues():
        #         player.collision_check(element)


    def collides_with_players(self, obj):
        collisions = []
        for player in self.players.itervalues():
            if player.collision_check(obj):
                collisions.append(player)
        return collisions

    def pack(self):

        # used by server
        data = {}
        for id in self.instances:
            d = self.instances[id].pack()
            if id not in self._add_cache and d is not None:
                data[id] = d
        data["add_cache"] = self._add_cache
        data["remove_cache"] = self._remove_cache
        self._add_cache = {}
        self._remove_cache = []
        return data

    def unpack(self, data):

        # used by client
        add_data = data.pop("add_cache", {})
        remove_data = data.pop("remove_cache", [])
        for id, e_data in data.iteritems():
            e = self.instances.get(id)
            if e is not None:
                e.unpack(e_data)
        self.unpack_add(add_data)
        self.unpack_remove(remove_data)

    def unpack_add(self, data):

        # used by client for add and persistent cache
        for id, (klass, e_data) in data.iteritems():
            if id not in self.instances:
                #check both elements and spawn
                try:
                    self.add_instance(getattr(elements, klass), id=id, **e_data)
                except:
                    self.add_instance(getattr(spawn, klass), id=id, **e_data)

    def unpack_remove(self, data):

        # used by client
        for id in data:
            self.remove_instance(id)

    def render(self):

        # used by client
        for element in self.instances.itervalues():
            element.render()
        if game.manager.camera is not None:
            # print "here1"
            cam = game.manager.camera

            self.h_well.draw(cam.position, cam.up)
            self.h_well_r1.draw(cam.position, cam.up)
            self.h_well_b1.draw(cam.position, cam.up)
            self.explosions.draw(cam.position, cam.up)
            self.puffs.draw(cam.position, cam.up)
        else:
            print("not drawing")
        # print self.laser_helix
        self.lasers.render()

    def _class_set(self, cls):
        result = []
        try:
            for id in self.classes.get(cls, []):
                result.append(self.instances[id])
        except:
            pass
        return result

    def class_set(self, cls):
        result = []
        result.extend(self._class_set(cls))
        for subclass in itersubclasses(cls):
            result.extend(self._class_set(subclass))
        return result
