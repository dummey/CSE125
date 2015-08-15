from euclid import Vector3, Point3
from game.model.room import Room
from game.resources import elements
from game.resources import wall
from game.resources import spawn

class TestRoom(Room):
    dimensions = Vector3(512, 512, 512)
    # elements = [
    # #blue side (9 blocks)
    #  (elements.CubeTest, {"position": Point3(100,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
    #  (elements.CubeTest, {"position": Point3(0,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
    #  (elements.CubeTest, {"position": Point3(-100,-100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
    #  (elements.CubeTest, {"position": Point3(0,-100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
    #  (elements.CubeTest, {"position": Point3(100,-100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
    #  (elements.CubeTest, {"position": Point3(100,0,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
    #  (elements.CubeTest, {"position": Point3(-100,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
    #  (elements.CubeTest, {"position": Point3(-100,0,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
    #  
    # #blue neutral (16 blocks)
    #  (elements.CubeTest, {"position": Point3(150,150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(50,150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(-50,150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(-150,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(-50,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(50,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(150,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(50,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(-50,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(-150,150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(50,50,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(-50,50,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(-50,-50,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  (elements.CubeTest, {"position": Point3(50,-50,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  
    #  # (elements.CubeTest, {"position": Point3(-150,-50,-100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  # (elements.CubeTest, {"position": Point3(-150,50,-100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  # (elements.CubeTest, {"position": Point3(150,-50,-100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  # (elements.CubeTest, {"position": Point3(150,50,-100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    #  #     
    #  # #neutral (25 blocks)
    #  # (elements.CubeTest, {"position": Point3(100,100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
    #  # (elements.CubeTest, {"position": Point3(-100,-100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
    #  # (elements.CubeTest, {"position": Point3(100,-100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
    #  # (elements.CubeTest, {"position": Point3(-100,100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
    #  # (elements.SphereTest, {"position": Point3(0,0,0), "forward": Vector3(1,0,0), "color":(0,1,0)}),
    #  # 
    #  # (elements.CubeTest, {"position": Point3(0,100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
    #  # (elements.CubeTest, {"position": Point3(0,-100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
    #  # (elements.CubeTest, {"position": Point3(100,0,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
    #  # (elements.CubeTest, {"position": Point3(-100,0,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
    # 
    # #red neutral
    #  (elements.CubeTest, {"position": Point3(150,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(50,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-50,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-150,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-50,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(50,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(150,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(50,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-50,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-150,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-150,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(50,50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-50,50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-50,-50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(50,-50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-150,-50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(-150,50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(150,-50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  (elements.CubeTest, {"position": Point3(150,50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
    #  
    # # #red side
    # #  (elements.CubeTest, {"position": Point3(100,100,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
    # #  (elements.CubeTest, {"position": Point3(-100,-100,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
    # #  (elements.CubeTest, {"position": Point3(100,-100,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
    # #  (elements.CubeTest, {"position": Point3(-100,100,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
    #  
    # #wall
    #  (wall.Wall, {"position": Point3(-250, 0, 0), "forward": Vector3( 1, 0, 0)}), # left
    #  (wall.Wall, {"position": Point3( 250, 0, 0), "forward": Vector3(-1, 0, 0)}), # right
    #  (wall.Wall, {"position": Point3(0, -250, 0), "forward": Vector3(0,  1, 0), "up": Vector3(0, 0, -1)}), # bottom
    #  (wall.Wall, {"position": Point3(0,  250, 0), "forward": Vector3(0, -1, 0), "up": Vector3(0, 0, -1)}), # top
    #  (wall.Wall, {"position": Point3(0, 0, -250), "forward": Vector3(0, 0,  1)}), # front
    #  (wall.Wall, {"position": Point3(0, 0,  250), "forward": Vector3(0, 0, -1)}),  # back
    # ]
    
    elements = [
     (elements.SphereTest, {"position": Point3(200,0,0), "forward": Vector3(1,0,0)}),
     (elements.SphereTest, {"position": Point3(-200,0,0), "forward": Vector3(1,0,0)}),
     (elements.SphereTest, {"position": Point3(0,200,0), "forward": Vector3(1,0,0), "color":(0,0,1)}),
     (elements.SphereTest, {"position": Point3(0,-200,0), "forward": Vector3(1,0,0), "color":(0,1,0)}),
     (elements.CubeTest, {"position": Point3(0,0,200), "forward": Vector3(1,0,0), "color":(1,0,0)}),
     (elements.SphereTest, {"position": Point3(0,0,-200), "forward": Vector3(1,0,0)}),
     (elements.TorusTest, {"position": Point3(-250, 0, 0), "forward": Vector3(1, 0, 0)}),
     (elements.TorusTest, {"position": Point3(250, 0, 0), "forward": Vector3(-1, 0, 0)}),
     (elements.PowerUp, {"position": Point3(0, 0, 0), "forward": Vector3(-1, 0, 0)}),
     (wall.Wall, {"position": Point3(-250, 0, 0), "forward": Vector3( 1, 0, 0)}), # left
     (wall.Wall, {"position": Point3( 250, 0, 0), "forward": Vector3(-1, 0, 0)}), # right
     (wall.Wall, {"position": Point3(0, -250, 0), "forward": Vector3(0,  1, 0), "up": Vector3(0, 0, -1)}), # bottom
     (wall.Wall, {"position": Point3(0,  250, 0), "forward": Vector3(0, -1, 0), "up": Vector3(0, 0, -1)}), # top
     (wall.Wall, {"position": Point3(0, 0, -250), "forward": Vector3(0, 0,  1)}), # front
     (wall.Wall, {"position": Point3(0, 0,  250), "forward": Vector3(0, 0, -1)})  # back
    ]

    spawn_points = [
     (spawn.SpawnPoint, {"position": Point3(0, 0,  50), "forward": Vector3(0, 0, -1)}),
     (spawn.SpawnPoint, {"position": Point3(0, 50,  0), "forward": Vector3(0, 0, -1)}),
     (spawn.SpawnPoint, {"position": Point3(50, 0,  0), "forward": Vector3(0, 0, -1)}),
     (spawn.SpawnPoint, {"position": Point3(0, 0,  -50), "forward": Vector3(0, 0, -1)}),
    ]


