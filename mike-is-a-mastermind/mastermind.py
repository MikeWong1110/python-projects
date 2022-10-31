from pycat.core import Window, Sprite, Label, Color, KeyCode
from pycat.base.event.mouse_event import MouseEvent, MouseButton
from random import randint, choice, shuffle

clone_height_decrease=0

window=Window(enforce_window_limits=True,width=640,height=640)

color_list=[Color.BLUE , Color.RED , Color.GREEN , Color.YELLOW , Color.CYAN , Color.PURPLE , Color.AMBER]

solution=color_list
shuffle(solution)
solution=solution[:4]

peg_input=[]

class ColourChooser(Sprite):
    def on_create(self):
        self.color=Color.WHITE
        self.image='white-circle.png'
        self.scale=0.03
        self.y=30
        self.my_color_list=color_list

    def on_left_click(self):
        self.color=self.my_color_list[0]
        self.my_color_list.append(self.my_color_list[0])
        self.my_color_list=self.my_color_list[1:]

    # def on_click(self, mouse_event: MouseEvent):
    #     if mouse_event.button==MouseButton.RIGHT:
    #         self.color=self.my_color_list[-1]
    #         self.my_color_list.insert(0,self.my_color_list[-1])
    #         self.my_color_list=self.my_color_list[:1]

    def clone(self):
        my_clone=window.create_sprite(scale=self.scale)
        my_clone.image=self.image
        my_clone.goto(self)
        my_clone.color=self.color
        my_clone.y=window.height-(60*clone_height_decrease)

class CheckButton(Sprite):
    def on_create(self):
        self.color=Color.WHITE
        self.scale_y=50
        self.scale_x=100
        self.y=30
        self.x=window.width/2+240

    def on_left_click(self):
        global clone_height_decrease
        clone_height_decrease+=1
        win=True
        pegs_right=0
        pegs_wrong_position=0
        for peg in peg_input:
            
            peg.clone()
            if peg.color!=solution[peg_input.index(peg)]:
                win=False
            else:
                pegs_right+=1

            if peg.color in solution:
                pegs_wrong_position+=1
        if win:
            print("Huh, seems like you won. But are you actually a mastermind? Or a ch...")
            game_won(window)

        pegs_right_label=window.create_label()
        pegs_right_label.text=str(pegs_right)+'  '+str(pegs_wrong_position-pegs_right)
        pegs_right_label.position=(window.width/2+120,window.height-(60*clone_height_decrease)+10)
        print("Pegs right: "+str(pegs_right))

class HintButton(Sprite):
    def on_create(self):
        self.color=Color.WHITE
        self.scale_y=50
        self.scale_x=100
        self.y=30
        self.x=window.width/2-240

    def on_left_click(self):
        if randint(0,1)==0:
            #wrong hint (most of the time)
            print("wrong hint:")
            print("Peg number "+str(randint(1,4))+" is "+str(choice(color_list)))
        else:
            peg_choice=randint(1,4)
            print("right hint:")
            print("Peg number "+str(peg_choice)+" is "+str(solution[peg_choice-1]))

window.create_sprite(HintButton)
window.create_sprite(CheckButton)
print(solution)
for offset in range(-120,120,60):
    peg_input.append(window.create_sprite(ColourChooser,x=window.width/2+offset))

def game_won(window:Window):
    window.delete_all_sprites()
    window.delete_all_labels()
    window.background_image="timhowan.png"
window.run()