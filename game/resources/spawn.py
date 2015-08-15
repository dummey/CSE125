from euclid import Point3, Vector3, Matrix4
import game.model.collision as collision
from game.model import components
from game.graphics import shapes
from game import settings
import game

class ColorObject(components.Position):
    def __init__(self, *args, **kwargs):
        if "color" in kwargs:
            self.color = kwargs["color"]
            del kwargs["color"]
        else:
            self.color = (0.5, 0.5, 0.5)
        super(ColorObject, self).__init__(*args, **kwargs)
        
class SpawnPoint(ColorObject):
    
    fields = ["spawnable"]
    alterable = True
    
    def __init__(self, team=None, **kwargs):
        super(SpawnPoint, self).__init__(**kwargs)
        x = y = z = 10
        self.oobb = collision.BoundingBox(-x, x, -y, y, -z, z)
        self.aabb = self.oobb.transformed(self.forward, self.up)
        self.team = team
        self.spawnable = True
        self.alive = True
    
    def __str__(self):
        return "{0} spawn point {1}".format("neutral" if self.is_neutral() else self.team, id(self))
    __repr__ = __str__
    
    def can_spawn(self):
        return self.spawnable

    def is_neutral(self):
        return self.team is None

    def for_team(self, team, team_name = None):
        if team_name is not None:
            return self.team == team_name
        else:
            return self.is_neutral() or self.team == team.team_name

class SpawnTarget(components.Position):
    
    fields = ["health"]
    
    alterable = True
    
    def __init__(self, gate, position, forward, up, color):
        self.gate = gate
        self.health = 100
        self.side = 5
        super(SpawnTarget, self).__init__(position, forward, up)
        self.color = color
        self.oobb = collision.BoundingBox(-self.side/2, self.side/2, -self.side/2, self.side/2, -self.side/2, self.side/2)
        self.aabb = self.oobb.transformed(self.forward, self.up)
    
    def hit_by_laser(self, player):
        self.health -= 5
    
    def render(self):
        shape = shapes.Block.get(self.side, self.side, self.side, 1, 1, 1)
        if self.health > 1:
            tmp_color = Vector3(0,0,0)
            tmp_color.x = self.color.x * (self.health / 100.0)
            tmp_color.y = self.color.y * (self.health / 100.0)
            tmp_color.z = self.color.z * (self.health / 100.0)
            shape.draw(self.position, self.forward, color=tmp_color)
        else:
            shape.draw(self.position, self.forward, color=Vector3(1,1,1))
                
        if settings.DISPLAY_BBOXES:
            bbox = shapes.BBox.get(self.aabb)
            bbox.draw(self.position)

class SpawnGate(SpawnPoint):
    
    fields = ["down_gates"]
    alterable = True
    
    def __init__(self, **kwargs):
        super(SpawnGate, self).__init__(**kwargs)
        self.health = 100
        self.radius = 5
        self.inner_radius = 0.5
        self.slices = 5
        self.inner_slices = 8
        x = y = self.radius + self.inner_radius
        z = self.inner_radius
        self.oobb = collision.BoundingBox(-x, x, -y, y, -z, z)
        self.aabb = self.oobb.transformed(self.forward, self.up)
        
        self.target_points = None
        self.down_gates = 0
        
    def update(self, dt):
        if self.target_points is None:
            self.target_points = []
            target = game.manager.room.add_instance(SpawnTarget, gate = self, position = self.position + Vector3(10,0,0), forward = self.forward, up = self.up, color=self.color)
            self.target_points.append(target)
            target = game.manager.room.add_instance(SpawnTarget, gate = self, position = self.position + Vector3(-10,0,0), forward = self.forward, up = self.up, color=self.color)
            self.target_points.append(target)
            target = game.manager.room.add_instance(SpawnTarget, gate = self, position = self.position + Vector3(0,10,0), forward = self.forward, up = self.up, color=self.color)
            self.target_points.append(target)
            target = game.manager.room.add_instance(SpawnTarget, gate = self, position = self.position + Vector3(0,-10,0), forward = self.forward, up = self.up, color=self.color)
            self.target_points.append(target)
            
            #let team know that a gate of it's team exists
            game.manager.teams.teams[self.team].gates.append(self)
            
        self.down_gates = self._num_downed_gates()
        if self.down_gates == len(self.target_points):
            self.spawnable = False
        
    def _num_downed_gates(self):
        downed_targets = 0
        if self.target_points:
            for target in self.target_points:
                if target.health < 1:
                    downed_targets += 1
        return downed_targets

    def render(self):
        shape = shapes.Torus.get(self.radius,
                                 self.inner_radius,
                                 self.slices,
                                 self.inner_slices)
        if self.down_gates < 4:
            shape.draw(self.position, self.forward, color=self.color)
        else:
            shape.draw(self.position, self.forward, color=Vector3(0,0,0))