class GameRoom(Room):
    dimensions = Vector3(500, 500, 500)
    
    elements = [
    #blue side (9 blocks)
     (elements.CubeTest, {"position": Point3(100,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(0,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,-100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(0,-100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(100,-100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(100,0,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,0,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     
    #blue neutral (16 blocks)
     (elements.CubeTest, {"position": Point3(150,150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(50,150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(-50,150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(-150,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(-50,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(50,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(150,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(50,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(-50,-150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(-150,150,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(50,50,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(-50,50,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(-50,-50,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(50,-50,100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     
     (elements.CubeTest, {"position": Point3(-150,-50,-100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(-150,50,-100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(150,-50,-100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
     (elements.CubeTest, {"position": Point3(150,50,-100), "forward": Vector3(0,0,-1), "color":(0,0.5,0.5)}),
    
     #neutral (25 blocks)
     (elements.CubeTest, {"position": Point3(100,100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     (elements.CubeTest, {"position": Point3(-100,-100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     (elements.CubeTest, {"position": Point3(100,-100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     (elements.CubeTest, {"position": Point3(-100,100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     (elements.PowerUp, {"position": Point3(0,0,0), "forward": Vector3(1,0,0)}),

     (elements.CubeTest, {"position": Point3(0,100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     (elements.CubeTest, {"position": Point3(0,-100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     (elements.CubeTest, {"position": Point3(100,0,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     (elements.CubeTest, {"position": Point3(-100,0,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     
     
     
    #center edge ring 
     (elements.Cliff, {"position": Point3(200, 200, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(-200, 200, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(-200, -200, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(200, -200, 0), "forward": Vector3(0,0,1)}),
     
     (elements.Cliff, {"position": Point3(200, 100, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(-200, 100, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(-200, -100, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(200, -100, 0), "forward": Vector3(0,0,1)}),
     
     (elements.Cliff, {"position": Point3(-200, 0, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(200, 0, 0), "forward": Vector3(0,0,1)}),
     
     (elements.Cliff, {"position": Point3(100, 200, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(-100, 200, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(-100, -200, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(100, -200, 0), "forward": Vector3(0,0,1)}),
     
     (elements.Cliff, {"position": Point3(0, 200, 0), "forward": Vector3(0,0,1)}),
     (elements.Cliff, {"position": Point3(0, -200, 0), "forward": Vector3(0,0,1)}),
    
    #red neutral
     (elements.CubeTest, {"position": Point3(150,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(50,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-50,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-150,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-50,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(50,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(150,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(50,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-50,-150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-150,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-150,150,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(50,50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-50,50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-50,-50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(50,-50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-150,-50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(-150,50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(150,-50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     (elements.CubeTest, {"position": Point3(150,50,-100), "forward": Vector3(0,0,-1), "color":(0.5,0.5,0)}),
     
    #red side
     (elements.CubeTest, {"position": Point3(100,100,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(-100,-100,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(100,-100,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(-100,100,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     
    #wall
     (wall.Wall, {"position": Point3(-250, 0, 0), "forward": Vector3( 1, 0, 0)}), # left
     (wall.Wall, {"position": Point3( 250, 0, 0), "forward": Vector3(-1, 0, 0)}), # right
     (wall.Wall, {"position": Point3(0, -250, 0), "forward": Vector3(0,  1, 0), "up": Vector3(0, 0, -1)}), # bottom
     (wall.Wall, {"position": Point3(0,  250, 0), "forward": Vector3(0, -1, 0), "up": Vector3(0, 0, -1)}), # top
     (wall.Wall, {"position": Point3(0, 0, -250), "forward": Vector3(0, 0,  1)}), # front
     (wall.Wall, {"position": Point3(0, 0,  250), "forward": Vector3(0, 0, -1)}),  # back
    ]
    
    spawn_points = [
    #red spawn
     # (spawn.SpawnGate, {"position": Point3(100, 100,  -249), "forward": Vector3(0, 0, 1), "color": Vector3(1,0,0), "team": "RED"}),
     # (spawn.SpawnGate, {"position": Point3(-100, -100,  -249), "forward": Vector3(0, 0, 1), "color": Vector3(1,0,0), "team": "RED"}),
     # (spawn.SpawnGate, {"position": Point3(100, -100,  -249), "forward": Vector3(0, 0, 1), "color": Vector3(1,0,0), "team": "RED"}),
     (spawn.SpawnGate, {"position": Point3(-100, 100,  -249), "forward": Vector3(0, 0, 1), "color": Vector3(1,0,0), "team": "RED"}),
     
    #blue spawn
     # (spawn.SpawnGate, {"position": Point3(100, 100,  249), "forward": Vector3(0, 0, -1), "color": Vector3(0,0,1), "team": "BLUE"}),
     # (spawn.SpawnGate, {"position": Point3(-100, -100,  249), "forward": Vector3(0, 0, -1), "color": Vector3(0,0,1), "team": "BLUE"}),
     # (spawn.SpawnGate, {"position": Point3(100, -100,  249), "forward": Vector3(0, 0, -1), "color": Vector3(0,0,1), "team": "BLUE"}),
     (spawn.SpawnGate, {"position": Point3(-100, 100,  249), "forward": Vector3(0, 0, -1), "color": Vector3(0,0,1), "team": "BLUE"})
    ]

class RRoom(Room):
    dimensions = Vector3(500, 500, 500)

    elements = [
    #blue side (9 blocks)
     (elements.CubeTest, {"position": Point3(100,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(0,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,-100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(0,-100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(100,-100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(100,0,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,0,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     
    #blue transition blocks
     (elements.CubeTest, {"position": Point3(-60,20,140), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     (elements.CubeTest, {"position": Point3(50,-10,120), "forward": Vector3(0,0,-1), "color":(0,0.8,1)}),
     (elements.CubeTest, {"position": Point3(-110,-110,100), "forward": Vector3(0,0,-1), "color":(0,0.8,1)}),
     
     (elements.CubeTest, {"position": Point3(60,50,80), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     (elements.CubeTest, {"position": Point3(150,-180,100), "forward": Vector3(0,0,-1), "color":(0,0.8,1)}),
     (elements.CubeTest, {"position": Point3(-10,110,80), "forward": Vector3(0,0,-1), "color":(0,0.8,1)}),
     
     (elements.CubeTest, {"position": Point3(-160,-120,60), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     (elements.CubeTest, {"position": Point3(-200,-20,40), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     (elements.CubeTest, {"position": Point3(-60,-60,20), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     
     (elements.CubeTest, {"position": Point3(100,100,60), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     (elements.CubeTest, {"position": Point3(20,50,40), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     (elements.CubeTest, {"position": Point3(160,90,20), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),

     (elements.CubeTest, {"position": Point3(-120,-200,60), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     (elements.CubeTest, {"position": Point3(-50,-150,40), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     (elements.CubeTest, {"position": Point3(-160,190,20), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     
     (elements.CubeTest, {"position": Point3(210,-200,60), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     (elements.CubeTest, {"position": Point3(90,-150,40), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     (elements.CubeTest, {"position": Point3(60,190,20), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),

    #  #blue (- left, + right [x])
    #blue mid gate bocks
     (elements.CubeTest, {"position": Point3(0,0,120), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     (elements.CubeTest, {"position": Point3(0,-20,160), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(0,20,160), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(-20,0,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(20,0,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     
     (elements.CubeTest, {"position": Point3(20,-230,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(0,-170,190), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-40,-200,180), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-20,230,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(0,170,190), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(40,200,180), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     
    #blue top gate blocks
     (elements.CubeTest, {"position": Point3(20,-100,220), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(0,-100,160), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-20,-100,220), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(0,-140,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(0,-60,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
    #  
    #blue side1 blocks
     (elements.CubeTest, {"position": Point3(160,100,180), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(100,100,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(40,100,220), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     
     (elements.CubeTest, {"position": Point3(200,60,140), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(120,60,160), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(40,60,180), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     
     (elements.CubeTest, {"position": Point3(100,-40,140), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     (elements.CubeTest, {"position": Point3(140,0,120), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     (elements.CubeTest, {"position": Point3(180,40,100), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     
     (elements.CubeTest, {"position": Point3(120,-80,180), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(60,-120,120), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     (elements.CubeTest, {"position": Point3(180,-180,200), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     
     (elements.CubeTest, {"position": Point3(220,-180,160), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(200,-20,120), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     (elements.CubeTest, {"position": Point3(240,200,200), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
    #  
    #  
    #blue side2 blocks
     (elements.CubeTest, {"position": Point3(-100,160,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,80,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,0,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,-80,200), "forward": Vector3(0,0,-1), "color":(0,0,1)}),
     (elements.CubeTest, {"position": Point3(-100,-160,160), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(-100,100,160), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(-100,40,160), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(-100,-20,160), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(-150,-40,180), "forward": Vector3(0,0,-1), "color":(0,0.3,1)}),
     (elements.CubeTest, {"position": Point3(-200,-60,140), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     
    #blue side healing
     (elements.PowerUp, {"position": Point3(-180,100,160), "forward": Vector3(1,0,0)}),
     (elements.CubeTest, {"position": Point3(-220,100,90), "forward": Vector3(0,0,-1), "color":(0,0.8,1)}),
     (elements.CubeTest, {"position": Point3(-180,60,120), "forward": Vector3(0,0,-1), "color":(0,0.6,1)}),
     (elements.CubeTest, {"position": Point3(-160,160,40), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),
     (elements.CubeTest, {"position": Point3(-90,50,80), "forward": Vector3(0,0,-1), "color":(0,1,0.5)}),

    #center heal
     (elements.PowerUp, {"position": Point3(0,0,0), "forward": Vector3(1,0,0)}),

     # (elements.CubeTest, {"position": Point3(0,100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     # (elements.CubeTest, {"position": Point3(0,-100,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     # (elements.CubeTest, {"position": Point3(100,0,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),
     # (elements.CubeTest, {"position": Point3(-100,0,0), "forward": Vector3(0,0,-1), "color":(0,1,0)}),

    #red transition blocks
     (elements.CubeTest, {"position": Point3(60,-20,-140), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     (elements.CubeTest, {"position": Point3(-50,10,-120), "forward": Vector3(0,0,-1), "color":(1,0.8,0)}),
     (elements.CubeTest, {"position": Point3(110,110,-100), "forward": Vector3(0,0,-1), "color":(1,0.8,0)}),
     
     (elements.CubeTest, {"position": Point3(-60,-50,-80), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     (elements.CubeTest, {"position": Point3(-150,180,-100), "forward": Vector3(0,0,-1), "color":(1,0.8,0)}),
     (elements.CubeTest, {"position": Point3(10,-110,-80), "forward": Vector3(0,0,-1), "color":(1,0.8,0)}),
     
     (elements.CubeTest, {"position": Point3(160,120,-60), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     (elements.CubeTest, {"position": Point3(200,20,-40), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     (elements.CubeTest, {"position": Point3(60,60,-20), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     
     (elements.CubeTest, {"position": Point3(-100,-100,-60), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     (elements.CubeTest, {"position": Point3(-20,-50,-40), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     (elements.CubeTest, {"position": Point3(-160,-90,-20), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),

     (elements.CubeTest, {"position": Point3(120,200,-60), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     (elements.CubeTest, {"position": Point3(50,150,-40), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     (elements.CubeTest, {"position": Point3(160,-190,-20), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     
     (elements.CubeTest, {"position": Point3(-210,200,-60), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     (elements.CubeTest, {"position": Point3(-90,150,-40), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     (elements.CubeTest, {"position": Point3(-60,-190,-20), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),

     #red (+ left, - right [x])
    #red mid gate bocks
     (elements.CubeTest, {"position": Point3(0,0,-120), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     (elements.CubeTest, {"position": Point3(0,20,-160), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(0,-20,-160), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(20,0,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(-20,0,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     
     (elements.CubeTest, {"position": Point3(-20,230,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(0,170,-190), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(40,200,-180), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(20,-230,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(0,-170,-190), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(-40,-200,-180), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     
    #red top gate blocks
     (elements.CubeTest, {"position": Point3(-20,100,-220), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(0,100,-160), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(20,100,-220), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(0,140,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(0,60,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     
    #red side1 blocks
     (elements.CubeTest, {"position": Point3(-160,-100,-180), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(-100,-100,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(-40,-100,-220), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     
     (elements.CubeTest, {"position": Point3(-200,-60,-140), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(-120,-60,-160), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(-40,-60,-180), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     
     (elements.CubeTest, {"position": Point3(-100,40,-140), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     (elements.CubeTest, {"position": Point3(-140,0,-120), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     (elements.CubeTest, {"position": Point3(-180,-40,-100), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     
     (elements.CubeTest, {"position": Point3(-120,80,-180), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(-60,120,-120), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     (elements.CubeTest, {"position": Point3(-180,180,-200), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     
     (elements.CubeTest, {"position": Point3(-220,180,-160), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(-200,20,-120), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     (elements.CubeTest, {"position": Point3(-240,-200,-200), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     
     
    #red side2 blocks
     (elements.CubeTest, {"position": Point3(100,-160,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(100,-80,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(100,0,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(100,80,-200), "forward": Vector3(0,0,-1), "color":(1,0,0)}),
     (elements.CubeTest, {"position": Point3(100,160,-160), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(100,-100,-160), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(100,-40,-160), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(100,20,-160), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(150,40,-180), "forward": Vector3(0,0,-1), "color":(1,0.3,0)}),
     (elements.CubeTest, {"position": Point3(200,60,-140), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     
    #red side healing
     (elements.PowerUp, {"position": Point3(180,-100,-160), "forward": Vector3(1,0,0)}),
     (elements.CubeTest, {"position": Point3(220,-100,-90), "forward": Vector3(0,0,-1), "color":(1,0.8,0)}),
     (elements.CubeTest, {"position": Point3(180,-60,-120), "forward": Vector3(0,0,-1), "color":(1,0.6,0)}),
     (elements.CubeTest, {"position": Point3(160,-160,-40), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),
     (elements.CubeTest, {"position": Point3(90,-50,-80), "forward": Vector3(0,0,-1), "color":(0.5,1,0)}),


    #wall
     (wall.Wall, {"position": Point3(-250, 0, 0), "forward": Vector3( 1, 0, 0)}), # left
     (wall.Wall, {"position": Point3( 250, 0, 0), "forward": Vector3(-1, 0, 0)}), # right
     (wall.Wall, {"position": Point3(0, -250, 0), "forward": Vector3(0,  1, 0), "up": Vector3(0, 0, -1)}), # bottom
     (wall.Wall, {"position": Point3(0,  250, 0), "forward": Vector3(0, -1, 0), "up": Vector3(0, 0, -1)}), # top
     (wall.Wall, {"position": Point3(0, 0, -250), "forward": Vector3(0, 0,  1)}), # front
     (wall.Wall, {"position": Point3(0, 0,  250), "forward": Vector3(0, 0, -1)}),  # back
    ]

    spawn_points = [
    #red spawn
     (spawn.SpawnGate, {"position": Point3(0, 0,  -249), "forward": Vector3(0, 0, 1), "color": Vector3(1,0,0), "team": "RED"}),
     (spawn.SpawnGate, {"position": Point3(-100, -100,  -249), "forward": Vector3(0, 0, 1), "color": Vector3(1,0,0), "team": "RED"}),
     (spawn.SpawnGate, {"position": Point3(100, -100,  -249), "forward": Vector3(0, 0, 1), "color": Vector3(1,0,0), "team": "RED"}),
     (spawn.SpawnGate, {"position": Point3(0, 100,  -249), "forward": Vector3(0, 0, 1), "color": Vector3(1,0,0), "team": "RED"}),

    #blue spawn
     (spawn.SpawnGate, {"position": Point3(0, 0,  249), "forward": Vector3(0, 0, -1), "color": Vector3(0,0,1), "team": "BLUE"}),
     (spawn.SpawnGate, {"position": Point3(100, 100,  249), "forward": Vector3(0, 0, -1), "color": Vector3(0,0,1), "team": "BLUE"}),
     (spawn.SpawnGate, {"position": Point3(-100, 100,  249), "forward": Vector3(0, 0, -1), "color": Vector3(0,0,1), "team": "BLUE"}),
     (spawn.SpawnGate, {"position": Point3(0, -100,  249), "forward": Vector3(0, 0, -1), "color": Vector3(0,0,1), "team": "BLUE"})
    ]



default_room = TestRoom



#TODO: def room_factory(file: string) -> Room:
