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
from pycat.sound import Player as Sound


import random

window = Window(background_image="img/backgrounds/mountains_03.png")

STARTING_HP = 100
hit_aud = Sound("audio/hit.wav")
bullet_to_shield = Sound("audio/bullet_hit_shield.mp3")
# mr_hat_shot = Sound("audio/gunshot_realistic.mp3")
# mr_ray_shot = Sound("audio/laser_gunshot.mp3")

# BOSS OF THE GAME!!!
class GameManager(Sprite):
    def on_create(self):
        self.playing = False
        self.selecting_player = False
        self.background_music = Sound("audio/background_music.wav")
        self.background_music_timer = 58
    def on_update(self, dt):
        if self.background_music_timer == 58:
            self.background_music.play()
            self.background_music_timer = 0
        self.background_music_timer += dt

game_manager = window.create_sprite(GameManager)

class StartButton(Sprite):

    def on_create(self):

        self.image = "img/start1.png"

        self.x = window.center.x
        self.y = window.center.y

        self.layer = 5

    def on_left_click(self):

        game_manager.selecting_player = True

    def on_update(self,dt):

        self.is_visible = False if game_manager.playing or game_manager.selecting_player else True

window.create_sprite(StartButton)

class PlayerSelector(Sprite):
    def on_create(self):
        self.image = "img/player_selector.png"

        self.player_image = None
        self.player_scale = 1

        self.chosen_p1 = False

        self.layer = 20

        self.x = window.center.x
        self.y = window.center.y
        self.scale = 0.6

    def on_click(self,mouse):

        if self.is_visible:

            if mouse.position.x > self.x: # Right
                if mouse.position.y > self.y:
                    self.player_image = "rockman" #"img/rockman_running_right.gif"
                    self.player_scale = 0.7
                else:
                    self.player_image = "harry_the_magician"
                    self.player_scale = 0.2
            
            else:
                if mouse.position.y < self.y:
                    self.player_image = "mr_ray"
                    self.player_scale = 0.38
                else:
                    self.player_image = "mr_hat"
                    self.player_scale = 4
            if not self.chosen_p1:
                me.player_image = self.player_image  
                me.image = "img/"+me.player_image+".gif"
                me.scale = self.player_scale            
            else:
                you.player_image = self.player_image
                you.image = "img/"+you.player_image+".gif"
                you.scale = self.player_scale
            if self.chosen_p1:
                self.is_visible = False
                game_manager.playing = True
            self.chosen_p1 = True


    def on_update(self,dt):

        if game_manager.playing == True:
            self.is_visible = False
            return

        self.is_visible = False if not game_manager.selecting_player else True


player_selector = window.create_sprite(PlayerSelector)

