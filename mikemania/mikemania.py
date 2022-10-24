from pycat.core import Window , Sprite, Label, Color, KeyCode 
from random import randint, uniform

#todo
#1.make a record score
#2.fix yellow
#3.mania mode?

lifecount=10

game_timer=0
score=0

window=Window()

class GameManager(Sprite):
    def on_create(self):
        self.game_time_label=window.create_label()
        self.score_label=window.create_label()
    def on_update(self,dt):
        global game_timer
        game_timer+=dt
        self.game_time_label.text=str(game_timer)
        self.score_label.text=str(score)

window.create_sprite(GameManager)
class DashingTower(Sprite):
    def on_create(self):
        self.add_tag("dasher")
        self.image='img/white-circle.png'
        self.dash_key=KeyCode.SPACE
        self.scale=0.06
        self.x=window.width/2
        self.is_dashing=False
        self.is_at_bottom=True

    def on_update(self,dt):
        if window.is_key_down(self.dash_key) and not self.is_dashing:
            global lifecount
            lifecount-=1
            self.is_dashing=True
        

        if self.is_at_bottom and self.is_dashing:
            self.y+=100
        elif self.is_dashing and not self.is_at_bottom:
            self.y-=100

        if self.is_touching_window_edge() and self.is_dashing:
            if lifecount==0:
                print("Dude, calm down with the spamming! This game takes concentration, not speed! You lived for "+str(game_timer)+" seconds.")
                window.close()
            self.is_dashing=False
            if self.is_at_bottom:
                self.is_at_bottom=False
            else:
                self.is_at_bottom=True 

class Spawner(Sprite):
    def on_create(self):
        self.image='img/white-circle.png'
        self.scale=0.05
        self.nst=randint(2,4)
        self.timer=0

    def on_update(self,dt):
        # if uniform(0.0,1.0)<=0.009:
        if self.timer >= self.nst:
            circle=window.create_sprite(Circle)
            circle.goto(self)
            circle.color=self.color
            self.timer=0
            self.nst=randint(2,4)

        
        self.timer+=dt

class Circle(Sprite):
    def on_create(self):
        self.image='img/white-circle.png'
        self.scale=0.02
        
    def on_update(self,dt):
        self.x+=3
        for dasher in window.get_sprites_with_tag('dasher'):
            if self.is_touching_sprite(dasher) and dasher.color==self.color:
                global lifecount
                global score
                lifecount+=1
                score+=1
                self.delete()
        if self.is_touching_window_edge():
            print("Oh wow! You're really bad, aren't you?\nWell anyways, you lived for "+str(game_timer)+" seconds.\nPretty accurate, huh? Thank me for that!")
            window.close()

circle=window.create_sprite(Spawner,x=80,y=560)
circle.color=Color.hex('FFCD00')
circle=window.create_sprite(Spawner,x=80,y=440)
circle.color=Color.hex('F5001D')
circle=window.create_sprite(Spawner,x=80,y=320)
circle.color=Color.hex('2DD700')
circle=window.create_sprite(Spawner,x=80,y=200)
circle.color=Color.hex('3016B0')

dash=window.create_sprite(DashingTower,x=320)
dash.color=Color.hex('FFCD00')
dash.dash_key=KeyCode.D
dash=window.create_sprite(DashingTower,x=640-100)
dash.color=Color.hex('F5001D')
dash.dash_key=KeyCode.F
dash=window.create_sprite(DashingTower,x=960-200)
dash.color=Color.hex('2DD700')
dash.dash_key=KeyCode.J
dash=window.create_sprite(DashingTower,x=1280-300)
dash.color=Color.hex('3016B0')
dash.dash_key=KeyCode.K

window.run()
        