import pygame
from pygame import mixer

mixer.init()
screen = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption("Pong")

# Background
background = pygame.image.load("pong/background.jpg")

FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Score
score_1 = 0
score_2 = 0
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 32)

# players
PLAYER_VEL = 10
player_1_width, player_1_height = 15, 50
player_2_width, player_2_height = 15, 50
player_1 = pygame.rect.Rect(0, 300, player_1_width, player_1_height)
player_2 = pygame.rect.Rect(785, 300, player_2_width, player_2_height)

# ball
ball_width, ball_height = 10, 10
ball = pygame.rect.Rect(400, 300, ball_width, ball_height) 
ball_x_change = 5
ball_y_change = 5

def draw_on_screen():
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, BLACK, player_1)
    pygame.draw.rect(screen, BLACK, player_2)
    pygame.draw.rect(screen, RED, ball)
    text_1 = font.render("score : " + str(score_1), True, WHITE)
    text_2 = font.render("score : " + str(score_2), True, WHITE)
    screen.blit(text_1, (10, 10))
    screen.blit(text_2, (640, 10))

    pygame.display.flip()

def handle_players_movements(keys_pressed):
    
    if keys_pressed[pygame.K_w] and player_1.y > 0:
        player_1.y -= PLAYER_VEL
    if keys_pressed[pygame.K_s] and player_1.y < 550:
        player_1.y += PLAYER_VEL        
    if keys_pressed[pygame.K_UP] and player_2.y > 0:
        player_2.y -= PLAYER_VEL
    if keys_pressed[pygame.K_DOWN] and player_2.y < 550:
        player_2.y += PLAYER_VEL 
    
def is_collision(ball, player_1, player_2):
    return ball.collidelist([player_1, player_2])
    
winner_font = pygame.font.Font('freesansbold.ttf', 50)
clock = pygame.time.Clock()
winner = ""
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    keys_pressed = pygame.key.get_pressed()
    handle_players_movements(keys_pressed)

    # ball movements
    ball.x += ball_x_change
    ball.y += ball_y_change

    # Collision with players
    collision = is_collision(ball, player_1, player_2)
    if collision == 0:
        ball_x_change = 5
        hit_sound = mixer.Sound("pong/ball_hit.wav")
        hit_sound.play()
    elif collision == 1:
        ball_x_change = -5
        hit_sound = mixer.Sound("pong/ball_hit.wav")
        hit_sound.play()

    # boundry top and bottom
    if ball.y < 0 :
        ball_y_change = 5
    if ball.y > 590:
        ball_y_change = -5

    # score
    if ball.x < 0 and collision is -1:
        score_2 += 1
        ball.x, ball.y = player_2.x, player_2.y + 15
    if ball.x > 785 and collision is -1:
        score_1 += 1
        ball.x, ball.y = player_1.x + 5, player_1.y + 15

    # Check for winner
    if score_1 >= 10:
        winner = "PLAYER 1 WINS!"
    if score_2 >= 10:
        winner = "PLAYER 2 WINS!"

    if winner != "":
        winner_text = winner_font.render(winner, True, RED)
        screen.blit(winner_text, (200 , 250))
        pygame.display.update()
        winner_sound = mixer.Sound("pong/winner.wav")
        winner_sound.play()
        pygame.time.delay(5000)
        # resetting all things
        score_1 = 0
        score_2 = 0
        player_1.x , player_1.y = 0, 300
        player_2.x , player_2.y = 785, 300
        ball.x, ball.y = 400, 300
        winner = ""

    draw_on_screen()
    
    