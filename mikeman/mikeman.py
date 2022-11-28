from pycat.core import Window, Sprite, Color, KeyCode, Point, RotationMode
from pycat.extensions.ldtk import LdtkLayeredLevel
from random import choice
from enum import Enum
from david_breadth_first_search import BreathFirstSearch
import string

window = Window()

bfs=BreathFirstSearch()

grid_x = 16
grid_y = 10

level = LdtkLayeredLevel.from_file(
    ldtk_file_path="level1.ldtk",
    level_id="Level_0",
    image_path="level1/png/",
    layer_ordering={
        "Tiles": -1,
    },

)

level.render(window, debug_entities=True)

position_to_cell={}

class GhostState(Enum):
    CHASING=1
    DAZED=2
    GOHOME=3
    REST=4


def find_cell(position):
    return position_to_cell.get( (int(position.x), int(position.y) ),None)


class Mikeman(Sprite):
    def on_create(self):
        self.add_tag("man")
        self.color = Color.YELLOW
        self.scale=60
        # self.image = "pacman.png"
        self.goto(window.get_sprite_with_tag("ldtk_start"))
        self.queued_rotation = None
        self.rotation = 0
        self.current_cell=find_cell(self.position)
        self.not_moving = False
        self.rotation_to_offset = {
            0: Point(64, 0),
            180: Point(-64, 0),
            90: Point(0, 64),
            270: Point(0, -64),
        }

        self.target_cell = find_cell(
            self.position + self.rotation_to_offset[self.rotation]
        )

    def on_update(self, dt):
        if self.target_cell != None:
            if self.distance_to(self.target_cell) > 2:
                self.move_forward(8)

            else:
                self.goto(self.target_cell)
                self.target_cell = None
                self.current_cell=find_cell(self.position)

        if not self.target_cell:
            old_rotation = self.rotation
            
            if self.queued_rotation != None:
                self.rotation = self.queued_rotation
                self.target_cell = find_cell(
                    self.position + self.rotation_to_offset[self.rotation]
                )
                if self.target_cell:
                    self.queued_rotation = None

            if not self.target_cell:
                self.rotation = old_rotation
                self.target_cell = find_cell(
                    self.position + self.rotation_to_offset[self.rotation]
                )

        for bit in window.get_sprites_with_tag("bit"):
            if self.is_touching_sprite(bit):
                if bit.big:
                    ghost.state=GhostState.DAZED
                bit.delete()

        if window.is_key_down(KeyCode.W):
            self.queued_rotation = 90
        elif window.is_key_down(KeyCode.A):
            self.queued_rotation = 180
        elif window.is_key_down(KeyCode.S):
            self.queued_rotation = 270
        elif window.is_key_down(KeyCode.D):
            self.queued_rotation = 0

            
class Ghost(Sprite):
    def on_create(self):
        self.timer=0
        self.state=GhostState.CHASING
        self.scale=60
        self.color=Color.RED
        self.goto(window.get_sprite_with_tag("ldtk_enemyspawn"))
        self.home=find_cell(self.position)
        self.target_cell=None
        
    def chase(self,dt):
        if self.target_cell:
            if self.distance_to(self.target_cell) > 2:
                self.point_toward_sprite(self.target_cell)
                self.move_forward(8)

            else:
                self.goto(self.target_cell)
                self.target_cell=None

        if not self.target_cell:
            print(find_cell(self.position))
            print(mikeman.current_cell)
            path = bfs.solve(find_cell(self.position),mikeman.current_cell) 
            print(path)
            if len(path)>1:
                self.target_cell=path[1]

        if self.is_touching_any_sprite_with_tag("man"):
            window.close()

    def daze(self,dt):
        self.timer+=dt
        if self.timer>5:
            self.state=GhostState.CHASING
            self.timer=0

        elif self.is_touching_any_sprite_with_tag("man"):
            self.state=GhostState.GOHOME
            self.timer=0
            self.target_cell=None


    def go_home(self,dt):
        if self.target_cell:
            if self.distance_to(self.target_cell) > 2:
                self.point_toward_sprite(self.target_cell)
                self.move_forward(8)

            else:
                self.goto(self.target_cell)
                if self.target_cell==self.home:
                    self.state==GhostState.REST
                    return
                self.target_cell=None

        if not self.target_cell:
            path = bfs.solve(find_cell(self.position),self.home) 
            if len(path)>1:
                self.target_cell=path[1]

    def rest(self,dt):
        self.timer+=dt
        if self.timer>5:
            self.timer=0
            self.state=GhostState.CHASING

    def on_update(self, dt):
        if self.state==GhostState.CHASING:
            self.chase(dt)
        elif self.state==GhostState.DAZED:
            self.daze(dt)
        elif self.state==GhostState.GOHOME:
            self.go_home(dt)
        elif self.state==GhostState.REST:
            self.rest(dt)


                    

class Bit(Sprite):
    def on_create(self):
        self.layer=100
        self.big=False
        self.add_tag("bit")
        self.scale=20
        self.color=Color.WHITE

class Cell(Sprite):
    def on_create(self):
        self.opacity = 0
        self.name = ""
        self.scale = 32
        self.add_tag("cell")
        

    def setup_bit(self):
        self.bit=window.create_sprite(Bit)
        self.bit.goto(self)
        self.bit.big = choice([False, False, True, False, False, False])
        if self.bit.big:
            self.bit.color = Color.BLACK

    def get_neighbors(self):
        neighbors = []
        right = find_cell(self.position+Point(64, 0))
        if right:
            neighbors.append(right)

        left = find_cell(self.position+Point(-64, 0))
        if left:
            neighbors.append(left)

        up = find_cell(self.position+Point(0, 64))

        if up:
            neighbors.append(up)

        down = find_cell(self.position+Point(0, -64))

        if down:
            neighbors.append(down)

        return neighbors

    def get_empty_neighbors(self):

        change_position = [Point(64,0),Point(-64,0),Point(0,64),Point(0,-64)]
        neighbors = []

        for p in change_position: 
            cell = find_cell(self.position+p)

            if cell:
                neighbors.append(cell)

        return neighbors


for x in range(0, grid_x*64, 64):

    for y in range(0, grid_y*64, 64):

        cell = window.create_sprite(Cell, x=x+32, y=y+32)
        if cell.is_touching_any_sprite_with_tag("ldtk_wall"):
            cell.delete()

        else:
            position_to_cell[(int(cell.position.x),int(cell.position.y))]= cell
            cell.setup_bit()

mikeman=window.create_sprite(Mikeman)
ghost=window.create_sprite(Ghost)
window.run()
