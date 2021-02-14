import pygame
import os
import random
pygame.font.init()  # for font of text
pygame.mixer.init()  # for sound effects

WIDTH, HEIGHT = 900, 500  # size of screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # starts the window
pygame.display.set_caption("Zombie Shooter")  # title

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# draw a rectangle on the screen as a border.
# pygame.rect(x (start of x value), y (start of y value),
# width (end of x value), height (end of y value))
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'oo.wav'))
BULLET_HIT_SOUND1 = pygame.mixer.Sound(os.path.join('Assets', 'aa.wav'))
WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'victory.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('sansserif', 40)  # font for health bar
WINNER_FONT = pygame.font.SysFont('sansserif', 100)  # font for who won

FPS = 60  # fps of game
VEL = 5  # speed at which each key moves the spaceships
BULLET_VEL = 7  # speed at which the bullets move
MAX_BULLETS = 2  # max amount of bullets on screen
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1  # create a new event where yellow is hit
RED_HIT = pygame.USEREVENT + 2  # create a new event where red is hit
ZOMBIE_HIT1, ZOMBIE_HIT2, ZOMBIE_HIT3, ZOMBIE_HIT4, ZOMBIE_HIT5 = \
    pygame.USEREVENT + 3, pygame.USEREVENT + 4, pygame.USEREVENT + 5,\
    pygame.USEREVENT + 6, pygame.USEREVENT + 7
ZOMBIE_HITS = [ZOMBIE_HIT1, ZOMBIE_HIT2, ZOMBIE_HIT3,
               ZOMBIE_HIT4, ZOMBIE_HIT5]

ZOMBIE_HIT6, ZOMBIE_HIT7, ZOMBIE_HIT8, ZOMBIE_HIT9, ZOMBIE_HIT10 = \
    pygame.USEREVENT + 8, pygame.USEREVENT + 9, pygame.USEREVENT + 10, \
    pygame.USEREVENT + 11, pygame.USEREVENT + 12
ZOMBIE_HITS2 = [ZOMBIE_HIT6, ZOMBIE_HIT7, ZOMBIE_HIT8,
                ZOMBIE_HIT9, ZOMBIE_HIT10]

