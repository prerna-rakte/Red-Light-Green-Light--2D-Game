import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Red Light Green Light - Squid Doll Edition")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
WHITE = (240,240,240)
BLACK = (15,15,15)
RED = (200,40,40)
GREEN = (40,200,90)
DARK_SKY = (30,20,40)
GROUND = (50,60,50)

SKIN = (255,220,177)
DRESS = (255,140,0)
SHIRT = (255,220,0)
HAIR = (50,30,10)

PLAYER_GREEN = (30,160,70)
PANTS = (30,30,30)
TREE_GREEN = (20,50,20)
TREE_TRUNK = (60,40,20)

status_font = pygame.font.SysFont("arial", 60, bold=True)
timer_font = pygame.font.SysFont("consolas", 36)
small_font = pygame.font.SysFont("arial", 26)

goal_line = 100
time_limit = 20

# ---------------- GAME STATE ----------------
game_started = False

# ---------------- RESET GAME ----------------
def reset_game():
    global player_x, player_y, leg_angle, arm_angle
    global player_speed, direction, breath_offset, breath_dir
    global light, light_timer, start_ticks, game_over, win
    global finish_hold_timer, eyes_open, blink_timer

    player_x = WIDTH//2
    player_y = HEIGHT - 60
    leg_angle = 0
    arm_angle = 0
    player_speed = 4
    direction = 1
    breath_offset = 0
    breath_dir = 1

    light = "GREEN"
    light_timer = 0
    start_ticks = pygame.time.get_ticks()

    game_over = False
    win = False
    finish_hold_timer = 0

    eyes_open = True
    blink_timer = 0

reset_game()

# ---------------- START SCREEN ----------------
def draw_start_screen():
    screen.fill((15, 10, 30))

    title_font = pygame.font.SysFont("arial", 75, bold=True)
    subtitle_font = pygame.font.SysFont("arial", 35)

    title = title_font.render("RED LIGHT GREEN LIGHT", True, RED)
    subtitle = subtitle_font.render("Press SPACE to Start", True, WHITE)

    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))

    pygame.display.update()

# ---------------- DRAW BACKGROUND ----------------
def draw_background():
    screen.fill(DARK_SKY)

    for x in range(150, WIDTH, 250):
        pygame.draw.rect(screen, TREE_TRUNK, (x, goal_line-50, 12, 50))
        pygame.draw.circle(screen, TREE_GREEN, (x+6, goal_line-70), 30)

    pygame.draw.rect(screen, GROUND,
                     (0, goal_line, WIDTH, HEIGHT-goal_line))

    pygame.draw.line(screen, WHITE,
                     (0, goal_line), (WIDTH, goal_line), 4)

# ---------------- DRAW PLAYER ----------------
def draw_player():
    body_y = player_y + breath_offset

    pygame.draw.circle(screen, SKIN, (int(player_x), int(body_y-40)), 14)
    pygame.draw.rect(screen, PLAYER_GREEN,
                     (int(player_x-15), int(body_y-40), 30, 45))

    number = small_font.render("456", True, WHITE)
    screen.blit(number, (int(player_x-16), int(body_y-30)))

    pygame.draw.line(screen, SKIN,
                     (int(player_x), int(body_y-20)),
                     (int(player_x-20), int(body_y+arm_angle)), 4)
    pygame.draw.line(screen, SKIN,
                     (int(player_x), int(body_y-20)),
                     (int(player_x+20), int(body_y-arm_angle)), 4)

    pygame.draw.line(screen, PANTS,
                     (int(player_x-8), int(body_y+5)),
                     (int(player_x-15), int(body_y+40+leg_angle)), 5)
    pygame.draw.line(screen, PANTS,
                     (int(player_x+8), int(body_y+5)),
                     (int(player_x+15), int(body_y+40-leg_angle)), 5)

