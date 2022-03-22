from pycat.window import Window
from pycat.keyboard import KeyCode
from pycat.sprite import Sprite
from pyglet.clock import schedule_interval as pyglet_schedule_interval
from pyglet.clock import unschedule as pyglet_unschedule
from pycat.scheduler import Scheduler
from pycat.collision import is_aabb_collision
from pycat.resource import set_resource_directory
from pycat.label import Label
from pycat.geometry.point import Point
from pycat.base.base_sprite import RotationMode
from pycat.core import Player, Color
from pycat.math import get_distance 
import random

window = Window(background_image="img/background.jpg")
gunshot_sniper = Player("audio/gunshot_sniper.mp3")
grenade_explosion = Player("audio/grenade_explosion1.mp3")
explosion = Player("audio/explosion1.mp3")
laser_shot = Player("audio/laser_shot.mp3")



class Explosion(Sprite):

    def on_create(self):
        self.image = 'img/explosion.gif'
        self.timer = 0
        self.scale = 0.4

    def on_update(self,dt):
        self.timer += dt
        if self.timer >= 2.8:
            self.delete()

        for enemy in self.window.get_sprites_with_tag("enemy"):
            if is_aabb_collision(self, enemy):
                    enemy.receive_damage(25)

class Tower(Sprite):
    
    def on_create(self):
        self.y = window.center.y
        self.x = window.center.x
        self.image = "img/Mike_tower.png"
        self.scale = 1
        self.health = 100 # 2 = full health, 1 = half health, 0 = dead
        self.add_tag("tower")

         
        self.time_survived = 0
        self.time_survived_label = window.create_label()
        self.time_survived_label.text = str(round(self.time_survived))
        self.time_survived_label.x = self.position.x - 10
        self.time_survived_label.y=self.position.y + 80

        self.health_label= window.create_label()
        self.health_label.text = str(self.health)
        self.health_label.x = self.position.x - 50
        self.health_label.y = self.position.y - 80
    
    def on_update(self,dt):

        if self.health <= 50 and self.health > 0: # Half health
            self.image = "img/Mike_tower_half.png"
        elif self.health > 50:
            self.image = "img/Mike_tower.png"
        elif self.health <= 0:
            self.health_label.text = "You Lost..."
            sniper.delete()
            # self.layer = 1000
            e = window.create_sprite(Explosion)
            e.layer = 1000
            explosion.play()
            e.goto(self)
            e.scale = 6
            self.delete()

        self.time_survived += dt
        self.time_survived_label.text = str(round(self.time_survived))
        if self.health > 0:
            self.health_label.text ="HP: " + str(self.health)
            

    def receive_damage(self, damage):
        self.health -= damage


class Sniper(Sprite):
    def on_create(self):
        self.scale = 10
        self.color = (255,255,255)
        self.bullet_reload_timer = 0
        self.bullet_type = "bullet"
        self.goto(tower)
        self.grenade_reload_timer = 0
        self.blackhole_reload_timer = 0

    def on_update(self,dt):

        self.grenade_reload_timer += dt
        self.bullet_reload_timer += dt
        self.blackhole_reload_timer += dt

        self.point_toward_mouse_cursor()

        if self.bullet_type == "blackhole" and self.blackhole_reload_timer >= 1:
            if self.window.is_key_pressed(KeyCode.SPACE):
                h = window.create_sprite(BlackholeBullet)
                h.custom_on_create(self)
                self.blackhole_reload_timer = 0

        elif self.bullet_type == "grenade" and self.grenade_reload_timer >= 1 : # We may need to change this later
            if self.window.is_key_pressed(KeyCode.SPACE):
                g = window.create_sprite(Grenade)
                g.custom_on_create(self)
                self.grenade_reload_timer  = 0

        elif self.bullet_type == "bullet" and self.bullet_reload_timer >= 0.3 or self.bullet_type == "lazer" and self.bullet_reload_timer >= 0.3:
            if window.is_key_pressed(KeyCode.SPACE):
                b = window.create_sprite(Bullet)
                b.custom_on_create(self,self.bullet_type)
                

                if self.bullet_type == "bullet":
                    self.bullet_reload_timer = 0
                    gunshot_sniper.play()
                if self.bullet_type == "lazer":
                    self.bullet_reload_timer = 0.3
                    laser_shot.play()
                    
        

        
            
        
        

        if window.is_key_down(KeyCode.A):
            self.bullet_type = "bullet"

        elif window.is_key_down(KeyCode.S):
            self.bullet_type = "lazer"

        elif window.is_key_down(KeyCode.D):
            self.bullet_type = "grenade"

        elif window.is_key_down(KeyCode.F):
            self.bullet_type = "blackhole"

