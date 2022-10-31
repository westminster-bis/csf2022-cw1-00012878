import sys
import random
import pygame
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.is_growing = False
        self.counter = 0

    def draw(self):
        for vec in self.body:
            snake_body = pygame.Rect(vec.x * CELL_SIZE, vec.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, snake_body)

    def move(self):
        if self.is_growing:
            snake_body = self.body[:]
            snake_body.insert(0, snake_body[0] + self.direction)
            self.body = snake_body[:]
            self.is_growing = False
        else:
            snake_body = self.body[:-1]
            snake_body.insert(0, snake_body[0] + self.direction)
            self.body = snake_body[:]

    def grow(self):
        self.is_growing = True


class Food:
    def __init__(self):
        self.regenerate()
    
    def draw(self):
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        food = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food)

    def regenerate(self):
        # Randomizing the x and y appearance position of the food.
        self.x = random.randint(0, CELL_AMOUNT - 1)
        self.y = random.randint(0, CELL_AMOUNT - 1)
        # Using Vector2 instead of list since vector is more readable when accesing 
        # its elements.
        self.pos = Vector2(self.x, self.y)

# Declaring the grid cell size and amount of 30px and 20px respectively.
CELL_SIZE = 30
CELL_AMOUNT = 20

# WIDTH, HEIGHT = CELL_SIZE * CELL_AMOUNT, CELL_SIZE * CELL_AMOUNT

# Setting the screen size of 600x600 px.
DIMENSION = CELL_SIZE * CELL_AMOUNT
screen = pygame.display.set_mode((DIMENSION, DIMENSION))

# Declaring constant color variables and fps value.
WHITE = (255, 255, 255)
GREEN = (86, 199, 123)
RED = (199, 40, 40)
FPS = 60

# Setting the caption of the window.
pygame.display.set_caption("Snake Game")

# Main game function that is executed when the application is opened directly (not imported 
# by some other code).
def main():
    # Screen update function.
    def draw_screen():
        screen.fill(GREEN)
        food.draw()
        snake.draw()
        pygame.display.update()
    
    # Collision checking function.
    def check_collision():
        if (snake.body[0] == food.pos):
            food.regenerate()
            snake.counter += 1
            # Snake will grow every 3 times it eats the food.
            if snake.counter > 3:
                snake.counter = 0
                snake.grow()

    # Check wether the snake hit itself or went out of the viewport.
    def check_fail():
        # Check if snake is out of the viewport.
        if (snake.body[0].x < 0 or snake.body[0].x >= CELL_AMOUNT) or (snake.body[0].y < 0 or snake.body[0].y >= CELL_AMOUNT):
            pygame.quit()
            sys.exit()
        
        # Check if snake hit itself.
        for i in snake.body[1:]:
            if snake.body[0] == i:
                pygame.quit()
                sys.exit()

    food = Food()
    snake = Snake()
    clock = pygame.time.Clock()

    # Checking for the user input on every 100ms.
    pygame.time.set_timer(pygame.USEREVENT, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if  event.type == pygame.USEREVENT:
                snake.move()
                check_collision()
                check_fail()
            # Checking for the user input.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if (snake.direction != Vector2(0, 1)):
                        snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN:
                    if (snake.direction != Vector2(0, -1)):
                        snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_RIGHT:
                    if (snake.direction != Vector2(-1, 0)):
                        snake.direction = Vector2(1, 0)
                elif event.key == pygame.K_LEFT:
                    if (snake.direction != Vector2(1, 0)):
                        snake.direction = Vector2(-1, 0) 
        draw_screen()
        clock.tick(FPS)

# Execute main() when the application is executed directly.
# main() will not execute, if external code will import this script.
if __name__ == "__main__":
    main()
