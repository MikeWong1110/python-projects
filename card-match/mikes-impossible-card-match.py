from pycat.core import Window, Sprite, Label, Color, KeyCode, Point
from pycat.base.event import KeyEvent
import random

window=Window(enforce_window_limits=True, draw_sprite_rects=True)

clicked_cards=[]

# Getting images and cardset
card_scale=1
cardsets=[("David",1),("Dungeon",4),("Splat",0.25)]
cardset,cardset_scale=random.choice(cardsets)
card_images=["1.png","2.png","3.png","4.png","5.png"]*4
random.shuffle(card_images)

class TypeableLabel(Label):
    def on_create(self):
        self.text="some text"
        window.subscribe(on_key_press=self.on_key_press)

    def on_key_press(self,key: KeyEvent):
        print(type(key))
        self.text+=key.character

class CardParticleSystem():
    def __init__(self):
        pass

class Card(Sprite):
    def on_create(self):
        # self.image="card-images/"+card_images[0]
        self.opacity=0
        self.should_delete=False

    def on_left_click(self):
        
        global clicked_cards
        if len(clicked_cards)<2 and self not in clicked_cards:
            clicked_cards.append(self)
            self.opacity=255

    def on_update(self, dt):
        if self.should_delete:
            self.move_forward(30)
            if self.scale>=0:
                self.scale-=0.02

        if self.is_touching_window_edge():
            self.delete()

    def delete_card(self):
        self.should_delete=True
        self.rotation=random.randint(0,360)

        # Alternate way to do this
        # point_to_dot=window.create_sprite()
        # point_to_dot.goto_random_position()
        # self.point_toward_sprite(point_to_dot)
        # point_to_dot.delete()

class CheckButton(Sprite):

    def on_create(self):

        self.check_label=window.create_label(text="CHECK :D",color=Color.BLACK)
        self.check_label.layer=1000
        self.scale_x=100
        self.scale_y=50

    def on_update(self, dt):

        if window.is_key_down(KeyCode.Z):
            self.on_left_click()

        self.check_label.position=Point(x=self.position.x-self.check_label.content_width/2,y=self.position.y-self.check_label.content_height/2)

    def on_left_click(self):

        global clicked_cards
        if len(clicked_cards)==2:

            if clicked_cards[0].image == clicked_cards[1].image:

                for card in clicked_cards:
                    card.delete_card()

            else: 

                for card in clicked_cards:
                    card.opacity=0
            
            clicked_cards=[]



window.create_sprite(CheckButton,x=640,y=320)

for x in range(100,600,100):
    for y in range(100,500,100):
        if len(card_images):
            image=card_images.pop()
        window.create_sprite(Card,x=x,y=y,image="card-images/"+cardset+"/"+image,scale=cardset_scale)

window.create_label(TypeableLabel)

window.run()