class Warrior(Sprite):
    def on_create(self):
        self.y_velocity = 0
        self.image = None
        self.player_image = None
        self.y = 50
        self.x = window.width/2
        self.x_velocity = 0
        self.friction = 0.97
        self.rotation_mode = RotationMode.RIGHT_LEFT
        
        self.key_jump = KeyCode.W
        self.key_move_left = KeyCode.A
        self.key_move_right = KeyCode.D
        self.key_shoot = KeyCode.V
        self.key_shield = KeyCode.B

        self.shoot_count = 0
        self.bullet_max_num = 10
        self.bullet_timeout = 0
        self.reload = 400        
        self.shield_timer = 0
        self.health_point = STARTING_HP

        self.speed_boosted = False
        self.speed_boost_timer = 0

        self.resistance_boosted = False
        self.resistance_boost_timer = 0

        self.shot_sound = None
    
    def on_update(self, dt):

        if not game_manager.playing:
            self.is_visible = False
            return

        self.is_visible = True

        self.color = (255,255,255)

        if self.health_point <= 0:
            self.y -= 10
            self.rotation_mode=RotationMode.ALL_AROUND
            self.rotation += 50
            self.scale -= 0.07
            if self.y <= 0:
                self.delete()
            return

        if self.image == "img/"+self.player_image+"_shooting.gif":
            self.image = "img/"+self.player_image+".gif"

        # Gravity
        self.y_velocity -= 1
        # Friction
        self.x_velocity *= self.friction

        # Changing pos using velocity
        self.y += self.y_velocity
        self.x += self.x_velocity

        # Dying if fall into void
        if self.y <= 0:
            self.health_point = -9999999
            self.hp_label.text = "HP: "+str(self.health_point)
            self.delete()

        if self.is_touching_any_sprite_with_tag("platform") and self.y_velocity <= 0:
            while self.is_touching_any_sprite_with_tag("platform"):
                self.y += 1
            self.y_velocity = 0
            self.y -= 30

        if self.window.is_key_down(self.key_jump) and self.y_velocity == 0:
            self.y_velocity = 25

        if self.window.is_key_pressed(self.key_move_right):
            if self.speed_boosted:
                self.x_velocity += 1
            else:
                self.x_velocity += 0.5
            self.rotation = 0

        if self.window.is_key_pressed(self.key_move_left):
            if self.speed_boosted:
                self.x_velocity -= 1
            else:
                self.x_velocity -= 0.5
            self.rotation = 180
        if self.window.is_key_down(self.key_shoot) and self.shoot_count != self.bullet_max_num:
            self.shot_sound = Sound("audio/"+self.player_image+"_gunshot.mp3")
            self.shot_sound.play()
            s = window.create_sprite(Bullet,tags=["bullet"])
            s.image = "img/"+self.player_image+"_bullet.png"
            s.goto(self)
            s.rotation = self.rotation
            s.move_forward(100)
            s.y += 17
            self.image = "img/"+self.player_image+"_shooting.gif"
            self.shoot_count += 1
            
        if self.window.is_key_down(self.key_shield) and self.shield_timer <= 1:
            l = window.create_sprite(Shield,tags=["shield"])
            l.goto(self)
            l.owner = self
            self.shield_timer = 300
        if self.shield_timer > 1:
            self.shield_timer -= 1


        if self.shoot_count == self.bullet_max_num:
            self.bullet_timeout += 1 
            if self.image == "img/"+self.player_image+".gif":
                self.image = "img/"+self.player_image+"_reloading.gif"
        if self.bullet_timeout >= self.reload:
            self.shoot_count = 0
            self.bullet_timeout = 0
            self.image = "img/"+self.player_image+".gif"


        if self.is_touching_any_sprite_with_tag("bullet"):
            self.color = (70,0,0)
            hit_aud.play()
            if self.resistance_boosted:
                self.health_point -= random.randint(1,8) - 2
                # self.health_point -= 1 - 3
            else:
                self.health_point -= random.randint(1,8)
                # self.health_point -= 1
            self.hp_label.text = "HP: "+str(self.health_point)
        
        if self.speed_boosted:
            l = window.create_sprite(LightningTrail)
            l.goto(self)
            l.y -=  60
            l.x += 30 if self.rotation == 180 else -30

            self.speed_boost_timer += dt
            if self.speed_boost_timer > 10:
                self.speed_boosted = False
                self.speed_boost_timer = 0



        if self.resistance_boosted:            
            self.resistance_boost_timer += dt
            self.color = (255,255,0)
            if self.resistance_boost_timer > 15:
                self.resistance_boosted = False
                self.resistance_boost_timer = 0
                print("RESISTANCE EXHAUSTED... REMOVING... DONE!")


    
you = window.create_sprite(Warrior,x= 1100, y=550)
you.layer = 2

you.hp_label = window.create_label()
you.hp_label.x=1180
you.hp_label.y = 650




you.key_move_left = KeyCode.LEFT
you.key_move_right = KeyCode.RIGHT
you.key_shoot = KeyCode.PERIOD
you.key_jump = KeyCode.UP
you.key_shield = KeyCode.COMMA
me = window.create_sprite(Warrior, x=100, y=550) 
me.layer = 2

me.hp_label = window.create_label()
me.hp_label.text = ""


player_list = [you,me]
power_up_limit_area = (300, 700, 150, 550)

