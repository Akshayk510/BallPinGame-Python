import pygame
import sys
import random
import math

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
GRAY = (200, 200, 200)

class Pin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.is_hit = False
        self.velocity_x = 0
        self.velocity_y = 0
        
    def draw(self, screen):
        if not self.is_hit:
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)
        else:
            # Draw falling pin
            self.x += self.velocity_x
            self.y += self.velocity_y
            self.velocity_y += 0.2  # Gravity
            
            if self.y > SCREEN_HEIGHT + self.radius:
                return False  # Pin is off-screen
                
            pygame.draw.circle(screen, GRAY, (int(self.x), int(self.y)), self.radius)
            
        return True
            
    def check_collision(self, ball):
        if self.is_hit:
            return False
            
        distance = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)
        if distance < (self.radius + ball.radius):
            self.is_hit = True
            
            # Calculate angle of impact
            angle = math.atan2(self.y - ball.y, self.x - ball.x)
            force = 5
            
            # Set velocity based on impact
            self.velocity_x = math.cos(angle) * force
            self.velocity_y = math.sin(angle) * force
            
            return True
        return False

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = BLUE
        self.velocity_x = 0
        self.velocity_y = 0
        self.moving = False
        self.power = 0
        self.angle = -math.pi/2  # Pointing upward
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw aiming line when not moving
        if not self.moving:
            end_x = self.x + math.cos(self.angle) * self.power * 3
            end_y = self.y + math.sin(self.angle) * self.power * 3
            pygame.draw.line(screen, RED, (self.x, self.y), (end_x, end_y), 3)
        
    def update(self):
        if self.moving:
            # Update position
            self.x += self.velocity_x
            self.y += self.velocity_y
            
            # Apply friction
            self.velocity_x *= 0.98
            self.velocity_y *= 0.98
            
            # Check if ball has stopped
            if abs(self.velocity_x) < 0.1 and abs(self.velocity_y) < 0.1:
                self.velocity_x = 0
                self.velocity_y = 0
                self.moving = False
                
            # Check boundaries
            if self.x < self.radius:
                self.x = self.radius
                self.velocity_x = -self.velocity_x * 0.8
            elif self.x > SCREEN_WIDTH - self.radius:
                self.x = SCREEN_WIDTH - self.radius
                self.velocity_x = -self.velocity_x * 0.8
                
            if self.y < self.radius:
                self.y = self.radius
                self.velocity_y = -self.velocity_y * 0.8
            elif self.y > SCREEN_HEIGHT - self.radius:
                self.y = SCREEN_HEIGHT - self.radius
                self.velocity_y = -self.velocity_y * 0.8
                
    def throw(self):
        if not self.moving:
            self.velocity_x = math.cos(self.angle) * (self.power / 5)
            self.velocity_y = math.sin(self.angle) * (self.power / 5)
            self.moving = True
            
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.moving = False
        self.power = 20  # Default power
        self.angle = -math.pi/2  # Pointing upward

class PinGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ball Pin Game")
        self.clock = pygame.time.Clock()
        
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.pins = []
        self.setup_pins()
        
        self.score = 0
        self.throws = 0
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
    def setup_pins(self):
        self.pins = []
        
        # Create a triangular formation of pins
        rows = 4
        spacing = 40
        start_x = SCREEN_WIDTH // 2
        start_y = 100
        
        for row in range(rows):
            for col in range(row + 1):
                x = start_x + (col - row/2) * spacing
                y = start_y + row * spacing
                self.pins.append(Pin(x, y))
                
    def reset_game(self):
        self.setup_pins()
        self.ball.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.throws += 1
        
    def draw_background(self):
        # Draw a simple background
        self.screen.fill(GREEN)
        
        # Draw the playing area
        pygame.draw.rect(self.screen, GRAY, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        
    def draw_ui(self):
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        throws_text = self.font.render(f"Throws: {self.throws}", True, BLACK)
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(throws_text, (20, 60))
        
        # Draw instructions
        if not self.ball.moving:
            instructions = self.small_font.render("UP/DOWN: Adjust power, LEFT/RIGHT: Aim, SPACE: Throw, R: Reset", True, BLACK)
            self.screen.blit(instructions, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 30))
        
    def run(self):
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.ball.moving:
                        self.ball.throw()
                    elif event.key == pygame.K_r:
                        self.reset_game()
                        
            # Handle continuous key presses
            if not self.ball.moving:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.ball.power = min(self.ball.power + 1, 50)
                if keys[pygame.K_DOWN]:
                    self.ball.power = max(self.ball.power - 1, 5)
                if keys[pygame.K_LEFT]:
                    self.ball.angle = max(self.ball.angle - 0.05, -math.pi)
                if keys[pygame.K_RIGHT]:
                    self.ball.angle = min(self.ball.angle + 0.05, 0)
                    
            # Update
            self.ball.update()
            
            # Check for collisions with pins
            pins_hit_this_frame = 0
            for pin in self.pins:
                if pin.check_collision(self.ball):
                    pins_hit_this_frame += 1
                    
            # Update score
            self.score += pins_hit_this_frame
            
            # Draw
            self.draw_background()
            
            # Draw pins (and remove any that are off-screen)
            self.pins = [pin for pin in self.pins if pin.draw(self.screen)]
            
            # Draw ball
            self.ball.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            # Check if all pins are hit
            if all(pin.is_hit for pin in self.pins) and not self.ball.moving:
                # Wait a moment before resetting
                pygame.display.flip()
                pygame.time.wait(1000)
                self.reset_game()
                
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PinGame()
    game.run()