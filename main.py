import pygame
import os
pygame.font.init()  # for font of text
pygame.mixer.init()  # for sound effects

WIDTH, HEIGHT = 900, 500  # size of screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # starts the window
pygame.display.set_caption("Balls")  # title

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# draw a rectangle on the screen as a border.
# pygame.rect(x (start of x value), y (start of y value),
# width (end of x value), height (end of y value))
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
# BULLET_FIRE_SOUND = pygame.mixer.Sound(
#     os.path.join('Assets', 'Gun+Silencer1.mp3'))

HEALTH_FONT = pygame.font.SysFont('timesnewroman', 40)  # font for health bar
WINNER_FONT = pygame.font.SysFont('timesnewroman', 100)  # font for who won

FPS = 60  # fps of game
VEL = 5  # speed at which each key moves the spaceships
BULLET_VEL = 7  # speed at which the bullets move
MAX_BULLETS = 3  # max amount of bullets on screen
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1  # create a new event where yellow is hit
RED_HIT = pygame.USEREVENT + 2  # create a new event where red is hit

# Imports the yellow spaceship image and then scales it down and rotates it
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join
                                           ('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# Imports the red spaceship image and then scales it down and rotates it
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join
                                        ('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Imports the background space image and resizes it to size of the screen
SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets,
                red_health, yellow_health):
    """Draws on the window. Things are drawn depending on the order written."""
    # WIN.fill(WHITE)  # color of window
    # WIN.blit puts things onto screen
    WIN.blit(SPACE, (0, 0))  # draws background image
    pygame.draw.rect(WIN, BLACK, BORDER)  # draws rectangle on screen

    red_health_text = HEALTH_FONT.render("Health: "
                                         + str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: "
                                            + str(yellow_health), True, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # 0,0 is top left of screen
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:  # draws red bullets
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:  # draws yellow bullets
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    """moves yellow spaceship with wasd"""
    if keys_pressed[pygame.K_a] and \
            yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and \
            yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and \
            yellow.y + VEL + yellow.height < HEIGHT - 10:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    """moves red spaceship with arrow keys"""
    if keys_pressed[pygame.K_LEFT] and \
            red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and \
            red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and \
            red.y + VEL + red.height < HEIGHT - 10:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    """shows where bullet is when shot and also checks if it collides with
    the enemy spaceship"""
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):  # checks if bullet collided with red
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:  # gets rid of bullet when on the right end
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):  # checks if bullet collided with yellow
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:  # gets rid of bullet when on the left end
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    # draws the winner text right in the middle of the screen
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2,
                         HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)  # pause for 5 seconds


def main():
    """main code"""
    # keeps location of each spaceship so we can change it
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:  # running the game
        clock.tick(FPS)  # controls how fast the while loop runs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # when we hit the close button
                pygame.quit()  # quit game

            if event.type == pygame.KEYDOWN:
                # if button is pressed and we don't have max bullets
                if event.key == pygame.K_LCTRL and \
                        len(yellow_bullets) < MAX_BULLETS:
                    # makes the bullet and puts it at the yellow spaceship
                    # with the width and height of the bullet being (10, 5)
                    bullet = pygame.Rect(yellow.x + yellow.width,
                                         yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()  # plays sound when firing

                if event.key == pygame.K_RCTRL and \
                        len(red_bullets) < MAX_BULLETS:
                    # makes the bullet and puts it at the red spaceship
                    # with the width and height of the bullet being (10, 5)
                    bullet = pygame.Rect(red.x, red.y +
                                         red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()  # plays sound when firing

            if event.type == RED_HIT:
                red_health -= 1
                # BULLET_HIT_SOUND.play()  # plays sound when ship is hit

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                # BULLET_HIT_SOUND.play()  # plays sound when ship is hit

        # win condition
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"

        if yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # tells us what keys are being pressed
        keys_pressed = pygame.key.get_pressed()
        # calls functions to move yellow
        yellow_handle_movement(keys_pressed, yellow)
        # calls functions to move red
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
