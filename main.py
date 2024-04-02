import pygame
import conf as c
import random
from pygame.math import Vector2

# initialize pygame, must be called always at start
pygame.init()

# open window
screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))

# set window title
pygame.display.set_caption("Let us play Pong!")

# used to set the frames
clock = pygame.time.Clock()

# run the game until this is true
pygame.mixer.music.load('sound/beep.wav')

# run the game until this is true
active = True

# ball pos and velocity
ball_pos = Vector2(c.BALL_START_X, c.BALL_START_Y)
ball_vel = Vector2(c.BALL_SPEED, c.BALL_SPEED)

# player bars
bar_left_pos = Vector2(c.BAR_POS, c.WINDOW_HEIGHT / 2)
bar_right_pos = Vector2(c.WINDOW_WIDTH - c.BAR_POS, c.WINDOW_HEIGHT / 2)

# create font
font1 = pygame.font.SysFont('chalkduster.ttf', 72)
rendered_font = font1.render('You Lost!', True, c.WHITE)

# ball color
ball_color = list(c.WHITE)


def handle_events(ball_color):
    # return false if game should be closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Change ball color to a random color
                ball_color[0] = random.randint(0, 255)
                ball_color[1] = random.randint(0, 255)
                ball_color[2] = random.randint(0, 255)

    # dict: containing for each key 1 if pressed, otherwise 0
    keys = pygame.key.get_pressed()
    bar_left_pos.y -= keys[pygame.K_w] * c.BAR_SPEED
    bar_left_pos.y += keys[pygame.K_s] * c.BAR_SPEED
    bar_right_pos.y -= keys[pygame.K_i] * c.BAR_SPEED
    bar_right_pos.y += keys[pygame.K_k] * c.BAR_SPEED

    return True, ball_color


def update_and_draw(ball_pos, ball_vel, bar_left_pos, bar_right_pos, ball_color):
    # draw
    ball = pygame.draw.ellipse(screen, ball_color,
                               pygame.Rect(ball_pos, (c.BALL_RADIUS, c.BALL_RADIUS)))
    player_1 = pygame.draw.rect(screen, c.WHITE,
                                pygame.Rect(bar_left_pos, (c.BAR_WIDTH, c.BAR_HEIGHT)))
    player_2 = pygame.draw.rect(screen, c.WHITE,
                                pygame.Rect(bar_right_pos, (c.BAR_WIDTH, c.BAR_HEIGHT)))

    # collision detection logic
    if player_1.colliderect(ball) or player_2.colliderect(ball):
        # play sound we loaded before from start
        pygame.mixer.music.play(0, 0)
        ball_vel.x *= -1

    # detect if ball leaves window
    if ball_pos.y > c.WINDOW_HEIGHT - c.BALL_RADIUS or ball_pos.y < 0:
        ball_vel.y *= -1

    # end game if ball enters left or right end --> freeze game
    if ball_pos.x > c.WINDOW_WIDTH - c.BALL_RADIUS or ball_pos.x < 0:
        screen.blit(rendered_font, (20, 20))
        ball_vel = Vector2(0, 0)

    ball_pos += ball_vel


# game loop
while active:
    # react to user input
    active = handle_events(ball_color)

    # draw elements and implement game logic
    update_and_draw(ball_pos, ball_vel, bar_left_pos, bar_right_pos, ball_color)

    # renew window
    pygame.display.flip()
    screen.fill(c.BLACK)

    # set frames
    clock.tick(c.FRAME_RATE)

pygame.quit()
quit()