class Bullet(Sprite):
    def on_create(self):
        self.scale = 10
        self.color = Color.RED
        self.type = ""

    def custom_on_create(self,bullet_start_sprite,bullet_type):
        self.type = bullet_type
        self.color = (255,0,0) if bullet_type == "bullet" else (0,255,255)
        self.goto(bullet_start_sprite)
        self.point_toward_mouse_cursor() # This must be after the goto command
        
    def on_update(self, dt):

            
        hit_enemy = False
        self.move_forward(15)
        if self.is_touching_window_edge():
            self.delete()
        for enemy in self.window.get_sprites_with_tag("enemy"):
            if is_aabb_collision(self, enemy):
                if self.type == "bullet":
                    enemy.receive_damage(25)
                    hit_enemy = True
                elif self.type == "lazer":
                    enemy.receive_damage(0.7)
                
        if hit_enemy:
            self.delete()

class Grenade(Sprite):

    def on_create(self):
        self.scale = 10
        self.color = Color.GREEN
        self.blow_up_timer = 0 #3 secs then blow up sits at 2 secs
        self.speed = 3

    def custom_on_create(self,bullet_start_sprite):
 
        self.goto(bullet_start_sprite)
        self.point_toward_mouse_cursor()

    def on_update(self, dt):

        if self.blow_up_timer < 1:
            
            self.move_forward(self.speed)
        elif self.blow_up_timer < 1.5:
            pass 
        else:
            window.create_sprite(Explosion, position=self.position)
            grenade_explosion.play()
            self.delete()

        if self.is_touching_any_sprite_with_tag("enemy"):
            self.speed = 0

        self.blow_up_timer += dt

class BlackholeBullet(Sprite):

    def on_create(self):
        self.scale = 10
        self.color = Color.WHITE
        self.transform_timer = 0
        self.speed = 4

    def custom_on_create(self,bullet_start_sprite):
 
        self.goto(bullet_start_sprite)
        self.point_toward_mouse_cursor()

    def on_update(self,dt):

        if self.transform_timer < 2.5:
            
            self.move_forward(self.speed)

        elif self.transform_timer < 3.5:

            pass 

        else:
            window.create_sprite(Blackhole, position=self.position, scale = 0.8)
            self.delete()

        if self.is_touching_any_sprite_with_tag("enemy"):
            self.transform_timer = 3.5

        self.transform_timer += dt

class Blackhole(Sprite):

    def on_create(self):

        self.add_tag("blackhole")
        self.image = "img/blackhole1.png"
        self.blow_up_timer = 0

    def on_update(self, dt):

        
        if self.blow_up_timer >= 5:

            e = window.create_sprite(Explosion, position=self.position)
            e.image = "img/explosion2.gif"
            e.scale = 1.05
            explosion.play()
            self.delete()

        elif self.blow_up_timer >= 3:
            self.set_random_color()

        self.blow_up_timer += dt

        
    

def goto_random_pos_on_edge(sprite):
    sprite.goto_random_position()
    edge = random.randint(1,4)
    if edge==1:
        sprite.y=0
    elif edge==2:
        sprite.y=window.height
    elif edge==3:
        sprite.x=0
    else:
        sprite.x=window.width

    


