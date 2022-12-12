from pycat.core import Sprite, Window, Color, KeyCode,Point
import random

window=Window()

class Player(Sprite):
    def on_create(self):
        # self.image=""
        self.can_jump=False
        self.x=640
        self.y=640
        self.scale=50
        self.FRICTION=0.96
        self.GRAVITY=-0.8
        self.speed=Point(0,0)

    def on_update(self,dt):
        self.speed.y+=self.GRAVITY
        self.speed.x*=self.FRICTION
        if window.is_key_pressed(KeyCode.D):
            self.speed.x+=0.3

        if window.is_key_pressed(KeyCode.A):
            self.speed.x-=0.3

        if (self.y<=0 or self.is_touching_any_sprite_with_tag("obstacle")):
            if self.speed.y<0:
                while self.y<0 or self.is_touching_any_sprite_with_tag("obstacle"):
                    self.y+=1
                self.can_jump=True
                self.speed.y=0
            elif self.speed.y>0:
                self.speed.y-=1
                
            



        if window.is_key_down(KeyCode.W) and self.can_jump:
            self.speed.y=20
            self.can_jump=False

        self.position+=self.speed
        
        
class Obstacle(Sprite):
    def on_create(self):
        self.add_tag("obstacle")

window.create_sprite(Obstacle,x=640,y=100,scale_x=100,scale_y=10)



player=window.create_sprite(Player)

window.run()