class SpeedPowerUp(Sprite):
    def on_create(self):
        self.goto_random_position()
        self.limit_position_to_area(*power_up_limit_area)
        self.image = "img/speed_boost.png"
        self.scale = 0.2
        self.timer = 0
    def on_update(self, dt):

        if not game_manager.playing:
            self.is_visible = False
            return

        self.timer += dt

        for player in player_list:
            if is_aabb_collision(self, player) and self.is_visible:
                player.speed_boosted = True
                self.is_visible = False
                self.timer = 0

        if not self.is_visible and self.timer > 10:
            self.is_visible = True
            self.goto_random_position()
            self.limit_position_to_area(*power_up_limit_area)
window.create_sprite(SpeedPowerUp)

class ResistancePowerUp(Sprite):
    def on_create(self):
        self.goto_random_position()
        self.limit_position_to_area(*power_up_limit_area)
        self.image = "img/resistance_boost1.png"
        self.scale = 0.02
        self.timer = 0
    def on_update(self, dt):

        if not game_manager.playing:
            self.is_visible = False
            return

        self.timer += dt

        for player in player_list:
            if is_aabb_collision(self, player) and self.is_visible:
                player.resistance_boosted = True
                self.is_visible = False
                self.timer = 0

        if not self.is_visible and self.timer > 20:
            self.is_visible = True
            self.goto_random_position()
            self.limit_position_to_area(*power_up_limit_area)
window.create_sprite(ResistancePowerUp)

class HealPowerUp(Sprite):
    def on_create(self):
        self.goto_random_position()
        self.limit_position_to_area(*power_up_limit_area)
        self.image = "img/pack1-platforms/HP_Bonus_01.png"
        self.scale = 0.3
        self.timer = 0
    def on_update(self, dt):

        if not game_manager.playing:
            self.is_visible = False
            return

        self.timer += dt

        for player in player_list:
            if is_aabb_collision(self, player) and self.is_visible and player.health_point > 0:
                player.health_point += 10
                self.is_visible = False
                self.timer = 0
                player.hp_label.text = "HP: "+str(player.health_point)
        if not self.is_visible and self.timer > 15:
            self.is_visible = True
            self.goto_random_position()
            self.limit_position_to_area(*power_up_limit_area)

window.create_sprite(HealPowerUp)

class LightningTrail(Sprite):
    def on_create(self):
        self.image = "img/lightning_trail.png"
        self.timer = 0
        self.scale = 0.2
    def on_update(self, dt):
        self.timer += dt
        if self.timer >= 1:
            self.delete()



class Bullet(Sprite):
    def on_create(self):
        self.rotation_mode = RotationMode.RIGHT_LEFT
        self.timer = 0
        self.image = "img/EnergyBall_Mike.gif"
        self.scale=0.3
        self.y += 15
    def on_update(self, dt):
        # Blasting forward
        self.move_forward(47.3)
        if self.timer > 0.3 or self.is_touching_window_edge() or self.is_touching_any_sprite():
            if self.is_touching_any_sprite_with_tag("shield"):
                bullet_to_shield.play()
            self.delete()
        
        self.timer += dt

class Shield(Sprite):
    def on_create(self):
        # self.owner = me
        self.image = "img/EnergyShield_Mike.gif"
        self.rotation_mode = RotationMode.RIGHT_LEFT
        self.timer = 0
        self.scale = 4
        # self.goto(self.owner)
    def on_update(self, dt):

        # Staying with player
        self.rotation = self.owner.rotation
        self.goto(self.owner)
        self.move_forward(75)

        # Deleting at a time limit
        if self.timer > 3:
            self.delete()
        self.timer += dt

        # If owner die, die
        if self.owner not in window.get_all_sprites():
            self.delete()


# HW: finish commenting your code
# HW: create an enemy
# HW: projectiles             


p1 = window.create_sprite(image='img/pack1-platforms/Pad_01_1.png',x=window.center.x, tags=["platform"])
p2 = window.create_sprite(image='img/pack1-platforms/Pad_03_1.png',x=100,y=window.center.y, tags=["platform"],scale=0.5)
p3 = window.create_sprite(image='img/pack1-platforms/Pad_03_1.png',x=1050,y=window.center.y, tags=["platform"], scale=0.5)
platlist = [p1,p2,p3]


# you2 = window.create_sprite(Warrior,x=1)
# you3 = window.create_sprite(Warrior,x=600)
window.run()