class Enemy(Sprite):
    def on_create(self):
        self.image = "img/zombie1.png"              
        goto_random_pos_on_edge(self)
        self.scale = 0.05
        self.speed = 2
        self.add_tag("enemy")
        self.health = 25
        if tower.is_deleted:
            self.point_toward_sprite(tower)
            self.move_forward(40)
            grenade_explosion.play()
            b = window.create_sprite(Explosion)
            b.goto(self)
        self.layer = 800
        self.point_toward_sprite(tower)

        

    def on_update(self, dt):

        
        self.move_forward(self.speed)

        if self.is_touching_any_sprite_with_tag("tower"):
            tower.receive_damage(5)
            self.delete()

        for blackhole in window.get_sprites_with_tag("blackhole"):
            if get_distance(self, blackhole) <= 130:
                self.point_toward_sprite(blackhole)
                self.speed = 6
                self.scale_x += 0.015



    def receive_damage(self, damage):
            self.health -= damage
            if self.health <= 0:
                self.delete()



class BigEnemy(Sprite):
    def on_create(self):
        self.image = "img/zombie2.png"
        goto_random_pos_on_edge(self)
        self.speed  = 1
        self.scale = 0.1
        self.add_tag("enemy")
        self.health = 100
        if tower.is_deleted:
            self.point_toward_sprite(tower)
            self.move_forward(40)
            grenade_explosion.play()
            b = window.create_sprite(Explosion)
            b.goto(self)
        self.layer = 800
        self.point_toward_sprite(tower)

    def on_update(self, dt):
        
        self.move_forward(self.speed)

        if self.is_touching_any_sprite_with_tag("tower"):
            tower.receive_damage(10)
            self.delete()

        for blackhole in window.get_sprites_with_tag("blackhole"):
            if get_distance(self, blackhole) <= 130:
                self.point_toward_sprite(blackhole)
                self.speed = 6
                self.scale_x -= 0.002
        
    def receive_damage(self, damage):
            self.health -= damage
            if self.health <= 0:
                self.delete()

class DemonEnemy(Sprite):
    def on_create (self):
        self.image = "img/zombie3.png"
        goto_random_pos_on_edge(self)
        self.scale = 0.1
        self.speed = 1
        self.add_tag("enemy")
        self.health = 75
        self.summon_timer = 0

        if tower.is_deleted:
            self.point_toward_sprite(tower)
            self.move_forward(40)
            grenade_explosion.play()
            b = window.create_sprite(Explosion)
            b.goto(self)
        self.point_toward_sprite(tower)
        self.layer = 800

    def on_update(self, dt):

        
        self.move_forward(self.speed)

        if self.is_touching_any_sprite_with_tag("tower"):
            tower.receive_damage(10)
            self.delete()

        if self.summon_timer >= 3.5:
            enemy_1 = window.create_sprite(Enemy, x = self.position.x + 20, y = self.position.y + 20)
            enemy_2 = window.create_sprite(Enemy, position = self.position)
            enemy_1.point_toward_sprite(tower)
            enemy_2.point_toward_sprite(tower)
            self.summon_timer = 0

        self.summon_timer += dt

        for blackhole in window.get_sprites_with_tag("blackhole"):
            if get_distance(self, blackhole) <= 130:
                self.point_toward_sprite(blackhole)
                self.speed = 6    #
                self.scale_x += 0.007
    
    def receive_damage(self, damage):
            self.health -= damage
            if self.health <= 0:
                self.delete()
tower = window.create_sprite(Tower)
sniper = window.create_sprite(Sniper)


def spawn_enemies(enemy_rate,big_rate, demon_rate):
    Scheduler.update(lambda: window.create_sprite(Enemy), enemy_rate)
    Scheduler.update(lambda: window.create_sprite(BigEnemy), big_rate)
    Scheduler.update(lambda: window.create_sprite(DemonEnemy), demon_rate)

spawn_enemies(1,3,5)

window.create_sprite(Explosion)

window.run()