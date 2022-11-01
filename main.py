import os
import sys
import random
import pygame
from pygame.math import Vector2

# I do not need pygame.init() since it initializes all modules by slowing down application start up.
# I only need font.init() and mixer.init() to use fonts and apply sound effects.
pygame.font.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

class Snake:
    def __init__(self):
        # Initial upward snake direction.
        self.body = [Vector2(10, 16), Vector2(10, 17), Vector2(10, 18)]
        self.direction = Vector2(0, -1)

        # Snake properties.
        self.is_growing = False
        self.counter = 0
        self.is_hardcore = False
        self.hardcore_counter = 0

        # Graphics.
        self.head = head_up
        self.tail = tail_up
        

    def draw(self):
        self.update_head()
        self.update_tail()

        for index, vec in enumerate(self.body):
            # Snake rectangle.
            snake_body = pygame.Rect(vec.x * CELL_SIZE, vec.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # Checking snake's heading direction.
            if index == 0:
                screen.blit(self.head, snake_body)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_body)
            else:
                prev = self.body[index + 1] - vec
                _next = self.body[index - 1] - vec
                if prev.x == _next.x:
                    screen.blit(body_vertical, snake_body)
                elif prev.y == _next.y:
                    screen.blit(body_horizontal, snake_body)
                else:
                    if (prev.x == -1 and _next.y == -1) or (prev.y == -1 and _next.x == -1):
                        screen.blit(body_tl, snake_body)
                    elif (prev.x == -1 and _next.y == 1) or (prev.y == 1 and _next.x == -1):
                        screen.blit(body_bl, snake_body)
                    elif (prev.x == 1 and _next.y == -1) or (prev.y == -1 and _next.x == 1):
                        screen.blit(body_tr, snake_body)
                    elif (prev.x == 1 and _next.y == 1) or (prev.y == 1 and _next.x == 1):
                        screen.blit(body_br, snake_body)

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

    # Head graphics update function.
    def update_head(self):
        rel = self.body[1] - self.body[0]
        if rel == Vector2(1, 0):
            self.head = head_left
        elif rel == Vector2(-1, 0):
            self.head = head_right
        elif rel == Vector2(0, 1):
            self.head = head_up
        elif rel == Vector2(0, -1):
            self.head = head_down
    # Tail graphics update.
    def update_tail(self):
        rel = self.body[-2] - self.body[-1]
        if rel == Vector2(1, 0):
            self.tail = tail_left
        elif rel == Vector2(-1, 0):
            self.tail = tail_right
        elif rel == Vector2(0, 1):
            self.tail = tail_up
        elif rel == Vector2(0, -1):
            self.tail = tail_down
        


class Food:
    def __init__(self):
        self.regenerate()
    
    def draw(self):
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        # Food rectangle.
        food = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        screen.blit(self.food_img, food)
        # pygame.draw.rect(screen, RED, food)

    def regenerate(self):
        # Randomizing the x and y appearance position of the food.
        self.x = random.randint(0, CELL_AMOUNT - 1)
        self.y = random.randint(0, CELL_AMOUNT - 1)
        # Using Vector2 instead of list since vector is more readable when accesing 
        # its elements.
        self.pos = Vector2(self.x, self.y)
        # Random food creation.
        self.index = random.randint(0, len(food_imgs) - 1)
        self.food_img = food_imgs[self.index]
        self.is_eaten = False

# Declaring the grid cell size and amount of 30px and 20px respectively.
CELL_SIZE = 30
CELL_AMOUNT = 20

# WIDTH, HEIGHT = CELL_SIZE * CELL_AMOUNT, CELL_SIZE * CELL_AMOUNT

# Setting the screen size of 600x600 px.
DIMENSION = CELL_SIZE * CELL_AMOUNT
screen = pygame.display.set_mode((DIMENSION, DIMENSION))

# Declaring constant color variables and fps value.
BLACK = (0, 0, 0)
GREEN = (75, 179, 30)
DARK_GREEN = (73, 168, 32)
RED = (245, 5, 5)
FPS = 60

# Setting the caption of the window.
pygame.display.set_caption("Snake Game")

# Importing graphics and scaling down to the grid cell size.
apple_img = pygame.image.load(os.path.join("graphics", "apple.png")).convert_alpha()
apple_img = pygame.transform.scale(apple_img, (CELL_SIZE, CELL_SIZE))
banana_img = pygame.image.load(os.path.join("graphics", "banana.png")).convert_alpha()
banana_img = pygame.transform.scale(banana_img, (CELL_SIZE, CELL_SIZE))
cherry_img = pygame.image.load(os.path.join("graphics", "cherry.png")).convert_alpha()
cherry_img = pygame.transform.scale(cherry_img, (CELL_SIZE, CELL_SIZE))
grapes_img = pygame.image.load(os.path.join("graphics", "grapes.png")).convert_alpha()
grapes_img = pygame.transform.scale(grapes_img, (CELL_SIZE, CELL_SIZE))
mouse_img = pygame.image.load(os.path.join("graphics", "mouse.png")).convert_alpha()
mouse_img = pygame.transform.scale(mouse_img, (CELL_SIZE, CELL_SIZE))

