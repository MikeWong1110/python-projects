from pycat.core import Window, Sprite, Label, Point, Color, KeyCode, Scheduler
import random
from enum import Enum

class GunMode(Enum):
    PISTOL=1
    GATLING=2
    SHOTGUN=3
    RPG=4

window = Window( enforce_window_limits=False)


class Lifebar(Sprite):
    def on_create(self):
        
        self.max_health = 200
        self.health = self.max_health
        self.background = window.create_sprite()
        self.background.color=Color.RED
        self.background.scale_y = 20
        self.background.scale_x = self.max_health + 12
        self.scale_y = 10
        self.scale_x = self.max_health
        self.layer=100
        self.color=Color.BLUE

    def refresh(self):
        self.health = self.max_health
        self.scale_x=self.health

    def on_update(self, dt):
        self.background.goto(self)
        if self.health<=0:
            spaceship.delete()
            self.scale_x=0
        else:
            self.scale_x=self.health

        self.health-=1

lifebar = window.create_sprite(Lifebar)
lifebar.x = window.width/2
lifebar.y = window.height-20

class ScoreLabel(Label):
    def on_create(self):
        self.score = 0
        self.text = "Score: "+str(self.score)

    def add_score(self):
        self.score += 1
        self.text = "Score: "+str(self.score)
        lifebar.refresh()


score_label = window.create_label(ScoreLabel)
score_label.x = window.width/2-45
score_label.y = window.height-30


class WrapSprite(Sprite):
    def wrap(self):
        if self.x >= window.width+self.width/2:
            self.x = 0-self.width/2
        elif self.x <= 0-self.width/2:
            self.x = window.width+self.width/2
        if self.y >= window.height+self.width/2:
            self.y = 0-self.width/2
        elif self.y <= 0-self.width/2:
            self.y = window.height+self.width/2


class Bullet(WrapSprite):
    def on_create(self):
        self.owner = None
        self.add_tag("bullet")
        self.image = "images/asteroids/bullet.png"

    def on_update(self, dt):
        self.move_forward(30)
        if self.is_touching_window_edge():
            self.delete()


class Spaceship(WrapSprite):
    def on_create(self):
        self.color = Color.BLUE
        self.image = "images/asteroids/ship.png"
        self.speed = 0
        self.gun_mode=GunMode.PISTOL
        self.gun_modes_list=[GunMode.GATLING,GunMode.SHOTGUN,GunMode.RPG,GunMode.PISTOL]

    def on_update(self, dt):
        for asteroid in window.get_sprites_with_tag('asteroid'):
            if self.is_touching_sprite(asteroid):
                lifebar.health-=lifebar.max_health/4
                asteroid.delete()
        self.wrap()
        if window.is_key_pressed(KeyCode.W):
            if self.speed <= 30:
                self.speed += 0.2
            else:
                self.speed = 30
        if window.is_key_pressed(KeyCode.S):
            if self.speed > 0:
                self.speed *= 0.88
            else:
                self.speed = 0

        if window.is_key_pressed(KeyCode.D):
            self.rotation -= 4
        if window.is_key_pressed(KeyCode.A):
            self.rotation += 4

        
        if self.gun_mode==GunMode.PISTOL:
            if window.is_key_down(KeyCode.J):
                bullet = window.create_sprite(Bullet)
                bullet.owner = self
                bullet.goto(self)
                bullet.rotation = self.rotation

        elif self.gun_mode==GunMode.GATLING:
            if window.is_key_pressed(KeyCode.J):
                bullet = window.create_sprite(Bullet)
                bullet.owner = self
                bullet.goto(self)
                bullet.rotation = self.rotation

        elif self.gun_mode==GunMode.SHOTGUN:
            if window.is_key_down(KeyCode.J):
                for offset in range(-9,9,3):
                    bullet = window.create_sprite(Bullet)
                    bullet.owner = self
                    bullet.goto(self)
                    bullet.rotation = self.rotation+offset

        elif self.gun_mode==GunMode.RPG:
            pass #add RPG mode in the guns haha pew pew boooooooom

        if window.is_key_down(KeyCode.K):
            self.gun_mode=self.gun_modes_list[0]
            self.gun_modes_list.append(self.gun_modes_list[0])
            self.gun_modes_list=self.gun_modes_list[1:]
            print("now using:")
            print(self.gun_mode)
            

        self.speed *= 0.98
        self.move_forward(self.speed)


class Asteroid(WrapSprite):
    def on_create(self):
        self.add_tag("asteroid")
        self.size = ""
        self.color = Color.random_rgb()
        self.image_set = False

    def on_update(self, dt):
        if self.size != "" and not self.image_set:
            self.image = "images/asteroids/"+self.size + \
                str(random.randint(1, 3))+".png"
            self.image_set = True
        self.wrap()
        self.move_forward(4)

        for bullet in self.get_touching_sprites_with_tag("bullet"):
            bullet.delete()
            if self.size == "big":
                for rotation in [90, -90]:
                    children_asteroid = window.create_sprite(Asteroid)
                    children_asteroid.size = "med"
                    children_asteroid.goto(self)
                    children_asteroid.rotation = self.rotation+rotation

            if self.size == "med":
                for rotation in [90, -90]:
                    children_asteroid = window.create_sprite(Asteroid)
                    children_asteroid.size = "small"
                    children_asteroid.goto(self)
                    children_asteroid.rotation = self.rotation+rotation

            score_label.add_score()
            self.delete()


def spawn():
    asteroid = window.create_sprite(Asteroid)
    asteroid.size = "big"
    random_y = random.randint(0, window.height)
    random_x = random.randint(0, window.width)
    asteroid.position = random.choice([
        Point(0, random_y),
        Point(window.width, random_y),
        Point(random_x, 0),
        Point(random_x, window.height)
    ])
    asteroid.point_toward_sprite(spaceship)


Scheduler.update(spawn, 2)

spaceship = window.create_sprite(
    Spaceship, y=window.height/2, x=window.width/2)

window.run()
