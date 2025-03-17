import pygame
import sys
import random
import math
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BEIGE = (245, 245, 220)

class Pin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.is_hit = False
        
    def draw(self, screen):
        if not self.is_hit:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
            pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius, 2)
            
    def check_collision(self, ball):
        distance = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)
        return distance < (self.radius + ball.radius) and not self.is_hit

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = BLUE
        self.speed_x = 0
        self.speed_y = 0
        self.moving = False
        self.power = 0
        self.angle = 0
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)
        
        # Draw power meter when not moving
        if not self.moving:
            pygame.draw.line(screen, RED, 
                            (self.x, self.y), 
                            (self.x + math.cos(self.angle) * self.power * 2, 
                             self.y + math.sin(self.angle) * self.power * 2), 
                            3)
        
    def update(self):
        if self.moving:
            self.x += self.speed_x
            self.y += self.speed_y
            
            # Apply friction
            self.speed_x *= 0.98
            self.speed_y *= 0.98
            
            # Check if ball has stopped
            if abs(self.speed_x) < 0.1 and abs(self.speed_y) < 0.1:
                self.speed_x = 0
                self.speed_y = 0
                self.moving = False
                
            # Check boundaries
            if self.x < self.radius:
                self.x = self.radius
                self.speed_x = -self.speed_x * 0.8
            elif self.x > SCREEN_WIDTH - self.radius:
                self.x = SCREEN_WIDTH - self.radius
                self.speed_x = -self.speed_x * 0.8
                
            if self.y < self.radius:
                self.y = self.radius
                self.speed_y = -self.speed_y * 0.8
            elif self.y > SCREEN_HEIGHT - self.radius:
                self.y = SCREEN_HEIGHT - self.radius
                self.speed_y = -self.speed_y * 0.8
                
    def throw(self):
        if not self.moving:
            self.speed_x = math.cos(self.angle) * (self.power / 5)
            self.speed_y = math.sin(self.angle) * (self.power / 5)
            self.moving = True
            
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.moving = False
        self.power = 0
        self.angle = -math.pi/2  # Pointing upward

class BowlingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bowling Game")
        self.clock = pygame.time.Clock()
        
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.pins = self.setup_pins()
        
        self.frame = 1
        self.throw_number = 1
        self.max_frames = 10
        self.scores = [0] * self.max_frames
        self.throws_history = []
        self.game_over = False
        
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
    def setup_pins(self):
        pins = []
        start_x = SCREEN_WIDTH // 2
        start_y = 100
        spacing = 40
        
        # Create a triangular formation of pins (4 rows)
        for row in range(4):
            for col in range(row + 1):
                x = start_x + (col - row/2) * spacing
                y = start_y + row * spacing
                pins.append(Pin(x, y))
                
        return pins
        
    def reset_pins(self):
        self.pins = self.setup_pins()
        
    def reset_ball(self):
        self.ball.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        
    def count_pins_hit(self):
        return sum(1 for pin in self.pins if pin.is_hit)
        
    def next_throw(self):
        pins_hit = self.count_pins_hit()
        self.throws_history.append(pins_hit)
        
        # Update score
        if self.throw_number == 1:
            if pins_hit == 10:  # Strike
                self.throw_number = 1
                self.frame += 1
                self.reset_pins()
            else:
                self.throw_number = 2
        else:  # Second throw
            self.throw_number = 1
            self.frame += 1
            self.reset_pins()
            
        self.reset_ball()
        
        # Check if game is over
        if self.frame > self.max_frames:
            self.game_over = True
            
    def calculate_score(self):
        throw_idx = 0
        for frame in range(self.max_frames):
            if throw_idx >= len(self.throws_history):
                break
                
            # Strike
            if self.throws_history[throw_idx] == 10:
                if throw_idx + 2 < len(self.throws_history):
                    self.scores[frame] = 10 + self.throws_history[throw_idx + 1] + self.throws_history[throw_idx + 2]
                throw_idx += 1
            # Spare
            elif throw_idx + 1 < len(self.throws_history) and self.throws_history[throw_idx] + self.throws_history[throw_idx + 1] == 10:
                if throw_idx + 2 < len(self.throws_history):
                    self.scores[frame] = 10 + self.throws_history[throw_idx + 2]
                throw_idx += 2
            # Open frame
            else:
                if throw_idx + 1 < len(self.throws_history):
                    self.scores[frame] = self.throws_history[throw_idx] + self.throws_history[throw_idx + 1]
                throw_idx += 2
                
    def draw_lane(self):
        # Draw bowling lane
        pygame.draw.rect(self.screen, BEIGE, (100, 50, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
        pygame.draw.rect(self.screen, BROWN, (100, 50, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100), 10)
        
        # Draw gutters
        pygame.draw.rect(self.screen, BLACK, (90, 50, 10, SCREEN_HEIGHT - 100))
        pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH - 100, 50, 10, SCREEN_HEIGHT - 100))
        
    def draw_scoreboard(self):
        # Draw scoreboard background
        pygame.draw.rect(self.screen, WHITE, (10, 10, SCREEN_WIDTH - 20, 80))
        pygame.draw.rect(self.screen, BLACK, (10, 10, SCREEN_WIDTH - 20, 80), 2)
        
        # Draw frame numbers
        for i in range(self.max_frames):
            x = 20 + i * 75
            pygame.draw.rect(self.screen, WHITE, (x, 20, 70, 60))
            pygame.draw.rect(self.screen, BLACK, (x, 20, 70, 60), 2)
            
            # Frame number
            frame_text = self.small_font.render(f"Frame {i+1}", True, BLACK)
            self.screen.blit(frame_text, (x + 10, 25))
            
            # Score
            if i < len(self.scores) and self.scores[i] > 0:
                score_text = self.font.render(str(self.scores[i]), True, BLACK)
                self.screen.blit(score_text, (x + 25, 45))
                
    def draw_game_info(self):
        # Draw current frame and throw info
        frame_text = self.font.render(f"Frame: {self.frame}", True, WHITE)
        throw_text = self.font.render(f"Throw: {self.throw_number}", True, WHITE)
        
        self.screen.blit(frame_text, (20, SCREEN_HEIGHT - 40))
        self.screen.blit(throw_text, (150, SCREEN_HEIGHT - 40))
        
        # Draw power meter
        power_text = self.small_font.render(f"Power: {self.ball.power}", True, WHITE)
        self.screen.blit(power_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40))
        
        # Draw instructions
        if not self.ball.moving:
            instructions = self.small_font.render("UP/DOWN: Adjust power, LEFT/RIGHT: Aim, SPACE: Throw", True, WHITE)
            self.screen.blit(instructions, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 40))
            
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, WHITE)
        total_score = sum(self.scores)
        score_text = self.font.render(f"Final Score: {total_score}", True, WHITE)
        restart_text = self.font.render("Press R to restart or Q to quit", True, WHITE)
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
        
    def run(self):
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.ball.moving and not self.game_over:
                        self.ball.throw()
                    elif event.key == pygame.K_r and self.game_over:
                        self.__init__()  # Reset the game
                    elif event.key == pygame.K_q and self.game_over:
                        running = False
                        
            # Handle continuous key presses
            if not self.ball.moving and not self.game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.ball.power = min(self.ball.power + 1, 50)
                if keys[pygame.K_DOWN]:
                    self.ball.power = max(self.ball.power - 1, 0)
                if keys[pygame.K_LEFT]:
                    self.ball.angle = max(self.ball.angle - 0.05, -math.pi)
                if keys[pygame.K_RIGHT]:
                    self.ball.angle = min(self.ball.angle + 0.05, 0)
                    
            # Update
            self.ball.update()
            
            # Check for collisions with pins
            if self.ball.moving:
                for pin in self.pins:
                    if pin.check_collision(self.ball):
                        pin.is_hit = True
                        
                        # Add some randomness to ball direction after hitting a pin
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(0.5, 2)
                        self.ball.speed_x += math.cos(angle) * speed
                        self.ball.speed_y += math.sin(angle) * speed
                        
                # Check if ball has stopped moving
                if not self.ball.moving and not self.game_over:
                    self.next_throw()
                    self.calculate_score()
                    
            # Draw
            self.screen.fill(BLACK)
            self.draw_lane()
            
            # Draw pins
            for pin in self.pins:
                pin.draw(self.screen)
                
            # Draw ball
            self.ball.draw(self.screen)
            
            # Draw UI
            self.draw_scoreboard()
            self.draw_game_info()
            
            if self.game_over:
                self.draw_game_over()
                
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BowlingGame()
    game.run()