food_imgs = [apple_img, banana_img, cherry_img, grapes_img, mouse_img]


head_up = pygame.image.load(os.path.join("graphics", "head_up.png")).convert_alpha()
head_up = pygame.transform.scale(head_up, (CELL_SIZE, CELL_SIZE))
head_down = pygame.image.load(os.path.join("graphics", "head_down.png")).convert_alpha()
head_down = pygame.transform.scale(head_down, (CELL_SIZE, CELL_SIZE))
head_right = pygame.image.load(os.path.join("graphics", "head_right.png")).convert_alpha()
head_right = pygame.transform.scale(head_right, (CELL_SIZE, CELL_SIZE))
head_left = pygame.image.load(os.path.join("graphics", "head_left.png")).convert_alpha()
head_left = pygame.transform.scale(head_left, (CELL_SIZE, CELL_SIZE))

tail_up = pygame.image.load(os.path.join("graphics", "tail_up.png")).convert_alpha()
tail_up = pygame.transform.scale(tail_up, (CELL_SIZE, CELL_SIZE))
tail_down = pygame.image.load(os.path.join("graphics", "tail_down.png")).convert_alpha()
tail_down = pygame.transform.scale(tail_down, (CELL_SIZE, CELL_SIZE))
tail_right = pygame.image.load(os.path.join("graphics", "tail_right.png")).convert_alpha()
tail_right = pygame.transform.scale(tail_right, (CELL_SIZE, CELL_SIZE))
tail_left = pygame.image.load(os.path.join("graphics", "tail_left.png")).convert_alpha()
tail_left = pygame.transform.scale(tail_left, (CELL_SIZE, CELL_SIZE))

body_vertical = pygame.image.load(os.path.join("graphics", "body_vertical.png")).convert_alpha()
body_vertical = pygame.transform.scale(body_vertical, (CELL_SIZE, CELL_SIZE))
body_horizontal = pygame.image.load(os.path.join("graphics", "body_horizontal.png")).convert_alpha()
body_horizontal = pygame.transform.scale(body_horizontal, (CELL_SIZE, CELL_SIZE))

body_tr = pygame.image.load(os.path.join("graphics", "body_tr.png")).convert_alpha()
body_tr = pygame.transform.scale(body_tr, (CELL_SIZE, CELL_SIZE))
body_tl = pygame.image.load(os.path.join("graphics", "body_tl.png")).convert_alpha()
body_tl = pygame.transform.scale(body_tl, (CELL_SIZE, CELL_SIZE))
body_br = pygame.image.load(os.path.join("graphics", "body_br.png")).convert_alpha()
body_br = pygame.transform.scale(body_br, (CELL_SIZE, CELL_SIZE))
body_bl = pygame.image.load(os.path.join("graphics", "body_bl.png")).convert_alpha()
body_bl = pygame.transform.scale(body_bl, (CELL_SIZE, CELL_SIZE))

# Font.
score_font = pygame.font.Font(os.path.join("fonts", "Ubuntu-Regular.ttf"), 20)
warn_font = pygame.font.Font(os.path.join("fonts", "Ubuntu-Regular.ttf"), 70)

# Sound effects.
pygame.mixer.music.load(os.path.join("audio", "bg.mp3"))
hiss_sound = pygame.mixer.Sound(os.path.join("audio", "hiss.wav"))
apple_eating_sound = pygame.mixer.Sound(os.path.join("audio", "eating.wav"))
soft_eating_sound = pygame.mixer.Sound(os.path.join("audio", "soft_eating.wav"))
burp_eating_sound = pygame.mixer.Sound(os.path.join("audio", "burp_eating.wav"))
hungry_eating_sound = pygame.mixer.Sound(os.path.join("audio", "hungry_eating.wav"))
joy_sound = pygame.mixer.Sound(os.path.join("audio", "enjoy.wav"))
laugh_sound = pygame.mixer.Sound(os.path.join("audio", "laugh.wav"))
fail_sound = pygame.mixer.Sound(os.path.join("audio", "fail.wav"))

pygame.mixer.music.set_volume(.7)
pygame.mixer.music.play(loops=-1)


