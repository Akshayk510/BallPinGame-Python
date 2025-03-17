# Ball Pin Game Collection

This collection contains three different implementations of a ball pin game, ranging from a simple text-based bowling game to more advanced visual implementations using Pygame.

## Game Versions

### 1. BowlingGame.py
A text-based bowling game that follows standard bowling rules:
- 10 frames
- Scoring with strikes and spares
- Final frame bonus throws
- Simple text-based interface

**How to run:**
```
python BowlingGame.py
```

**Controls:**
- Press Enter to throw the ball
- The pins knocked down are randomly determined

### 2. BowlingGameVisual.py
A visual bowling game with full bowling rules and physics:
- 10 frames with proper bowling scoring
- Visual representation of the lane, pins, and ball
- Aiming and power control
- Physics-based pin collisions

**Requirements:**
- Pygame library (`pip install pygame`)

**How to run:**
```
python BowlingGameVisual.py
```

**Controls:**
- UP/DOWN arrows: Adjust throwing power
- LEFT/RIGHT arrows: Adjust throwing angle
- SPACE: Throw the ball
- R: Restart game (after game over)
- Q: Quit game (after game over)

### 3. SimplePinGame.py
A simplified pin game focused on knocking down pins:
- No frame system, just continuous play
- Score based on number of pins knocked down
- Physics-based collisions
- Visual representation with aiming system

**Requirements:**
- Pygame library (`pip install pygame`)

**How to run:**
```
python SimplePinGame.py
```

**Controls:**
- UP/DOWN arrows: Adjust throwing power
- LEFT/RIGHT arrows: Adjust throwing angle
- SPACE: Throw the ball
- R: Reset pins and ball

## Game Mechanics

### Bowling Scoring
- Strike (all 10 pins on first throw): 10 + the value of your next two throws
- Spare (all 10 pins using two throws): 10 + the value of your next throw
- Open frame: Total pins knocked down in the frame
- Maximum score: 300 points (12 strikes in a row)

### Physics
The visual games use simplified physics including:
- Momentum transfer from ball to pins
- Friction to slow the ball
- Collision detection between ball and pins
- Gravity effect on falling pins

## Tips
- In the visual games, adjust your power and angle carefully for the best results
- Try to aim slightly off-center for the best chance to knock down all pins
- In bowling, consistency is key - find an angle and power that works for you

Enjoy playing!
