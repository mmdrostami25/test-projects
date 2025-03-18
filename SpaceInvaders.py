import pygame
import random

pygame.init()

# تنظیمات
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# بازیکن
player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 60, 50, 30)
player_speed = 5

# لیست مهاجمان
invaders = []
for row in range(3):
    for col in range(8):
        invaders.append(pygame.Rect(100 + col*70, 50 + row*50, 40, 30))

# گلوله‌ها
bullets = []
invader_bullets = []
bullet_speed = 7

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(
                    player.centerx - 2, player.top, 4, 10))

    # حرکت بازیکن
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # حرکت مهاجمان
    for invader in invaders:
        invader.x += 1
        if invader.right > WIDTH or invader.left < 0:
            for inv in invaders:
                inv.y += 10
                inv.x -= 1

    # حرکت گلوله‌ها
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)
            
    # شلیک مهاجمان
    if random.randint(0, 100) < 2 and invaders:
        invader = random.choice(invaders)
        invader_bullets.append(pygame.Rect(
            invader.centerx - 2, invader.bottom, 4, 10))

    # حرکت گلوله‌های مهاجمان
    for bullet in invader_bullets:
        bullet.y += bullet_speed//2
        if bullet.top > HEIGHT:
            invader_bullets.remove(bullet)

    # تشخیص برخورد
    for bullet in bullets[:]:
        for invader in invaders[:]:
            if bullet.colliderect(invader):
                bullets.remove(bullet)
                invaders.remove(invader)
                break

    # رسم اجزا
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    
    for invader in invaders:
        pygame.draw.rect(screen, RED, invader)
    
    for bullet in bullets + invader_bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()