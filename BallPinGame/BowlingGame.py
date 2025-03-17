import random
import time
import os

class BowlingGame:
    def __init__(self):
        self.total_frames = 10
        self.current_frame = 1
        self.pins = 10
        self.score = 0
        self.frame_scores = [0] * self.total_frames
        self.throws = []
        self.frame_throws = []
        self.game_over = False
        
    def reset_pins(self):
        """Reset pins for a new frame"""
        self.pins = 10
        
    def throw_ball(self):
        """Simulate throwing a ball and knocking down pins"""
        # If all pins are already down, return 0
        if self.pins == 0:
            return 0
            
        # Simulate knocking down random number of pins
        knocked_down = random.randint(0, self.pins)
        self.pins -= knocked_down
        
        # Add throw to current frame
        self.frame_throws.append(knocked_down)
        self.throws.append(knocked_down)
        
        return knocked_down
        
    def is_strike(self):
        """Check if the current throw is a strike"""
        return len(self.frame_throws) == 1 and self.frame_throws[0] == 10
        
    def is_spare(self):
        """Check if the current frame is a spare"""
        return len(self.frame_throws) == 2 and sum(self.frame_throws) == 10
        
    def calculate_frame_score(self, frame_index):
        """Calculate score for a specific frame"""
        throw_index = 0
        score = 0
        
        # Calculate throw index for the current frame
        for i in range(frame_index):
            if i < frame_index - 1:
                # For previous frames, add number of throws
                if self.is_strike_at(i):
                    throw_index += 1
                else:
                    throw_index += 2
            else:
                # For current frame
                throw_index = throw_index
                
        # Calculate score based on frame type
        if self.is_strike_at(frame_index):
            # Strike: 10 + next two throws
            score = 10
            if len(self.throws) > throw_index + 2:
                score += self.throws[throw_index + 1] + self.throws[throw_index + 2]
        elif self.is_spare_at(frame_index):
            # Spare: 10 + next throw
            score = 10
            if len(self.throws) > throw_index + 2:
                score += self.throws[throw_index + 2]
        else:
            # Open frame: sum of two throws
            if throw_index + 1 < len(self.throws):
                score = self.throws[throw_index] + self.throws[throw_index + 1]
            elif throw_index < len(self.throws):
                score = self.throws[throw_index]
                
        return score
        
    def is_strike_at(self, frame_index):
        """Check if a specific frame is a strike"""
        throw_index = 0
        for i in range(frame_index):
            if self.is_strike_at(i):
                throw_index += 1
            else:
                throw_index += 2
                
        return throw_index < len(self.throws) and self.throws[throw_index] == 10
        
    def is_spare_at(self, frame_index):
        """Check if a specific frame is a spare"""
        throw_index = 0
        for i in range(frame_index):
            if self.is_strike_at(i):
                throw_index += 1
            else:
                throw_index += 2
                
        return (throw_index + 1 < len(self.throws) and 
                self.throws[throw_index] + self.throws[throw_index + 1] == 10 and
                self.throws[throw_index] != 10)
        
    def next_frame(self):
        """Move to the next frame"""
        self.current_frame += 1
        self.frame_throws = []
        self.reset_pins()
        
    def update_score(self):
        """Update the total score"""
        self.score = sum(self.frame_scores)
        
    def play_frame(self):
        """Play a single frame"""
        print(f"\nFrame {self.current_frame}")
        print("-" * 20)
        
        # First throw
        input("Press Enter to throw the ball...")
        pins_down = self.throw_ball()
        print(f"You knocked down {pins_down} pins!")
        
        # Check for strike
        if self.is_strike():
            print("STRIKE!")
            self.next_frame()
            return
            
        # Second throw
        input("Press Enter for your second throw...")
        pins_down = self.throw_ball()
        print(f"You knocked down {pins_down} pins!")
        
        # Check for spare
        if self.is_spare():
            print("SPARE!")
            
        self.next_frame()
        
    def play_final_frame(self):
        """Play the final (10th) frame with special rules"""
        print("\nFinal Frame")
        print("-" * 20)
        
        # First throw
        input("Press Enter to throw the ball...")
        pins_down = self.throw_ball()
        print(f"You knocked down {pins_down} pins!")
        
        # Check for strike
        if self.is_strike():
            print("STRIKE!")
            self.reset_pins()  # Reset pins for bonus throw
            
            # First bonus throw
            input("Bonus throw! Press Enter...")
            pins_down = self.throw_ball()
            print(f"You knocked down {pins_down} pins!")
            
            # Check for another strike
            if pins_down == 10:
                print("STRIKE!")
                self.reset_pins()  # Reset pins for second bonus throw
            
            # Second bonus throw
            input("Final bonus throw! Press Enter...")
            pins_down = self.throw_ball()
            print(f"You knocked down {pins_down} pins!")
            
            self.game_over = True
            return
            
        # Second throw
        input("Press Enter for your second throw...")
        pins_down = self.throw_ball()
        print(f"You knocked down {pins_down} pins!")
        
        # Check for spare
        if self.is_spare():
            print("SPARE!")
            self.reset_pins()  # Reset pins for bonus throw
            
            # Bonus throw
            input("Bonus throw! Press Enter...")
            pins_down = self.throw_ball()
            print(f"You knocked down {pins_down} pins!")
            
        self.game_over = True
        
    def calculate_total_score(self):
        """Calculate the total score for all frames"""
        for i in range(self.total_frames):
            self.frame_scores[i] = self.calculate_frame_score(i)
        self.update_score()
        
    def display_scoreboard(self):
        """Display the current scoreboard"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 40)
        print("BOWLING SCOREBOARD")
        print("=" * 40)
        
        # Display frame numbers
        print("Frame:", end=" ")
        for i in range(1, self.total_frames + 1):
            print(f"{i:^4}", end=" ")
        print()
        
        # Display frame scores
        print("Score:", end=" ")
        for i in range(self.total_frames):
            if i < self.current_frame - 1 or self.game_over:
                print(f"{self.frame_scores[i]:^4}", end=" ")
            else:
                print(f"{'':^4}", end=" ")
        print()
        
        # Display total score
        print("-" * 40)
        print(f"Total Score: {self.score}")
        print("=" * 40)
        
    def play_game(self):
        """Play a complete game of bowling"""
        print("Welcome to Python Bowling!")
        print("=" * 40)
        
        while not self.game_over:
            self.display_scoreboard()
            
            if self.current_frame < self.total_frames:
                self.play_frame()
            else:
                self.play_final_frame()
                
            self.calculate_total_score()
            time.sleep(1)
            
        # Final scoreboard
        self.display_scoreboard()
        print("\nGame Over!")
        print(f"Your final score is: {self.score}")
        
        if self.score >= 200:
            print("Amazing game! You're a bowling pro!")
        elif self.score >= 150:
            print("Great game! You've got skills!")
        elif self.score >= 100:
            print("Good game! Keep practicing!")
        else:
            print("Nice try! Better luck next time!")

# Run the game if this script is executed directly
if __name__ == "__main__":
    game = BowlingGame()
    game.play_game()