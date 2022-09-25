from pycat.core import Sprite, Window, Point, Color, Label
from pycat.base.event import KeyEvent
from random import randint

start_game=False
grid_width=20
grid=[]

window=Window(enforce_window_limits=True,width=700,height=700)


class TypeableLabel(Label):
    def on_create(self):
        self.text=""
        window.subscribe(on_key_press=self.on_key_press)
        self.position=Point(window.width/2,window.height/2)
        print(self.font_size)

    def on_key_press(self,key: KeyEvent):
        if not start_game:
            if key.character=="\n" or len(self.text)<2:
                self.text+=key.character

    def on_update(self, dt):
        if "\n" in self.text:
            self.text=self.text[:-1]
            if self.text.isnumeric():
            # Called after Enter key (\n) is pressed
                global grid_width
                global start_game

                grid_width=int(self.text)
                start_game=True
                for _ in range(grid_width):
                    grid.append([None]*grid_width)

                self.text=""

            else:
                self.text=""
                print("Sorry kind sir, but I'm dearly afraid I got no idea what in the world that is man like bro why cant you type something better?")

        self.position=Point(window.width/2-(6*len(self.text)),window.height/2)

class Cell(Sprite):
    def on_create(self):
        self.scale=window.width/grid_width
        self.layer=1
        self.color=Color.RED
        self.i=0
        self.j=0
        
    def on_left_click(self):
        grid[self.i+1][self.j].toggle_colour()
        grid[self.i-1][self.j].toggle_colour()
        grid[self.i][self.j+1].toggle_colour()
        grid[self.i][self.j-1].toggle_colour()
        if self.check_for_win():
            for sprite in window.get_all_sprites():
                sprite.delete()


    def toggle_colour(self):
        if self.color==Color.RED:
            self.color=Color.WHITE
        else: 
            self.color=Color.RED

    def check_for_win(self):
        for row in grid:
            for cell in row:
                if type(cell)==Cell:
                    if cell.color != Color.RED:
                        print("siuuu")
                        return False
        return True

class DummyCell(Sprite):
    def on_create(self):
        self.layer=1
        self.color=Color.PURPLE
        self.i=0
        self.j=0
        
    def on_left_click(self):
        pass

    def toggle_colour(self):
        pass

class GameStarter(Sprite):
    def on_create(self):
        self.game_started=False

    def on_update(self, dt):
        if start_game and not self.game_started:


            for i in range(grid_width):
                for j in range(grid_width):
                    if i==0 or i==grid_width-1 or j==0 or j==grid_width-1:
                        cell_to_add=window.create_sprite(DummyCell,x=i*(window.width/grid_width)+(window.width/grid_width/2),y=j*(window.width/grid_width)+(window.width/grid_width/2),scale=window.width/grid_width)
                    else:
                        cell_to_add=window.create_sprite(Cell,x=i*(window.width/grid_width)+(window.width/grid_width/2),y=j*(window.width/grid_width)+(window.width/grid_width/2),scale=window.width/grid_width)
                        cell_to_add.i=i
                        cell_to_add.j=j
                    grid[i][j]=cell_to_add

            for i in range(grid_width):
                for j in range(grid_width):
                    if randint(0,8)==8:
                        grid[i][j].on_left_click()

            self.game_started=True

game_starter=window.create_sprite(GameStarter)

window.create_label(TypeableLabel)

window.run()