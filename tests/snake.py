from random import randint
from tkinter import Tk, Canvas
from typing_extensions import Literal
from threading import Thread
from time import sleep

Direction = Literal['up', 'right', 'down', 'left']

class SnakeGame:
    def __init__(
        self,
        canvas: Canvas,
        arenaSize: int,
        snakeSpeed: int,
        wall: list[list[int]] | None = None
    ):
        self.canvas = canvas
        self.arenaSize = arenaSize
        self.snakeSpeed = snakeSpeed
        self.wall = wall

        self.isPaused = True
        self.direction: Direction = 'right'
        
        self.elements: list = []

        self.body = self.getSnakeInitialPos()
        self.food = self.getFoodRandomPos()

        self.drawArena()
        self.drawUpdate()
        
        for key in ['<Up>', 'w', '<Down>', 's', '<Left>', '<a>', '<Right>', '<d>']:
            self.canvas.bind(key, self.switchSnakeDirection)
        self.canvas.focus_set()
        
    def switchSnakeDirection(self, event):
        match event.keysym:
            case 'Up' | 'w':
                if self.direction == 'down': return
                self.direction = 'up'
            case 'Down' | 'd':
                if self.direction == 'up': return
                self.direction = 'down'
            case 'Left' | 's':
                if self.direction == 'right': return
                self.direction = 'left'
            case 'Right' | 'd':
                if self.direction == 'left': return
                self.direction = 'right'

        if self.isPaused:
            self.body = self.getSnakeInitialPos();
            self.food = self.getFoodRandomPos();
            self.isPaused = False;
            self.move();
    
    def drawArena(self):
        canvasSize = self.canvas.winfo_reqwidth()
        pixelSize = int(canvasSize / self.arenaSize)

        self.create_rectangle(0, 0, canvasSize, canvasSize, '#87D973')

        for x in range(self.arenaSize):
            for y in range(self.arenaSize):
                wallIndex = -1

                if (self.wall is not None and [x, y] in self.wall):
                    wallIndex = self.wall.index([x, y])

                color = ''

                if wallIndex != -1:
                    color = '#373737' if self.isEven(wallIndex) else '#3C3C3C'
                elif (self.isEven(x) and self.isOdd(y)) or (self.isOdd(x) and self.isEven(y)):
                    color = '#7ECE6A'
                else:
                    continue

                self.create_rectangle(x * pixelSize, y * pixelSize, pixelSize, pixelSize, color)
    
    def drawUpdate(self, prevBody: list[list[int]] | None = None, prevFood: list[int] | None = None):
        canvasSize = self.canvas.winfo_reqwidth()
        pixelSize = int(canvasSize / self.arenaSize)
        
        for element in self.elements:
            self.canvas.delete(element)

        for i, pos in enumerate(self.body):
            x, y = pos
            
            color = '#3A29A8' if self.isEven(i) else '#4430BE'          
            
            element = self.create_rectangle(x * pixelSize, y * pixelSize, pixelSize, pixelSize, color)
            self.elements.append(element)

        if self.food is not None:
            x, y = self.food
            
            element = self.create_rectangle(x * pixelSize, y * pixelSize, pixelSize, pixelSize, '#BE3049')
            self.elements.append(element)

        if not self.isPaused:
            return

        element = self.create_rectangle(0, 0, canvasSize, canvasSize, '#373737')        
        self.elements.append(element)

        isStarting = self.getSnakeInitialPos() == self.body;
        isFinalizing = len(self.body) == self.arenaSize ** 2
        
        text = ''
        
        if isStarting:
            text = 'Jogar Snake'
        elif isFinalizing:
            text = 'Parabens'
        else:
            text = f'Sua Pontucao: {self.getSnakePonctuation()}'
        
        element = self.create_text(int(canvasSize / 2), int(canvasSize / 2), text, '#fff')
        self.elements.append(element)
        
    def create_rectangle(self, x: int, y: int, w: int, h: int, color: str):
        return self.canvas.create_rectangle(x, y, x + w, y + h, fill=color, width=0)

    def create_text(self, x: int, y: int, text: str, color: str):
        return self.canvas.create_text(x, y, text=text, fill=color, font=('minecraft', 50), justify='center')

    def move(self):
        if (self.isPaused): return
        
        currentHead = self.body[-1]

        match self.direction:
            case 'up':
                self.body.append([currentHead[0], currentHead[1] - 1])
            case 'down':
                self.body.append([currentHead[0], currentHead[1] + 1])
            case 'left':
                self.body.append([currentHead[0] - 1, currentHead[1]])
            case 'right':
                self.body.append([currentHead[0] + 1, currentHead[1]])

        *body, head = self.body

        isBodyColiding = head in body
        isFoodColiding = head == self.food if self.food is not None else False
        isWallColiding = head in self.wall if self.wall is not None else False
        isArenaColiding = -1 in head or self.arenaSize in head
        isFinalizing = len(self.body) == self.arenaSize ** 2

        if isFoodColiding:
            self.food = self.getFoodRandomPos()
        elif isBodyColiding or isWallColiding or isArenaColiding or isFinalizing:
            self.isPaused = True
            self.body.pop()
        else:
            self.body.pop(0)

        if self.isPaused:
            return
        
        self.drawUpdate()

        Thread(target=self.update).start()

    def update(self):
        sleep(1 / self.snakeSpeed)    
        self.move()

    def getAvailableSpots(self):
        availableSpots: list[list[int]] = []

        for x in range(self.arenaSize):
            for y in range(self.arenaSize):
                currentPos: list[int] = [x, y]
                isInBody = currentPos in self.body
                isInColiders = currentPos in self.wall if self.wall is not None else False

                if isInBody or isInColiders:
                    continue
                availableSpots.append(currentPos)

        return availableSpots

    def getFoodRandomPos(self) -> list[int] | None:
        availableSpots = self.getAvailableSpots()
        if len(availableSpots) == 0:
            return None

        random: int = randint(0, len(availableSpots) - 1)
        return availableSpots[random]

    def getSnakeInitialPos(self) -> list[list[int]]:
        x = int(self.arenaSize / 4)
        y = int(self.arenaSize / 2)

        return [[x, y], [x + 1, y], [x + 2, y]]

    def getSnakePonctuation(self):
        return len(self.body) - len(self.getSnakeInitialPos())

    def isEven(self, value: int):
        return value % 2 == 0

    def isOdd(self, value: int):
        return value % 2 == 1

root = Tk()
canvas = Canvas(root, width=800, height=800)
canvas.pack(expand=1)

SnakeGame(canvas, 10, 10, [[0, 0], [0, 1]])

root.mainloop()
