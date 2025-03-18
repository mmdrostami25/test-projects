import pygame
import random
import json
import os
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
FPS = 15

# Colors
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128)
}

# Game Settings
SETTINGS_FILE = "snake_settings.json"
DEFAULT_SETTINGS = {
    "snake_color": COLORS["green"],
    "bg_color": COLORS["black"],
    "speed": FPS,
    "high_score": 0
}

class PowerUp:
    TYPES = [
        {"name": "Double Points", "color": COLORS["yellow"], "duration": 10},
        {"name": "Speed Boost", "color": COLORS["orange"], "duration": 8},
        {"name": "Shield", "color": COLORS["purple"], "duration": 12}
    ]
    
    def __init__(self):
        self.type = random.choice(self.TYPES)
        self.x = random.randint(0, WIDTH - BLOCK_SIZE)
        self.y = random.randint(0, HEIGHT - BLOCK_SIZE)
        self.spawn_time = time.time()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game - Single Player')
        self.clock = pygame.time.Clock()
        self.load_settings()
        self.reset_game()
        
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                self.settings = {**DEFAULT_SETTINGS, **json.load(f)}
        else:
            self.settings = DEFAULT_SETTINGS

    def save_settings(self):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f)

    def reset_game(self):
        self.snake = [[WIDTH//2, HEIGHT//2]]
        self.direction = [BLOCK_SIZE, 0]
        self.score = 0
        self.level = 1
        self.apple = self.new_apple()
        self.powerups = []
        self.obstacles = []
        self.active_powerups = {}
        self.game_over = False
        self.spawn_obstacles()
        
    def new_apple(self):
        return [
            random.randint(0, WIDTH - BLOCK_SIZE),
            random.randint(0, HEIGHT - BLOCK_SIZE)
        ]

    def spawn_obstacles(self):
        for _ in range(3):
            self.obstacles.append({
                "x": random.randint(0, WIDTH - 50),
                "y": random.randint(0, HEIGHT - 50),
                "speed": random.choice([-5, 5])
            })

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont('Arial', size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def handle_powerups(self):
        if random.randint(1, 100) < 3 and len(self.powerups) < 2:
            self.powerups.append(PowerUp())
        
        for powerup in self.powerups[:]:
            pu_rect = pygame.Rect(powerup.x, powerup.y, BLOCK_SIZE, BLOCK_SIZE)
            if pu_rect.colliderect(pygame.Rect(self.snake[0][0], self.snake[0][1], BLOCK_SIZE, BLOCK_SIZE)):
                self.activate_powerup(powerup)
                self.powerups.remove(powerup)

    def activate_powerup(self, powerup):
        self.active_powerups[powerup.type["name"]] = {
            "start_time": time.time(),
            "duration": powerup.type["duration"]
        }
        
    def check_powerups(self):
        current_time = time.time()
        for name in list(self.active_powerups.keys()):
            if current_time - self.active_powerups[name]["start_time"] > self.active_powerups[name]["duration"]:
                del self.active_powerups[name]

    def run(self):
        while not self.game_over:
            self.handle_input()
            self.move()
            self.check_collisions()
            self.update_screen()
            self.clock.tick(self.settings["speed"] + self.level*2)
            
        self.game_over_screen()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction[0] != BLOCK_SIZE:
                    self.direction = [-BLOCK_SIZE, 0]
                elif event.key == pygame.K_RIGHT and self.direction[0] != -BLOCK_SIZE:
                    self.direction = [BLOCK_SIZE, 0]
                elif event.key == pygame.K_UP and self.direction[1] != BLOCK_SIZE:
                    self.direction = [0, -BLOCK_SIZE]
                elif event.key == pygame.K_DOWN and self.direction[1] != -BLOCK_SIZE:
                    self.direction = [0, BLOCK_SIZE]

    def move(self):
        new_head = [
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        ]
        
        # Screen wrapping
        new_head[0] = new_head[0] % WIDTH
        new_head[1] = new_head[1] % HEIGHT
        
        self.snake.insert(0, new_head)
        
        if self.check_apple_collision(new_head):
            self.handle_apple_collision()
        else:
            self.snake.pop()

    def check_apple_collision(self, head):
        return (
            abs(head[0] - self.apple[0]) < BLOCK_SIZE and
            abs(head[1] - self.apple[1]) < BLOCK_SIZE
        )

    def handle_apple_collision(self):
        self.score += 2 if "Double Points" in self.active_powerups else 1
        self.apple = self.new_apple()
        if self.score % 5 == 0:
            self.level += 1
        if self.score > self.settings["high_score"]:
            self.settings["high_score"] = self.score

    def check_collisions(self):
        # Self collision
        if any(segment == self.snake[0] for segment in self.snake[1:]):
            if "Shield" not in self.active_powerups:
                self.game_over = True
                
        # Obstacle collision
        for obs in self.obstacles:
            if (
                abs(self.snake[0][0] - obs["x"]) < BLOCK_SIZE and
                abs(self.snake[0][1] - obs["y"]) < BLOCK_SIZE
            ):
                self.game_over = True

    def update_screen(self):
        self.screen.fill(self.settings["bg_color"])
        
        # Draw obstacles
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, COLORS["blue"], 
                           (obs["x"], obs["y"], 50, 50))
            obs["x"] += obs["speed"]
            if obs["x"] > WIDTH or obs["x"] < 0:
                obs["speed"] *= -1
        
        # Draw apple
        pygame.draw.rect(self.screen, COLORS["red"], 
                        (*self.apple, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.settings["snake_color"], 
                            (*segment, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw powerups
        for powerup in self.powerups:
            pygame.draw.circle(self.screen, powerup.type["color"],
                              (powerup.x, powerup.y), 15)
        
        # Draw UI
        self.draw_text(f"Score: {self.score}  Level: {self.level}", 24, COLORS["white"], 10, 10)
        self.draw_text(f"High Score: {self.settings['high_score']}", 24, COLORS["white"], 10, 40)
        
        pygame.display.flip()

    def game_over_screen(self):
        while True:
            self.screen.fill(COLORS["black"])
            self.draw_text("GAME OVER!", 64, COLORS["red"], WIDTH//4, HEIGHT//3)
            self.draw_text(f"Final Score: {self.score}", 48, COLORS["white"], WIDTH//4, HEIGHT//2)
            self.draw_text("Press R to Restart  |  Q to Quit", 36, COLORS["white"], WIDTH//4, HEIGHT*2//3)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.save_settings()
                        self.reset_game()
                        self.run()
                    if event.key == pygame.K_q:
                        self.save_settings()
                        pygame.quit()
                        quit()

if __name__ == "__main__":
    game = Game()
    game.run()