# Imports the yellow spaceship image and then scales it down and rotates it
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join
                                           ('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                                          (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Imports the red spaceship image and then scales it down and rotates it
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join
                                        ('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE,
                                       (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

ZOMBIE_1 = pygame.transform.rotate(pygame.image.load(
    os.path.join('Assets', 'zombie.png')), 180)
ZOMBIE = pygame.transform.scale(ZOMBIE_1, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

ZOMBIE_2 = pygame.transform.rotate(pygame.image.load(
    os.path.join('Assets', 'zombie2.png')), 180)
ZOMBIE2 = pygame.transform.scale(ZOMBIE_2, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

ZOMBIE_3 = pygame.transform.rotate(pygame.image.load(
    os.path.join('Assets', 'zombie3.png')), 180)
ZOMBIE3 = pygame.transform.scale(ZOMBIE_3, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Imports the background grass image and resizes it to size of the screen
GRASS = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'grass.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets,
                red_health, yellow_health, zombie_list, zombie_list2):
    """Draws on the window. Things are drawn depending on the order written."""
    # WIN.fill(WHITE)  # color of window
    # WIN.blit puts things onto screen
    WIN.blit(GRASS, (0, 0))  # draws background image
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
    for sublist in zombie_list:
        if sublist[0] < 45:
            WIN.blit(ZOMBIE2, (sublist[1].x, sublist[1].y))
        elif sublist[0] == 65:
            WIN.blit(ZOMBIE3, (sublist[1].x, sublist[1].y))
        else:
            WIN.blit(ZOMBIE, (sublist[1].x, sublist[1].y))
    for sublist in zombie_list2:
        if sublist[0] < 45:
            WIN.blit(ZOMBIE2, (sublist[1].x, sublist[1].y))
        elif sublist[0] == 65:
            WIN.blit(ZOMBIE3, (sublist[1].x, sublist[1].y))
        else:
            WIN.blit(ZOMBIE, (sublist[1].x, sublist[1].y))
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


def handle_bullets(yellow_bullets, red_bullets, zombie_list,
                   zombie_list2, yellow, red):
    """shows where bullet is when shot and also checks if it collides with
    the enemy spaceship"""
    for bullet in yellow_bullets:
        bullet.y -= BULLET_VEL
        count = 0
        for sublist in zombie_list:
            # checks if bullet collides zombies
            if sublist[1].colliderect(bullet):
                pygame.event.post(pygame.event.Event(ZOMBIE_HITS[count]))
                yellow_bullets.remove(bullet)
                break
            elif bullet.y < 0:  # gets rid of bullet when it hits the top
                yellow_bullets.remove(bullet)
                break
            count += 1

    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        count = 0
        for sublist in zombie_list2:
            # checks if bullet collides zombies
            if sublist[1].colliderect(bullet):
                pygame.event.post(pygame.event.Event(ZOMBIE_HITS2[count]))
                red_bullets.remove(bullet)
                break
            elif bullet.y < 0:  # gets rid of bullet when it hits the top
                red_bullets.remove(bullet)
                break
            count += 1

    count = 0
    for sublist in zombie_list:
        # checks if zombie collided with yellow
        if yellow.colliderect(sublist[1]):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            pygame.event.post(pygame.event.Event(ZOMBIE_HITS[count]))
        elif sublist[1].y >= HEIGHT:  # gets rid of zombie when at bottom
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            pygame.event.post(pygame.event.Event(ZOMBIE_HITS[count]))
        count += 1

    count = 0
    for sublist in zombie_list2:
        # checks if zombie collided with yellow
        if red.colliderect(sublist[1]):
            pygame.event.post(pygame.event.Event(RED_HIT))
            pygame.event.post(pygame.event.Event(ZOMBIE_HITS2[count]))
        elif sublist[1].y >= HEIGHT:  # gets rid of zombie when at bottom
            pygame.event.post(pygame.event.Event(RED_HIT))
            pygame.event.post(pygame.event.Event(ZOMBIE_HITS2[count]))
        count += 1


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    # draws the winner text right in the middle of the screen
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2,
                         HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(500)
    WIN_SOUND.play()
    pygame.time.delay(3500)  # pause for 5 seconds


def main():
    """main code"""
    # keeps location of each spaceship so we can change it
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    zombie_list = [[25, pygame.Rect(
        random.randint(0, WIDTH//2 - SPACESHIP_WIDTH - 5), 0,
        SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 3],
                   [35, pygame.Rect(
                       random.randint(0, WIDTH//2 - SPACESHIP_WIDTH - 5), 0,
                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 3],
                   [45, pygame.Rect(
                       random.randint(0, WIDTH//2 - SPACESHIP_WIDTH - 5), 0,
                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 5],
                   [55, pygame.Rect(
                       random.randint(0, WIDTH//2 - SPACESHIP_WIDTH - 5), 0,
                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 5],
                   [65, pygame.Rect(
                       random.randint(0, WIDTH//2 - SPACESHIP_WIDTH - 5), 0,
                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 7]]

    zombie_list2 = [[25, pygame.Rect(
        random.randint(WIDTH//2 - SPACESHIP_WIDTH - 5, WIDTH), 0,
        SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 3],
                   [35, pygame.Rect(
                       random.randint(WIDTH//2, WIDTH - 50), 0,
                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 3],
                   [45, pygame.Rect(
                       random.randint(WIDTH//2, WIDTH - 50), 0,
                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 5],
                   [55, pygame.Rect(
                       random.randint(WIDTH//2, WIDTH - 50), 0,
                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 5],
                   [65, pygame.Rect(
                       random.randint(WIDTH//2, WIDTH - 50), 0,
                       SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 7]]

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    timeit = 0
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
                    bullet = pygame.Rect(yellow.x + yellow.width//2,
                                         yellow.y, 5, 10)
                    yellow_bullets.append(bullet)
                    # plays sound when firing
                    BULLET_FIRE_SOUND.play()  # plays sound when firing

                if event.key == pygame.K_RCTRL and \
                        len(red_bullets) < MAX_BULLETS:
                    # makes the bullet and puts it at the red spaceship
                    # with the width and height of the bullet being (10, 5)
                    bullet = pygame.Rect(red.x + red.width//2, red.y, 5, 10)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()  # plays sound when firing

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

            for i in range(0, 5):
                if event.type == ZOMBIE_HITS[i]:
                    zombie_list[i][2] -= 1
                    # plays sound when ship is hit
                    BULLET_HIT_SOUND1.play()

                if zombie_list[i][2] == 0:
                    zombie_list[i][1] = pygame.Rect(
                        random.randint(0, WIDTH//2 - SPACESHIP_WIDTH - 5), 0,
                        SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
                    if zombie_list[i][0] <= 35:
                        zombie_list[i][2] = 3
                    elif zombie_list[i][0] <= 55:
                        zombie_list[i][2] = 5
                    else:
                        zombie_list[i][2] = 7

            for i in range(0, 5):
                if event.type == ZOMBIE_HITS2[i]:
                    zombie_list2[i][2] -= 1
                    # plays sound when ship is hit
                    BULLET_HIT_SOUND.play()

                if zombie_list2[i][2] == 0:
                    zombie_list2[i][1] = pygame.Rect(
                        random.randint(WIDTH//2, WIDTH - 50),
                        0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
                    if zombie_list2[i][0] <= 35:
                        zombie_list2[i][2] = 3
                    elif zombie_list2[i][0] <= 55:
                        zombie_list2[i][2] = 5
                    else:
                        zombie_list2[i][2] = 7

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

        handle_bullets(yellow_bullets, red_bullets, zombie_list,
                       zombie_list2, yellow, red)

        timeit += 1
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, zombie_list, zombie_list2)
        for sublist in zombie_list:
            if timeit % sublist[0] == 0:
                sublist[1].y += 25

        for sublist in zombie_list2:
            if timeit % sublist[0] == 0:
                sublist[1].y += 25
    main()


if __name__ == "__main__":
    main()
