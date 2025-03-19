import pygame
import random

# تنظیمات اولیه
pygame.init()

# رنگ‌ها
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# اندازه صفحه
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pechman Game')

# تنظیمات پکمن
packman_size = 20
packman_x = WIDTH // 2
packman_y = HEIGHT // 2
packman_speed = 5

# تنظیمات امتیاز
score = 0
food = [(random.randint(0, WIDTH // packman_size - 1) * packman_size,
          random.randint(0, HEIGHT // packman_size - 1) * packman_size) for _ in range(10)]

# تنظیمات دشمنان
enemies = [(random.randint(0, WIDTH // packman_size - 1) * packman_size,
            random.randint(0, HEIGHT // packman_size - 1) * packman_size) for _ in range(3)]

# تابع برای نمایش امتیاز
def show_score(score):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

# حلقه اصلی بازی
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # حرکت پکمن
    if keys[pygame.K_LEFT]:
        packman_x -= packman_speed
    if keys[pygame.K_RIGHT]:
        packman_x += packman_speed
    if keys[pygame.K_UP]:
        packman_y -= packman_speed
    if keys[pygame.K_DOWN]:
        packman_y += packman_speed

    # محدود کردن حرکت پکمن داخل صفحه
    packman_x = max(0, min(packman_x, WIDTH - packman_size))
    packman_y = max(0, min(packman_y, HEIGHT - packman_size))

    # بررسی جمع‌آوری غذا
    for f in food[:]:
        if f[0] == packman_x and f[1] == packman_y:
            food.remove(f)
            score += 1

    # بررسی برخورد با دشمنان
    for e in enemies:
        if e[0] == packman_x and e[1] == packman_y:
            print("Game Over!")
            running = False

    # نمایش صفحه و محتوا
    screen.fill(BLACK)
    pygame.draw.rect(screen, YELLOW, (packman_x, packman_y, packman_size, packman_size))

    for f in food:
        pygame.draw.rect(screen, WHITE, (f[0], f[1], packman_size, packman_size))

    for e in enemies:
        pygame.draw.rect(screen, BLUE, (e[0], e[1], packman_size, packman_size))

    show_score(score)

    pygame.display.update()
    pygame.time.delay(100)

# پایان بازی
pygame.quit()