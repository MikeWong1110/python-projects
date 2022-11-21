from pycat.core import Window, Sprite, Color, KeyCode, Point, RotationMode
from pycat.extensions.ldtk import LdtkLayeredLevel
from random import choice
import string

window = Window()

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


def find_cell(position):
    cells = window.get_sprites_with_tag("cell")
    for cell in cells:
        if cell.distance_to(position) < 2:
            return cell
    return None


class Mikeman(Sprite):
    def on_create(self):
        self.color = Color.YELLOW
        self.scale = 60
        self.goto(window.get_sprite_with_tag("ldtk_start"))
        self.queued_rotation = None
        self.rotation = 0
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
            if self.distance_to(self.target_cell) > 3:
                self.move_forward(2)

            else:
                self.goto(self.target_cell)
                self.target_cell = None

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

        if window.is_key_down(KeyCode.W):
            self.queued_rotation = 90
        elif window.is_key_down(KeyCode.A):
            self.queued_rotation = 180
        elif window.is_key_down(KeyCode.S):
            self.queued_rotation = 270
        elif window.is_key_down(KeyCode.D):
            self.queued_rotation = 0


class Cell(Sprite):
    def on_create(self):
        self.opacity = 110
        self.name = ""
        self.scale = 32
        self.add_tag("cell")

        # self.is_barrier = choice([False, False, True, False])
        # if self.is_barrier:
        #     self.color = Color.BLACK

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


for x in range(0, grid_x*64, 64):

    for y in range(0, grid_y*64, 64):

        cell = window.create_sprite(Cell, x=x+32, y=y+32)
        if cell.is_touching_any_sprite_with_tag("ldtk_wall"):
            cell.delete()

window.create_sprite(Mikeman)
window.run()
