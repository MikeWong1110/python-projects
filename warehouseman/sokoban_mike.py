from pycat.core import Sprite, Window, Color, KeyCode, Point
from pycat.extensions.ldtk import LdtkLayeredLevel
import random

level=LdtkLayeredLevel.from_file("sokoban_levels.ldtk", "Level_0","sokoban_levels/png/",{
    "Tiles":0
})


grid_size=15
window= Window(enforce_window_limits=False,height=960,width=960)
level.render(window,debug_entities=True)

class Pixel(Sprite):
    def on_create(self):
        
        self.placeholder=window.create_sprite(scale=64)
        
        self.placeholder.opacity=0

    def setup(self, pixel_type):
        self.placeholder.goto(self)
        if pixel_type=="w":
            if "wall" not in self.tags:
                self.add_tag("wall")
                self.color=Color.BLUE
                self.placeholder.opacity=255
                self.placeholder.color=Color.BLUE
        if pixel_type=="f":
            if "wall" in self.tags:
                self.tags.remove("wall")
            if "finish" not in self.tags:
                self.add_tag("finish")
                self.color=Color.GREEN
                self.placeholder.opacity=255
                self.placeholder.color=Color.GREEN
                self.placeholder.scale=64

    def on_update(self,dt):
        if "finish" in self.tags:
            if check_win():
                print("win")
                window.close()

        

grid=[]
for rows in range(grid_size):
    grid.append([None]*grid_size)

for x in range(grid_size):
    for y in range(grid_size):
        cell=window.create_sprite(Pixel,x=x*64+32,y=y*64+32)
        grid[x][y]=cell
        if x==0 or y==0 or x==grid_size-1 or y==grid_size-1:
            cell.setup("w")

class Box(Sprite):
    def move(self,direction):
        if direction=="u" :
            self.y+=64
        if direction=="d":
            self.y-=64

        if direction=="l":
            self.x-=64
        if direction=="r":
            self.x+=64

    def on_create(self):
        self.scale=60
        self.add_tag("box")
        self.color=Color.RED
        self.layer=2

class Sokoban(Sprite):
    
    def on_create(self):
        self.scale=60
        self.goto(grid[1][1])
        self.vector_dict={
            "u":Point(0,64),
            "d":Point(0,-64),
            "l":Point(-64,0),
            "r":Point(64,0),
        }
        self.opposite_dict={
            "u":"d",
            "d":"u",
            "r":"l",
            "l":"r",
        }

    def try_move(self,direction):
        boxes=window.get_sprites_with_tag("box")
        self.position+=self.vector_dict[direction]
        if self.is_touching_any_sprite_with_tag("wall"):
            self.try_move(self.opposite_dict[direction])
            return
        for box in boxes:
            if self.is_touching_sprite(box):
                box.move(direction)
                if box.is_touching_any_sprite_with_tag("wall") or box.is_touching_any_sprite_with_tag("box"):
                    box.move(self.opposite_dict[direction])
                    self.try_move(self.opposite_dict[direction])
                    return

    

    def on_update(self, dt):
        if window.is_key_down(KeyCode.W):
            self.try_move("u")

        elif window.is_key_down(KeyCode.A):
            self.try_move("l") 
        
        elif window.is_key_down(KeyCode.S):
            self.try_move("d")

        elif window.is_key_down(KeyCode.D):
            self.try_move("r")

def check_win():
    finish_pixel=window.get_sprites_with_tag("finish")
    for pixel in finish_pixel:
        if not pixel.is_touching_any_sprite_with_tag("box"):
            return False
    return True

window.create_sprite(Sokoban)
box=window.create_sprite(Box)
box.goto(grid[2][2])
box=window.create_sprite(Box)
box.goto(grid[2][3])
grid[random.randint(1,grid_size-2)][random.randint(1,grid_size-2)].setup("f")
grid[random.randint(1,grid_size-2)][random.randint(1,grid_size-2)].setup("f")

window.run()