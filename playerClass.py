import pygame
from bulletClass import Bullet
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets, laser_sound):
        super().__init__()
        self.image = pygame.image.load("hola/sprites/nave1.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100
        self.nombre = ""  # Nuevo atributo "nombre" para almacenar el nombre del jugador
        self.all_sprites = all_sprites
        self.bullets = bullets
        self.laser_sound = laser_sound

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)
        self.laser_sound.play()

