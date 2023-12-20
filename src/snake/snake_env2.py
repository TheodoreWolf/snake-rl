import turtle
import random
import time
import math

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from gymnasium.utils import seeding

SIZE = 20
PIXEL_SCALE = 20

HEIGHT = SIZE     # number of steps vertically from wall to wall of screen
WIDTH = SIZE       # number of steps horizontally from wall to wall of screen
PIXEL_H = PIXEL_SCALE*HEIGHT  # pixel height + border on both sides
PIXEL_W = PIXEL_SCALE*WIDTH   # pixel width + border on both sides

SLEEP = 0.1     # time to wait between steps

GAME_TITLE = 'Snake'
BG_COLOR = 'white'

SNAKE_SHAPE = 'square'
SNAKE_COLOR = 'green'
SNAKE_START_LOC_H = 0
SNAKE_START_LOC_V = 0

APPLE_SHAPE = 'circle'
APPLE_COLOR = 'red'

class Snake(gym.Env):

    def __init__(self, human=False, env_info={'state_space':None}):
        super(Snake, self).__init__()

        self.done = False
        self.seed()
        self.reward = 0
        self.action_space = spaces.Discrete(4)
        self.grid = np.zeros((HEIGHT+1, WIDTH+1))
        self.observation_space = spaces.Box(self.grid, self.grid+4)

        self.total, self.maximum = 0, 0
        self.human = human

        ## GAME CREATION WITH TURTLE (RENDER?)
        # screen/background
        self.win = turtle.Screen()
        self.win.title(GAME_TITLE)
        self.win.bgcolor(BG_COLOR)
        self.win.tracer(0)
        self.win.setup(width=PIXEL_W+32, height=PIXEL_H+32)

        # apple
        self.apple = turtle.Turtle()
        self.apple.speed(0)
        self.apple.shape(APPLE_SHAPE)
        self.apple.color(APPLE_COLOR)
        self.apple.penup()

        # snake
        self.snake = turtle.Turtle()
        self.snake.shape(SNAKE_SHAPE)
        self.snake.speed(0)
        self.snake.penup()
        self.snake.color(SNAKE_COLOR)
        self.snake_body = []
        self.reset()

        # score
        self.score = turtle.Turtle()
        self.score.speed(0)
        self.score.color('black')
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 100)
        self.score.write(f"Total: {self.total}   Highest: {self.maximum}", align='center', font=('Courier', 18, 'normal'))

        # control
        self.win.listen()
        self.win.onkey(self.go_up, 'Up')
        self.win.onkey(self.go_right, 'Right')
        self.win.onkey(self.go_down, 'Down')
        self.win.onkey(self.go_left, 'Left')
        self.win.onkey(self.bye, 'q')

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def random_coordinates(self):
        apple_x = random.randint(-WIDTH/2, WIDTH/2)
        apple_y = random.randint(-HEIGHT/2, HEIGHT/2)
        return apple_x, apple_y
    
    def move_snake(self):
        if self.snake.direction == 'stop':
            self.reward = 0
        if self.snake.direction == 'up':
            y = self.snake.ycor()
            self.snake.sety(y + PIXEL_SCALE)
        if self.snake.direction == 'right':
            x = self.snake.xcor()
            self.snake.setx(x + PIXEL_SCALE)
        if self.snake.direction == 'down':
            y = self.snake.ycor()
            self.snake.sety(y - PIXEL_SCALE)
        if self.snake.direction == 'left':
            x = self.snake.xcor()
            self.snake.setx(x - PIXEL_SCALE)
        
    
    def go_up(self):
        if self.snake.direction != "down":
            self.snake.direction = "up"
    
    
    def go_down(self):
        if self.snake.direction != "up":
            self.snake.direction = "down"
    
    
    def go_right(self):
        if self.snake.direction != "left":
            self.snake.direction = "right"
    
    
    def go_left(self):
        if self.snake.direction != "right":
            self.snake.direction = "left"


    def move_apple(self, first=False):
        if first or self.snake.distance(self.apple) < PIXEL_SCALE:    
            while True:
                self.apple.x, self.apple.y = self.random_coordinates()
                self.apple.goto(round(self.apple.x*PIXEL_SCALE), round(self.apple.y*PIXEL_SCALE))
                if not self.body_check_apple():
                    break
            if not first:
                self.update_score()
                self.add_to_body()
            first = False
            return True


    def update_score(self):
        self.total += 1
        if self.total >= self.maximum:
            self.maximum = self.total
        self.score.clear()
        self.score.write(f"Total: {self.total}   Highest: {self.maximum}", align='center', font=('Courier', 18, 'normal'))


    def reset_score(self):
        self.score.clear()
        self.total = 0
        self.score.write(f"Total: {self.total}   Highest: {self.maximum}", align='center', font=('Courier', 18, 'normal'))
                    

    def add_to_body(self):
        body = turtle.Turtle()
        body.speed(0)
        body.shape(SNAKE_SHAPE)
        body.color(SNAKE_COLOR)
        body.penup()
        self.snake_body.append(body)
        

    def move_snakebody(self):
        if len(self.snake_body) > 0:
            for index in range(len(self.snake_body)-1, 0, -1):
                x = self.snake_body[index-1].xcor()
                y = self.snake_body[index-1].ycor()
                self.snake_body[index].goto(x, y)

            self.snake_body[0].goto(self.snake.xcor(), self.snake.ycor())
        

    def body_check_snake(self):
        if len(self.snake_body) > 1:
            for body in self.snake_body[1:]:
                if body.distance(self.snake) < PIXEL_SCALE:
                    self.reset_score()
                    return True

    def body_check_apple(self):
        if len(self.snake_body) > 0:
            for body in self.snake_body[:]:
                if body.distance(self.apple) < PIXEL_SCALE:
                    return True

    def wall_check(self):
        if self.snake.xcor() > PIXEL_W/2  or self.snake.xcor() < -PIXEL_W/2 or self.snake.ycor() > PIXEL_H/2 or self.snake.ycor() < -PIXEL_H/2:
            self.reset_score()
            return True
    
    def reset(self, seed=None, options=None):
        if self.human:
            time.sleep(1)
        for body in self.snake_body:
            body.goto(1000, 1000)

        self.snake_body = []
        self.add_to_body()
        self.snake.goto(SNAKE_START_LOC_H, SNAKE_START_LOC_V)
        self.snake.direction = 'stop'
        self.reward = 0
        self.total = 0
        self.move_apple(first=True)
        self.done = False

        state = self.get_state()

        return state, {}


    def run_game(self):
        self.win.update()
        self.move_snake()
        if self.move_apple():
            self.reward = 1
        self.move_snakebody()
        if self.body_check_snake():
            self.reward = 0
            self.done = True
            if self.human:
                self.reset()
        if self.wall_check():
            self.reward = 0
            self.done = True
            if self.human:
                self.reset()
        # time.sleep(0.1)
        if self.human:
            time.sleep(SLEEP)

    
    # AI agent
    def step(self, action):
        if action == 0:
            self.go_up()
        if action == 1:
            self.go_right()
        if action == 2:
            self.go_down()
        if action == 3:
            self.go_left()
        self.run_game()
        state = self.get_state()
        return state, self.reward, self.done, False, {}


    def get_state(self):
        # reset grid
        self.grid = np.zeros((HEIGHT+1, WIDTH+1))
        # snake body
        for body in self.snake_body[1:]:
            x, y = int(body.xcor()/PIXEL_SCALE + WIDTH/2), int(body.ycor()/PIXEL_SCALE + HEIGHT/2)
            self.grid[y, x] = 2
        # snake head
        if not self.done:
            self.snake.x, self.snake.y = int(self.snake.xcor()/PIXEL_SCALE+ WIDTH/2), int(self.snake.ycor()/PIXEL_SCALE + HEIGHT/2)
        self.grid[self.snake.y, self.snake.x] = 3
        
        # apple
        self.apple.x, self.apple.y = self.apple.xcor()/PIXEL_SCALE + WIDTH/2, self.apple.ycor()/PIXEL_SCALE + HEIGHT/2
        self.grid[int(self.apple.y), int(self.apple.x)] = 1 
        return self.grid

    def bye(self):
        self.win.bye()



if __name__ == '__main__':            
    human = True
    env = Snake(human=human)

    if human:
        while True:
            env.run_game()

    

    



    