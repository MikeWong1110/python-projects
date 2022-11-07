from pycat.core import Window, Sprite, Point, Color
import string
from random import choice
from bfs import BFS

grid_x = 16
grid_y = 9

window = Window()


def find_cell(position):
    cells = window.get_sprites_with_tag("cell")
    for cell in cells:
        if cell.distance_to(position) < 2:
            return cell
    return None


class Cell(Sprite):
    def on_create(self):
        self.name = ""
        self.scale = 64
        self.add_tag("cell")
        self.is_barrier = choice([False, False, True, False])
        if self.is_barrier:
            self.color = Color.BLACK
        # self.color = Color.random_rgb()

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


for x in range(0, grid_x):
    for y in range(0, grid_y):
        cell = window.create_sprite(Cell, x=x*64+32, y=y*64+32)
        cell.name = string.ascii_lowercase[len(
            window.get_sprites_with_tag(cell))-1]

start_cell = find_cell(Point(64+32, 64+32))
start_cell.is_barrier=False
start_cell.color = Color.GREEN
end_cell = find_cell(Point(15*64+32, 8*64+32))
end_cell.is_barrier=False
end_cell.color = Color.RED

bfs = BFS()
bfs.solve(
    start=start_cell,
    end=end_cell
)

for cell in bfs.get_path():
    if cell != start_cell and cell != end_cell:
        cell.color = Color.BLUE

print(bfs.get_path())

window.run()
