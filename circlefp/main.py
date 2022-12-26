from pycat.core import Sprite, Window, Color, KeyCode, Point, RotationMode
import random

current_enemy = "triangle"
current_obstacle = "rectangle"
current_npc = ""

window = Window()
# draw_sprite_rects=True


class Circle(Sprite):
    def on_create(self):
        # self.image=""
        self.add_tag("player")
        self.can_jump = False
        self.x = 640
        self.y = 640
        self.scale = 50
        self.FRICTION = 0.96
        self.GRAVITY = -0.8
        self.speed = Point(0, 0)

    def on_update(self, dt):

        if self.is_touching_any_sprite_with_tag(current_enemy):
            window.close()

        self.speed.x *= self.FRICTION
        self.speed.y += self.GRAVITY

        self.take_user_input()

        self.position += self.speed

        self.adjust_player_position()

        if self.y<=0:
            self.delete()

    def take_user_input(self):

        if window.is_key_pressed(KeyCode.D):
            self.speed.x += 0.3

        if window.is_key_pressed(KeyCode.A):
            self.speed.x -= 0.3

        if window.is_key_down(KeyCode.W) and self.can_jump:
            self.speed.y = 20
            self.can_jump = False

    def adjust_player_position(self):
        ground = False
        ceiling = False

        for obstacle in window.get_sprites_with_tag(current_obstacle):
            obstacle: Rectangle

            if (self.is_touching_sprite(obstacle)):
                if self.speed.y < 0:
                    while self.y < 0 or self.is_touching_sprite(obstacle):
                        self.y += 0.05
                        ground = True

                    if not obstacle.resistant:
                        self.can_jump = True
                    if obstacle.bouncy:
                        self.speed.y = abs(self.speed.y)-(abs(self.speed.y)/5)
                    else:
                        self.speed.y = 0

                if self.speed.y >= 0:
                    if obstacle.headbump and (self.y+(self.height/2) < obstacle.y+self.height/10 or self.distance_to(obstacle)+self.width/10<obstacle.width/2+self.width/2):
                        while self.is_touching_sprite(obstacle):
                            self.y -= 1
                            ceiling = True
                        print("hehehehaw")

                        self.speed.y = 0
                    else:
                        self.speed.y -= 0.2

                if ground and ceiling:
                    self.delete()
        print(ground, ceiling)

        if self.is_touching_any_sprite_with_tag("rectangle"):
            if self.x <= obstacle.x:
                while self.is_touching_any_sprite_with_tag("rectangle"):
                    self.x -= 0.05

            elif self.x >= obstacle.x:
                while self.is_touching_any_sprite_with_tag("rectangle"):
                    self.x += 0.05


class Rectangle(Sprite):
    def on_create(self):
        self.rotation_mode = RotationMode.RIGHT_LEFT
        self.add_tag("rectangle")
        self.headbump = False
        self.bouncy = False
        self.resistant = False
        self.moving = False
        self.start_point = None
        self.end_point = None
        self.going_to = "end"

    def on_update(self, dt):
        if self.bouncy:
            self.color = Color.YELLOW
            self.resistant = False
        if self.resistant:
            self.color = Color.ROSE

        if self.moving:
            self.headbump = True
            self.color = Color.GREEN
            if self.start_point and self.end_point:
                if self.going_to == "end":
                    self.point_toward(self.end_point)
                    self.move_forward(1)
                    if self.distance_to(self.end_point) < 2:
                        self.position = self.end_point
                        self.going_to = "start"

                elif self.going_to == "start":
                    self.point_toward(self.start_point)
                    self.move_forward(1)
                    if self.distance_to(self.start_point) < 2:
                        self.position = self.start_point
                        self.going_to = "end"


class Triangle(Sprite):
    def on_create(self):
        self.image = "white_triangle.png"
        self.hitbox = window.create_sprite()
        self.hitbox.goto(self)
        self.hitbox.scale = 23
        self.hitbox.opacity = 0
        self.hitbox.add_tag("triangle")

    def on_update(self, dt):
        self.hitbox.goto(self)


class Oval(Sprite):
    def on_create(self):
        self.scale_x = 2
        self.cooldown = 0
        self.target_oval: Oval

    def on_update(self, dt):
        if self.is_touching_sprite(player) and self.cooldown == 0:
            if self.target_oval:
                player.goto(self.target_oval)
                self.target_oval.cooldown = 5

        if self.cooldown > 0:
            self.cooldown -= dt
            if self.cooldown <= 0:
                self.cooldown = 0


class Hexagon(Sprite):
    pass


hb_platform = window.create_sprite(
    Rectangle, x=500, y=100, scale_x=1280, scale_y=10)
nothb_platform = window.create_sprite(
    Rectangle, x=1180, y=100, scale_x=100, scale_y=10)
nothb_platform.moving = True
nothb_platform.end_point = Point(1180, 300)
nothb_platform.start_point = Point(1180, 100)

e=window.create_sprite(
    Rectangle, x=500, y=300, scale_x=1280, scale_y=10
)
e.bouncy=True
e.headbump=True

# spike=window.create_sprite(Triangle,x=800,y=132)


player = window.create_sprite(
    Circle, x=100, y=200)

window.run()
