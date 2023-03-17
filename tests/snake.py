from tkinter import Tk, Canvas, Event
from random import choice
from typing_extensions import Literal

# Types
Pos = list[int]
Direction = Literal['up', 'right', 'down', 'left']

# Globals
CANVAS_SIZE = 800
GRID_SIZE = 17

PIXEL_SIZE = int(CANVAS_SIZE / GRID_SIZE)

SNAKE_COLORS = ['#3A29A8', '#4430BE']
BG_COLORS = ['#7ECE6A', '#87D973']
FOOD_COLOR = '#BE3049'
MESSAGE_BG_COLOR = '#373737'

SPEED = 100

FONT_CONFIG = ('Minecraft', 50)

# Classes
class Snake:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        
        self.coords: list[Pos] = []
        self.rectangles: list = []
        
        self.direction: Direction = 'right'
        self.score = 0
        self.color_index = 0
        
        self.reset()

    def reset(self):
        self.canvas.delete('snake')
        
        self.coords.clear()
        self.rectangles.clear()
        
        self.direction = 'right'
        self.score = 0
        self.color_index = 0
        
        for pos in self.getInitialPos():
            self.add_coord(pos)

    def create_rectangle(self, pos: Pos):
        fill = SNAKE_COLORS[self.color_index]
        
        self.color_index = 1 if self.color_index == 0 else 0
        
        rectangle = self.canvas.create_rectangle(
            pos[0] * PIXEL_SIZE, 
            pos[1] * PIXEL_SIZE, 
            (pos[0] + 1) * PIXEL_SIZE, 
            (pos[1] + 1) * PIXEL_SIZE, 
            fill=fill,
            width=0,
            tags='snake'
        )
        
        self.rectangles.append(rectangle)

    def add_coord(self, pos: Pos):
        self.coords.append(pos)
        
        self.create_rectangle(pos)
    
    def remove_coord(self):
        self.coords.pop(0)
        
        rectangle = self.rectangles.pop(0)
        self.canvas.delete(rectangle)
    
    def getInitialPos(self) -> list[Pos]:
        x = int(GRID_SIZE / 4)
        y = int(GRID_SIZE / 2)
        
        return [[x, y], [x + 1, y], [x + 2, y]]

    def change_direction(self, direction: Direction):
        match direction:
            case 'up':
                if self.direction != 'down':
                    self.direction = 'up'
            case 'right':
                if self.direction != 'left':
                    self.direction = 'right'
            case 'down':
                if self.direction != 'up':
                    self.direction = 'down'
            case 'left':
                if self.direction != 'right':
                    self.direction = 'left'

class Food:
    def __init__(self, game, canvas: Canvas):
        self.canvas = canvas
        self.game = game
        
        self.coord = self.move_coord()
    
    def move_coord(self):
        self.canvas.delete('food')
        
        coord = self.getRandomPos()
        
        if coord is not None:
            self.create_rectangle(coord)
        
        return coord
    
    def create_rectangle(self, pos: Pos):
        self.canvas.create_rectangle(
            pos[0] * PIXEL_SIZE, 
            pos[1] * PIXEL_SIZE, 
            (pos[0] + 1) * PIXEL_SIZE, 
            (pos[1] + 1) * PIXEL_SIZE, 
            fill=FOOD_COLOR,
            width=0,
            tags='food'
        )        
    
    def getRandomPos(self):
        availableSpots: list[Pos] = self.game.getAvailableSpots()
        
        if len(availableSpots) == 0:
            return None
        
        return choice(availableSpots)

class Game:
    def __init__(self, win: Tk, canvas: Canvas):
        self.canvas = canvas
        
        self.is_paused = True
        
        self.create_bg()
        
        self.snake = Snake(canvas)
        self.food = Food(self, canvas)
        
        self.create_message('Jogar Snake')
        self.listen_keys(win)
        
        # self.move()
    
    def listen_keys(self, win: Tk):    
        for key in ['<Up>', '<Right>', '<Down>', '<Left>', 'w', 'd', 's', 'a']:
            win.bind(key, self.key_event)
    
    def get_key_direction(self, key: str) -> Direction:
        match(key):
            case 'Up' | 'w':
                return 'up'
            case 'Right' | 'd':
                return 'right'
            case 'Down' | 's':
                return 'down'
            case 'Left' | 'a':
                return 'left'
            case _:
                return 'right'
    
    def key_event(self, event: Event):
        key = event.keysym
        self.snake.change_direction(self.get_key_direction(key))
        
        if self.is_paused: self.start()
    
    def start(self):
        self.is_paused = False
        
        self.remove_message()
        
        self.move()
        
    def game_over(self):
        self.is_paused = True
        
        score = self.snake.score
        
        self.snake.reset()
        
        self.create_message(f'Pontuacao: {score}')
    
    def finished(self):
        self.is_paused = True
        
        self.snake.reset()
        
        self.create_message('Parabens!')
    
    def move(self):
        snakePos = self.snake.coords[-1][:]
        
        if (self.snake.direction == 'up'):
            snakePos[1] -= 1
        elif (self.snake.direction == 'down'):
            snakePos[1] += 1
        elif (self.snake.direction == 'left'):
            snakePos[0] -= 1
        elif (self.snake.direction == 'right'):
            snakePos[0] += 1
        
        self.snake.add_coord(snakePos)
        
        isBodyColiding = snakePos in self.snake.coords[:-1]
        isWallColiding = -1 in snakePos or GRID_SIZE in snakePos
        
        if snakePos == self.food.coord:
            self.food.coord = self.food.move_coord()
            self.snake.score += 1
        elif isBodyColiding or isWallColiding: 
            return self.game_over()
        elif len(self.snake.coords) == GRID_SIZE ** 2:
            return self.finished()
        else:
            self.snake.remove_coord()
            
        self.canvas.after(SPEED, self.move)
    
    def getAvailableSpots(self):
        availableSpots: list[Pos] = []

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                pos = [x, y]
                
                if pos in self.snake.coords:
                    continue
                
                availableSpots.append(pos)

        return availableSpots
        
    def create_bg(self):
        self.canvas.create_rectangle(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill=BG_COLORS[0], width=0)
        
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if not ((x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0)):
                    continue
                
                self.canvas.create_rectangle(
                    x * PIXEL_SIZE,
                    y * PIXEL_SIZE, 
                    (x + 1) * PIXEL_SIZE,
                    (y + 1) * PIXEL_SIZE,
                    fill=BG_COLORS[1], 
                    width=0
                )
    def create_message(self, text: str):
        self.canvas.create_rectangle(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill=MESSAGE_BG_COLOR, width=0, tags='message')
        
        self.canvas.create_text(
            CANVAS_SIZE / 2,
            CANVAS_SIZE / 2,
            text=text,
            font=FONT_CONFIG,
            fill='white',
            tags='message'
        )
    
    def remove_message(self):
        self.canvas.delete('message')
        
class Main:
    def __init__(self):
        win = Tk()
        win.title('Snake Game')

        canvas = Canvas(win, width=CANVAS_SIZE, height=CANVAS_SIZE)
        canvas.pack(expand=1)
        
        self.center_win(win)
        
        Game(win, canvas)
        
        win.mainloop()
    
    def center_win(self, win):
        win.update()
        
        win_width = win.winfo_width()
        win_height = win.winfo_height()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        
        win_x = int((screen_width - win_width) / 2)
        win_y = int((screen_height - win_height) / 2)
        
        win.geometry(f'{win_width}x{win_height}+{win_x}+{win_y}')
        
Main()