# ---------------- DRAW DOLL ----------------
def draw_doll():
    doll_x = WIDTH//2
    doll_y = goal_line - 10

    pygame.draw.circle(screen, SKIN, (doll_x, doll_y), 40)
    pygame.draw.circle(screen, HAIR, (doll_x-20, doll_y-25), 20)
    pygame.draw.circle(screen, HAIR, (doll_x+20, doll_y-25), 20)

    if eyes_open:
        pygame.draw.circle(screen, BLACK, (doll_x-12, doll_y), 6)
        pygame.draw.circle(screen, BLACK, (doll_x+12, doll_y), 6)
    else:
        pygame.draw.line(screen, BLACK, (doll_x-16, doll_y), (doll_x-8, doll_y), 2)
        pygame.draw.line(screen, BLACK, (doll_x+8, doll_y), (doll_x+16, doll_y), 2)

    pygame.draw.polygon(screen, DRESS,
                        [(doll_x-60, doll_y+40),
                         (doll_x+60, doll_y+40),
                         (doll_x+30, doll_y+170),
                         (doll_x-30, doll_y+170)])

    pygame.draw.line(screen, SKIN, (doll_x-30, doll_y+50), (doll_x-75, doll_y+90), 6)
    pygame.draw.line(screen, SKIN, (doll_x+30, doll_y+50), (doll_x+75, doll_y+90), 6)

# ---------------- MAIN LOOP ----------------
running = True
finish_hold_timer = 0

while running:
    clock.tick(60)

    # START SCREEN
    if not game_started:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    reset_game()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (game_over or win) and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()
    moving = False

    if not game_over and not win:
        if keys[pygame.K_UP]:
            player_y -= player_speed
            moving = True
        if keys[pygame.K_DOWN]:
            player_y += player_speed
            moving = True
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        player_x = max(20, min(WIDTH-20, player_x))
        player_y = max(goal_line, min(HEIGHT-20, player_y))

        breath_offset += 0.2 * (1 if moving else -1)
        if abs(breath_offset) > 3:
            breath_offset *= -1

        if moving:
            leg_angle = (leg_angle + 3) % 30 - 15
            arm_angle = (arm_angle + 3) % 30 - 15

        if light == "RED" and moving:
            game_over = True

        light_timer += 1
        if light_timer >= random.randint(100,180):
            light_timer = 0
            light = "GREEN" if light == "RED" else "RED"

        blink_timer += 1
        if blink_timer > 120:
            eyes_open = not eyes_open
            blink_timer = 0

        seconds = (pygame.time.get_ticks() - start_ticks)/1000
        remaining = max(0, time_limit - seconds)

        if player_y <= goal_line + 5:
            finish_hold_timer += 1
            if finish_hold_timer > 30:
                win = True
            player_speed = 0
        else:
            finish_hold_timer = 0

    else:
        remaining = max(0, time_limit - (pygame.time.get_ticks() - start_ticks)/1000)

    draw_background()
    draw_doll()
    draw_player()

    if light == "RED" and not win and not game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((200,0,0))
        screen.blit(overlay, (0,0))

    status_text = "GREEN LIGHT" if light=="GREEN" else "RED LIGHT"
    color = GREEN if light=="GREEN" else RED
    text_surface = status_font.render(status_text, True, color)
    screen.blit(text_surface, text_surface.get_rect(center=(WIDTH//2,50)))

    timer_display = f"{int(remaining)//60:02}:{int(remaining)%60:02}"
    timer_surface = timer_font.render(timer_display, True, WHITE)
    screen.blit(timer_surface, (30,30))

    if game_over:
        over = status_font.render("GAME OVER", True, RED)
        screen.blit(over, over.get_rect(center=(WIDTH//2, HEIGHT//2)))
        restart = small_font.render("Press R to Restart", True, WHITE)
        screen.blit(restart, restart.get_rect(center=(WIDTH//2, HEIGHT//2+60)))

    if win:
        win_text = status_font.render("YOU WIN", True, GREEN)
        screen.blit(win_text, win_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        restart = small_font.render("Press R to Restart", True, WHITE)
        screen.blit(restart, restart.get_rect(center=(WIDTH//2, HEIGHT//2+60)))

    pygame.display.update()

pygame.quit()
sys.exit()
