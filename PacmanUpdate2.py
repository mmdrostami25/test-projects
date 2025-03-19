import pygame
import random

# تنظیمات اولیه
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 30
PLAYER_SPEED = 5

# رنگ‌ها
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# ساخت نقشه
maze = [
    "####################",
    "#..................#",
    "#.###.###..###.###.#",
    "#.#...#......#...#.#",
    "#.#.###.####.###.#.#",
    "#.................#",
    "#.###.#.######.###.#",
    "#.....#....##....# #",
    "#######.# ## #.####",
    "#..........P........#",
    "####################"
]

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = (0, 0)

class Ghost:
    def __init__(self):
        self.x = random.randint(1, 18) * CELL_SIZE
        self.y = random.randint(1, 18) * CELL_SIZE
        self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])

def draw_maze(screen):
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, (col_idx*CELL_SIZE, row_idx*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == '.':
                pygame.draw.circle(screen, WHITE, 
                                   (col_idx*CELL_SIZE + CELL_SIZE//2, row_idx*CELL_SIZE + CELL_SIZE//2), 
                                   3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    player = Player()
    ghost = Ghost()
    score = 0
    
    # پیدا کردن موقعیت اولیه پکمن
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == 'P':
                player.x = x * CELL_SIZE
                player.y = y * CELL_SIZE
                break
    
    running = True
    while running:
        screen.fill(BLACK)
        
        # پردازش رویدادها
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    player.direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    player.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.direction = (1, 0)
        
        # حرکت پکمن
        new_x = player.x + player.direction[0] * PLAYER_SPEED
        new_y = player.y + player.direction[1] * PLAYER_SPEED
        
        # بررسی برخورد با دیوارها
        col = int(new_x // CELL_SIZE)
        row = int(new_y // CELL_SIZE)
        if maze[row][col] != '#':
            player.x = new_x
            player.y = new_y
        
        # حرکت روح
        ghost.x += ghost.direction[0] * 2
        ghost.y += ghost.direction[1] * 2
        if random.randint(0, 100) < 5:  # تغییر جهت تصادفی
            ghost.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        
        # جمع کردن نقاط
        col = int(player.x // CELL_SIZE)
        row = int(player.y // CELL_SIZE)
        if maze[row][col] == '.':
            maze[row] = maze[row][:col] + ' ' + maze[row][col+1:]
            score += 10
        
        # کشیدن المان‌ها
        draw_maze(screen)
        pygame.draw.circle(screen, YELLOW, (player.x + CELL_SIZE//2, player.y + CELL_SIZE//2), CELL_SIZE//2)
        pygame.draw.circle(screen, RED, (ghost.x + CELL_SIZE//2, ghost.y + CELL_SIZE//2), CELL_SIZE//2)
        
        # نمایش امتیاز
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    main()