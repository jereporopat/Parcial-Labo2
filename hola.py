import pygame
import sys
from config import *
from playerClass import Player
from meteorClass import Meteor
from database import guardar_datos

def game_over(screen):
    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, "Game Over", 50, WIDTH // 2, HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def setup_game():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shooter")
    clock = pygame.time.Clock()
    return screen, clock


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(midtop=(x, y))
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)


def load_images():
    meteor_images = []
    meteor_list = [
        "hola/sprites/meteorGrey_big1.png",
        "hola/sprites/meteorGrey_big2.png",
        "hola/sprites/meteorGrey_big3.png",
        "hola/sprites/meteorGrey_big4.png",
        "hola/sprites/meteorGrey_med1.png",
        "hola/sprites/meteorGrey_med2.png",
        "hola/sprites/meteorGrey_small1.png",
        "hola/sprites/meteorGrey_small2.png",
        "hola/sprites/meteorGrey_tiny1.png",
        "hola/sprites/meteorGrey_tiny2.png"
    ]

    for img in meteor_list:
        meteor_images.append(pygame.image.load(img).convert())

    return meteor_images


def main(player_name):
    screen, clock = setup_game()
    meteor_images = load_images()

    # Cargar fondo.
    background = pygame.image.load("hola/sprites/fondo.jpg").convert()

    # Cargar sonidos
    laser_sound = pygame.mixer.Sound("hola/sprites/assets_laser5.ogg")
    pygame.mixer.music.load("hola/sprites/assets_music.ogg")
    pygame.mixer.music.set_volume(0.1)

    all_sprites = pygame.sprite.Group()
    meteor_group = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player(all_sprites, bullets, laser_sound)
    all_sprites.add(player)

    for _ in range(8):
        meteor = Meteor(meteor_images)
        all_sprites.add(meteor)
        meteor_group.add(meteor)

    # Marcador / Score
    score = 0
    level = 1
    meteor_count = 0
    pygame.mixer.music.play(loops=-1)

    # Game Loop
    running = True
    while running:
        # Keep loop running at the right speed
        clock.tick(60)

        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()

        # Colisiones meteoro - laser
        hits = pygame.sprite.groupcollide(meteor_group, bullets, True, True)
        for hit in hits:
            score += 1
            meteor_count += 1
            if meteor_count >= 20:
                level += 1
                meteor_count = 0
                for _ in range(level * 5):  # Generar más asteroides en niveles superiores
                    meteor = Meteor(meteor_images)
                    all_sprites.add(meteor)
                    meteor_group.add(meteor)
            meteor = Meteor(meteor_images)
            all_sprites.add(meteor)
            meteor_group.add(meteor)

        # Colisiones jugador - meteoro
        hits = pygame.sprite.spritecollide(player, meteor_group, True)
        for hit in hits:
            player.shield -= 25
            meteor = Meteor(meteor_images)
            all_sprites.add(meteor)
            meteor_group.add(meteor)
            if player.shield <= 0:
                running = False
                guardar_datos(player_name, score)
                game_over(screen)  # Mostrar pantalla de "Game Over" y volver al menú principal

        # Draw / Render
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Marcador
        draw_text(screen, "Score: " + str(score), 25, WIDTH // 2, 10)

        # Nivel
        draw_text(screen, "Level: " + str(level), 25, WIDTH // 2, 40)

        # ESCUDO.
        draw_shield_bar(screen, 5, 5, player.shield)

        pygame.display.update()

    pygame.quit()
    main()