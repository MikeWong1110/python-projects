from operator import index
from pycat.core import Window, Sprite, Point, Color, KeyCode, Label
from pycat.base.event.mouse_event import MouseButton, MouseEvent
import string
from random import choice
from bfs import BFS

grid_x = 19
grid_y = 9

window = Window()

e = window.create_sprite(scale=10000)
e.color = Color.PURPLE
e.layer = -1

output = window.create_label(Label, x=20, y=620)

start_cell = None
end_cell = None


def find_cell(position):
    cells = window.get_sprites_with_tag("cell")
    for cell in cells:
        if cell.distance_to(position) < 2:
            return cell
    return None


class Dude(Sprite):
    def on_create(self):
        self.found_path = False

    def on_update(self, dt):
        if window.is_key_down(KeyCode.E) and not self.found_path:
            bfs.solve(start=start_cell, end=end_cell)
            if bfs.get_path() != []:
                output.text = "Output: Successful"
                self.colour_the_stuff()
            else:
                output.text = "Output: Unsuccessful"
            

    def colour_the_stuff(self):
        for cell in bfs.get_path():
            if cell != start_cell and cell != end_cell:
                cell.color = Color.BLUE
        self.found_path = True
        md=window.create_sprite(MovingDude)
        md.goto(start_cell)


class MovingDude(Sprite):
    def on_create(self):
        self.path= bfs.get_path()
        self.layer=10
        self.index = 1
        self.scale=16
        self.target=self.path[self.index]

    def on_update(self, dt):
        if self.target==end_cell:
            return "Deez nuts"
        if self.distance_to(self.target)<2 and len(self.path)-1>self.index:
            self.index+=1
        else:
            self.target = self.path[self.index]
            self.point_toward_sprite(self.target)
            self.move_forward(2)



class Cell(Sprite):
    def on_create(self):
        self.name = ""
        self.scale = 64
        self.add_tag("cell")
        self.is_barrier = choice([False, False, True, False])
        if self.is_barrier:
            self.color = Color.BLACK

    def get_neighbors(self):
        neighbors = []
        right = find_cell(self.position+Point(64, 0))
        if right and not right.is_barrier:
            neighbors.append(right)

        left = find_cell(self.position+Point(-64, 0))
        if left and not left.is_barrier:
            neighbors.append(left)

        up = find_cell(self.position+Point(0, 64))

        if up and not up.is_barrier:
            neighbors.append(up)

        down = find_cell(self.position+Point(0, -64))

        if down and not down.is_barrier:
            neighbors.append(down)

        return neighbors

    def on_click(self, mouse_event: MouseEvent):

        global end_cell
        global start_cell

        if not self.is_barrier:

            if mouse_event.button == MouseButton.RIGHT:

                if end_cell != None:
                    end_cell.color = Color.WHITE

                self.color = Color.RED
                end_cell = self

            elif mouse_event.button == MouseButton.LEFT:

                if start_cell != None:
                    start_cell.color = Color.WHITE

                self.color = Color.GREEN
                start_cell = self

        if mouse_event.button == MouseButton.MIDDLE:
            if start_cell != self and end_cell != self:
                if not self.is_barrier:
                    self.is_barrier = True
                    self.color = Color.BLACK
                else:
                    self.is_barrier = False
                    self.color = Color.WHITE


for x in range(0, grid_x):

    for y in range(0, grid_y):

        cell = window.create_sprite(Cell, x=x*64+32, y=y*64+32)
        cell.name = string.ascii_lowercase[len(
            window.get_sprites_with_tag(cell)) - 1]

bfs = BFS()

window.create_sprite(Dude)

window.run()