# Main game function that is executed when the application is opened directly (not imported 
# by some other code).
def main():
    # Game restart function.
    def restart():
        snake.body = [Vector2(10, 16), Vector2(10, 17), Vector2(10, 18)]
        snake.direction = Vector2(0, -1)
        snake.counter = 0
        snake.is_hardcore = False
        snake.hardcore_counter = 0
        snake_speed = 100
        pygame.time.set_timer(pygame.USEREVENT, snake_speed)
        
        
    # Screen update function.
    def draw_screen():
        screen.fill(GREEN)
        prettify_grid()
        snake.draw()
        first_food.draw()
        second_food.draw()
        third_food.draw()
        
        # Fixing the bug when the food appears on the body of the snake
        # and on the other food.
        for i in snake.body[1:]:
            if i == first_food.pos:
                first_food.regenerate()
            if i == second_food.pos:
                second_food.regenerate()
            if i == third_food.pos:
                third_food.regenerate()
            if first_food.pos == second_food.pos:
                first_food.regenerate()
            if second_food.pos == third_food.pos:
                second_food.regenerate()
            if third_food.pos == first_food.pos:
                third_food.regenerate()

        display_score()
        # Display warning before the hard-core mode.
        if (snake.counter + 1) % 15 == 0 and snake.counter != 0:
            display_warning()

        pygame.display.update()
    
    # Collision checking functions.
    def check_internal(food_instance):
        if snake.body[0] == food_instance.pos:
            # Eating sound play.
            if food_instance.index == 0:
                apple_eating_sound.play()
            elif food_instance.index == 4:
                burp_eating_sound.play()
            else:
                soft_eating_sound.play()

            # Food regeneration.
            food_instance.regenerate()

            # Incresing the score value.        
            snake.counter += 1
            
            # Hard core mode checking.
            if snake.is_hardcore:
                snake.hardcore_counter += 1
            hardcore_check()

            # Eating sound play with accordance to the score.
            if snake.counter % 6 == 0:
                hungry_eating_sound.play()

            # Snake will grow every 2 times it eats the food and will keep growing until score 50.
            if snake.counter % 2 == 0 and snake.counter < 60:
                snake.grow()
            # Play joy sound every 10 points. 
            if snake.counter % 10 == 0:
                joy_sound.play()

    def check_eating():
        check_internal(first_food)
        check_internal(second_food)
        check_internal(third_food)
        

    # Check wether the snake hit itself or went out of the viewport.
    def check_fail():
        # Check if snake is out of the viewport.
        if (snake.body[0].x < 0 or snake.body[0].x >= CELL_AMOUNT) or (snake.body[0].y < 0 or snake.body[0].y >= CELL_AMOUNT):
            fail_sound.play()
            restart()
        
        # Check if snake hit itself.
        for i in snake.body[1:]:
            if snake.body[0] == i:
                fail_sound.play()
                restart()
                
    
    # Creating chess-alike grid color pattern.
    def prettify_grid():
        for i in range(CELL_AMOUNT):
            if i % 2 == 0:
                for j in range(CELL_AMOUNT):
                    if j % 2 == 0:
                        grid = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, DARK_GREEN, grid)
            else:
                for j in range(CELL_AMOUNT):
                    if j % 2 != 0:
                        grid = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, DARK_GREEN, grid)

    # Score display function.
    def display_score():
        score = "Score: " + str(snake.counter)
        x, y = CELL_SIZE + 20, CELL_SIZE
        score_surface = score_font.render(score, True, BLACK)
        score_rect = score_surface.get_rect(center = (x, y))
        screen.blit(score_surface, score_rect)

    # Warning display.
    def display_warning():
        x, y = CELL_SIZE + 20, CELL_SIZE * CELL_AMOUNT - 50
        warn_surface = warn_font.render("!", True, RED)
        warn_rect = warn_surface.get_rect(center = (x, y))
        screen.blit(warn_surface, warn_rect)
    
    # Hard-core mode.
    def hardcore_check():
        if snake.is_hardcore == False:
            # Turn on hard-core on every 15th point.
            if snake.counter % 15 == 0:
                snake.is_hardcore = True
                laugh_sound.play()
                if snake.hardcore_counter < 4:
                    snake_speed = 50
                else:
                    snake_speed = 100
                    snake.is_hardcore = False
                    snake.hardcore_counter = 0
                pygame.time.set_timer(pygame.USEREVENT, snake_speed)
        else:
            if snake.hardcore_counter < 4:
                snake_speed = 50
            else:
                snake_speed = 100
                snake.is_hardcore = False
                snake.hardcore_counter = 0
            pygame.time.set_timer(pygame.USEREVENT, snake_speed)

    first_food = Food()
    second_food = Food()
    third_food = Food()
    snake = Snake()
    clock = pygame.time.Clock()

    snake_speed = 100

    # Checking for the user input on every 100ms.
    pygame.time.set_timer(pygame.USEREVENT, snake_speed)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if  event.type == pygame.USEREVENT:
                snake.move()
                check_eating()
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

        check_fail()
        draw_screen()
        clock.tick(FPS)

# Execute main() when the application is executed directly.
# main() will not execute, if external code will import this script.
if __name__ == "__main__":
    main()
