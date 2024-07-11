import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Juego Completo en Pygame")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Configuración del jugador
player_size = 50
player_pos = [width // 2, height - 2 * player_size]
player_speed = 10

# Configuración de enemigos
enemy_size = 50
enemy_pos = [random.randint(0, width - enemy_size), 0]
enemy_list = [enemy_pos]
enemy_speed = 10

# Configuración de balas
bullet_size = 20
bullet_pos = [0, 0]
bullet_speed = 20
bullet_list = []

# Configuración de poderes
power_size = 30
power_pos = [random.randint(0, width - power_size), 0]
power_list = [power_pos]
power_speed = 5

# Sistema de puntuación y vidas
score = 0
lives = 3

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Fuentes
font = pygame.font.SysFont("monospace", 35)

# Funciones auxiliares
def draw_player():
    pygame.draw.rect(screen, green, (player_pos[0], player_pos[1], player_size, player_size))

def draw_enemies():
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def draw_bullets():
    for bullet_pos in bullet_list:
        pygame.draw.rect(screen, blue, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))

def draw_powers():
    for power_pos in power_list:
        pygame.draw.rect(screen, white, (power_pos[0], power_pos[1], power_size, power_size))

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def update_bullet_positions(bullet_list):
    for idx, bullet_pos in enumerate(bullet_list):
        if bullet_pos[1] > 0:
            bullet_pos[1] -= bullet_speed
        else:
            bullet_list.pop(idx)

def update_power_positions(power_list):
    for idx, power_pos in enumerate(power_list):
        if power_pos[1] >= 0 and power_pos[1] < height:
            power_pos[1] += power_speed
        else:
            power_list.pop(idx)

def collision_with_bullets(enemy_list, bullet_list):
    for enemy_pos in enemy_list:
        for bullet_pos in bullet_list:
            if detect_collision(enemy_pos, bullet_pos):
                enemy_list.remove(enemy_pos)
                bullet_list.remove(bullet_pos)
                return True
    return False

def collision_with_power(player_pos, power_list):
    for power_pos in power_list:
        if detect_collision(player_pos, power_pos):
            power_list.remove(power_pos)
            return True
    return False

# Pantalla de inicio
def start_screen():
    while True:
        screen.fill(black)
        welcome_text = font.render("Presiona Enter para empezar", True, white)
        screen.blit(welcome_text, (width//4, height//2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# Pantalla de fin
def game_over_screen(score):
    while True:
        screen.fill(black)
        game_over_text = font.render(f"Game Over! Puntuación: {score}", True, white)
        screen.blit(game_over_text, (width//4, height//2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# Pantalla de inicio
start_screen()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_pos[0] -= player_speed
            if event.key == pygame.K_RIGHT:
                player_pos[0] += player_speed
            if event.key == pygame.K_UP:
                player_pos[1] -= player_speed
            if event.key == pygame.K_DOWN:
                player_pos[1] += player_speed
            if event.key == pygame.K_SPACE:
                bullet_list.append([player_pos[0] + player_size//2 - bullet_size//2, player_pos[1]])

    player_pos[0] = max(0, min(player_pos[0], width - player_size))
    player_pos[1] = max(0, min(player_pos[1], height - player_size))

    score = update_enemy_positions(enemy_list, score)
    update_bullet_positions(bullet_list)
    update_power_positions(power_list)

    if collision_with_bullets(enemy_list, bullet_list):
        score += 5

    if collision_with_power(player_pos, power_list):
        lives += 1

    if random.randint(1, 20) == 1:
        enemy_list.append([random.randint(0, width - enemy_size), 0])

    if random.randint(1, 100) == 1:
        power_list.append([random.randint(0, width - power_size), 0])

    screen.fill(black)
    draw_player()
    draw_enemies()
    draw_bullets()
    draw_powers()

    if any(detect_collision(player_pos, enemy_pos) for enemy_pos in enemy_list):
        lives -= 1
        if lives == 0:
            game_over_screen(score)
            start_screen()
            score = 0
            lives = 3
            enemy_list = []
            bullet_list = []
            power_list = []

    score_text = font.render(f"Puntuación: {score}", True, white)
    lives_text = font.render(f"Vidas: {lives}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    pygame.display.update()
    clock.tick(30)