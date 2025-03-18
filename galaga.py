import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH = 480
HEIGHT = 640
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaga Lite")
clock = pygame.time.Clock()

# Sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-50))
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(screen.get_rect())

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(30, WIDTH-30), 30))
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create initial enemies
for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update
    all_sprites.update()

    # Collision detection
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        # Spawn new enemy
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw everything
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()