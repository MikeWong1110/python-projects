from pycat.core import Sprite, Window, Color,Label
import random
import math

window=Window()
grid=[['','','',''],['','','',''],['','','',''],['','','','']]

score=0
score_label=window.create_label(Label)
score_label.x=40
score_label.y=window.height-window.height/4
score_label.text=str(score)
guessed_words=[]
word_list=[]

with open("words.txt","r") as f:
    for line in f.readlines():
        clean_word = line.strip("\n").upper()
        if len(clean_word)>2:
            word_list.append(clean_word)

scoresheet={
    3:1,
    4:3,
    5:5,
    6:7,
    7:9,
    8:11,
    9:13,
    10:15,
    11:17,
    12:19,
}


dice_select = [ # new version
    ['A','A','E','E','G','N'],
    ['E','L','R','T','T','Y'],
    ['A','O','O','T','T','W'],
    ['A','B','B','J','O','O'],
    ['E','H','R','T','V','W'],
    ['C','I','M','O','T','U'],
    ['D','I','S','T','T','Y'],
    ['E','I','O','S','S','T'],
    ['D','E','L','R','V','Y'],
    ['A','C','H','O','P','S'],
    ['H','I','M','N','Q','U'],
    ['E','E','I','N','S','U'],
    ['E','E','G','H','N','W'],
    ['A','F','F','K','P','S'],
    ['H','L','N','N','R','Z'],
    ['D','E','I','L','R','X'],
]
attempt=""
attempt_sprite_list=[]

class Die(Sprite):
    # def __str__(self):
    #     return self.letter
    def on_create(self):
        self.letter=""

    def on_update(self,dt):

        pass

    def on_left_click(self):
        global attempt
        if attempt=="":
            if self.color!=Color.RED:
                self.color=Color.RED
                
                attempt+=self.letter
                attempt_sprite_list.append(self)

                return

        for x in range(4):
            for y in range(4):
                if self.distance_to(grid[x][y]) <= math.sqrt(64*64*2):
                    if grid[x][y]==attempt_sprite_list[-1]:
                        if self.color!=Color.RED:
                            self.color=Color.RED
                            attempt+=self.letter
                            attempt_sprite_list.append(self)
                            return



    def setup(self):
        self.image="wood/letter_"+self.letter+".png"
        self.width=64
        self.height=64

class CheckButton(Sprite):
    def on_create(self):
        self.color=Color.GREEN
        self.scale=50
        self.scale_x=2
        self.x=500
        self.y=300

    def on_left_click(self):
        global attempt
        if attempt!="":
            if attempt in word_list and attempt not in guessed_words:
                guessed_words.append(attempt)
                global score
                score+=scoresheet[len(attempt)]
                score_label.text="SCORE: "+str(score)
                print(guessed_words)
                print(score)

            #check for the word if it is spelled right 
            attempt=""
            for x in range(4):
                for y in range(4):
                    grid[x][y].color=Color.RGB(255,255,255)

window.create_sprite(CheckButton)



for x in range(4):
    for y in range(4):
        e=window.create_sprite(Die)
        selected_list=random.choice(dice_select)
        e.letter=random.choice(selected_list)
        dice_select.remove(selected_list)
        e.setup()
        e.x=x*64+64
        e.y=y*64+200
        grid[x][y]=e

window.run()
        
