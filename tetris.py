import pygame
import random

# تنظیمات بازی
WIDTH = 800
HEIGHT = 700
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# رنگ‌ها
COLORS = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0, 255),
    (0, 220, 220)
]

# اشکال تتریس
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

class Tetromino:
    def __init__(self, x, y):
        self.shape = random.choice(SHAPES)
        self.color = random.randint(1, len(COLORS)-1)
        self.x = x
        self.y = y
        self.rotation = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.score = 0
        self.game_over = False
        self.new_piece()
        self.fall_time = 0
        self.fall_speed = 500

    def new_piece(self):
        self.current_piece = Tetromino(GRID_WIDTH // 2 - 1, 0)
        if self.check_collision():
            self.game_over = True

    def check_collision(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece.x + x
                    board_y = self.current_piece.y + y
                    if (board_x < 0 or board_x >= GRID_WIDTH or
                        board_y >= GRID_HEIGHT or
                        self.grid[board_y][board_x]):
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.clear_lines()

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT-1, -1, -1):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0]*GRID_WIDTH)
                lines_cleared += 1
        self.score += lines_cleared ** 2 * 100

    def move(self, dx, dy):
        self.current_piece.x += dx
        self.current_piece.y += dy
        if self.check_collision():
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False
        return True

    def rotate(self):
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if self.check_collision():
            self.current_piece.shape = original_shape

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, COLORS[self.grid[y][x]],
                                (x*BLOCK_SIZE + 1, y*BLOCK_SIZE + 1,
                                 BLOCK_SIZE - 2, BLOCK_SIZE - 2))

    def draw_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, COLORS[self.current_piece.color],
                                    ((self.current_piece.x + x)*BLOCK_SIZE + 1,
                                     (self.current_piece.y + y)*BLOCK_SIZE + 1,
                                     BLOCK_SIZE - 2, BLOCK_SIZE - 2))

    def draw_score(self):
        font = pygame.font.SysFont('Arial', 30)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(text, (GRID_WIDTH*BLOCK_SIZE + 20, 20))

    def draw_game_over(self):
        font = pygame.font.SysFont('Arial', 50)
        text = font.render('GAME OVER!', True, (255, 0, 0))
        self.screen.blit(text, (WIDTH//2 - 130, HEIGHT//2 - 50))
        text = font.render('Press R to restart', True, (255, 255, 255))
        self.screen.blit(text, (WIDTH//2 - 160, HEIGHT//2 + 20))

    def run(self):
        while not self.game_over:
            self.screen.fill((0, 0, 0))
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.move(1, 0)
                    if event.key == pygame.K_DOWN:
                        self.move(0, 1)
                    if event.key == pygame.K_UP:
                        self.rotate()
                    if event.key == pygame.K_SPACE:
                        while self.move(0, 1):
                            pass

            if current_time - self.fall_time > self.fall_speed:
                if not self.move(0, 1):
                    self.merge_piece()
                    self.new_piece()
                self.fall_time = current_time

            self.draw_grid()
            self.draw_piece()
            self.draw_score()
            pygame.display.flip()
            self.clock.tick(60)

        # Game over loop
        while True:
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_score()
            self.draw_game_over()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.run()
                        return

if __name__ == "__main__":
    game = Tetris()
    game.run()