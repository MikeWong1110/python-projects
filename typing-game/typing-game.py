from pycat.core import Window, Sprite, Label, Point, Color, KeyCode, Scheduler
from pycat.base.event import KeyEvent
import random

# letters=list(map(chr, range(97, 123)))
letters=["what","where","when","why","who","how"]
summon_speed=0.6

window=Window(background_image="background.jpg",enforce_window_limits=True,width=700,height=400)
enemy_list=[]

class Player(Sprite):
    def on_create(self):
        self.scale=50
        self.score=0
        self.color=Color.BLUE

    def on_update(self, dt):
        if self.is_touching_any_sprite_with_tag("enemy"):
            window.close()

    def shoot(self):
        self.score+=1
        print(self.score)

        bullet=window.create_sprite(Bullet)
        bullet.goto(self)

        if self.score==30:
            self.score=0
            global summon_speed
            summon_speed-=0.1
            Scheduler.cancel_update(spawn_enemy)
            Scheduler.update(spawn_enemy,summon_speed)

player=window.create_sprite(Player,x=60,y=80)

class TypeableLabel(Label):
    def on_create(self):
        self.parent=None
        self.disabled=False
        self.text=random.choice(letters)
        window.subscribe(on_key_press=self.on_key_press)

    # def on_update(self,dt):

    def on_key_press(self,key: KeyEvent):
        if not self.disabled and enemy_list[0]==self.parent and self.text!='':
            if self.text[0] == key.character:
                self.text=self.text[1:]
                player.shoot()

class Bullet(Sprite):
    def on_create(self):
        self.add_tag('bullet')

    def on_update(self, dt):
        self.x+=30

        if self.is_touching_any_sprite_with_tag("enemy"):
            Scheduler.wait(0.01,self.delete)
            
        
        self.scale=50
        self.color=Color.CYAN
        if self.x>=650:
            self.delete()

class Enemy(Sprite):
    def on_create(self):
        self.add_tag("enemy")
        self.scale=50
        self.color=Color.RED
        self.label=window.create_label(TypeableLabel)
        self.label.parent=self
        
        self.x=window.width
        self.y=player.y
        

    def on_update(self,dt):
        self.label.position=Point(self.position.x-self.scale/4,self.position.y+self.scale/4)
        # if self.label.text=='':
        if self.is_touching_any_sprite_with_tag("bullet") and len(self.label.text)==0:
            self.label.disabled=True
            enemy_list.remove(self)
            self.delete() #maybe special effect in the future?
        self.point_toward_sprite(player)
        self.move_forward(3)
        
def spawn_enemy():
    enemy=window.create_sprite(Enemy)
    enemy_list.append(enemy)

Scheduler.update(spawn_enemy,summon_speed)

window.run()