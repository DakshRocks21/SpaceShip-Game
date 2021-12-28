import pygame
import os

pygame.font.init()

#######################
### GAME SETTINGS
#######################
WIDTH, HEIGHT = 900, 500
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")
BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

## PLAYERS
SPEED = 10

## BULLET
BULLET_SPEED = 10
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
MAX_BULLETS = 3
HEALTH = 10

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#######################
### BACKGROUND
#######################
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space.png")), (WIDTH, HEIGHT))

#######################
### SPACESHIPS
#######################
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),270)

#######################
### COLOURS
#######################
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#######################
### WINDOWS
#######################
    
def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER) #BORDER
    
    yellow_health_text = HEALTH_FONT.render(f"Health : {yellow_health}", 1, WHITE)
    red_health_text = HEALTH_FONT.render(f"Health : {red_health}", 1, WHITE)
    
    WIN.blit(yellow_health_text, (10,10))
    WIN.blit(red_health_text, (WIDTH-red_health_text.get_width()-10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2-draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
#######################
### MOVEMENT
#######################
padding_bottom = 15 
def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - SPEED > 0: # LEFT
        yellow.x -= SPEED
    if key_pressed[pygame.K_d] and yellow.x - SPEED + yellow.width < BORDER.x: # RIGHT
        yellow.x += SPEED
    if key_pressed[pygame.K_w] and yellow.y - SPEED > 0: # UP
        yellow.y -= SPEED
    if key_pressed[pygame.K_s] and yellow.y - SPEED + yellow.height < HEIGHT - padding_bottom: # DOWN
        yellow.y += SPEED

def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - SPEED > BORDER.x + BORDER.width: # LEFT
        red.x -= SPEED
    if key_pressed[pygame.K_RIGHT] and red.x - SPEED + red.width < WIDTH: # RIGHT
        red.x += SPEED
    if key_pressed[pygame.K_UP] and red.y - SPEED > 0: # UP
        red.y -= SPEED
    if key_pressed[pygame.K_DOWN] and red.y - SPEED + red.height < HEIGHT - padding_bottom: # DOWN
        red.y += SPEED

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    yellow = pygame.Rect(100, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = []
    red_bullets = []

    yellow_health = HEALTH
    red_health = HEALTH

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - BULLET_HEIGHT/2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height/2 - BULLET_HEIGHT//2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)


            if event.type == YELLOW_HIT:
                yellow_health -= 1
            if event.type == RED_HIT:
                red_health -= 1
        winner_text = ""
        if yellow_health <= 0:
            winner_text = "RED WIN!!"
        if red_health <= 0:
            winner_text = "YELLOW WIN!!"

        if winner_text != "":
            draw_winner(winner_text)
            run = False


        key_pressed = pygame.key.get_pressed()
        
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
        pygame.display.update()

    main()


if __name__ == "__main__":
    main()
