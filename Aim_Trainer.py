import math
import random
import time
import pygame

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BG_COLOR = (0, 25, 40)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Font
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

# Target properties
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

# Player properties
LIVES = 3
TOP_BAR_HEIGHT = 50

# Define the Target class
class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = RED

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        # Update the size of the target
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        # Draw the target on the window
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)

    def collide(self, x, y):
        # Check if a point (x, y) collides with the target
        dis = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return dis <= self.size

# Function to draw targets on the window
def draw(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

# Function to format time as string
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"

# Function to draw the top bar showing time, hits, and lives
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, GRAY, (0, 0, WIDTH, TOP_BAR_HEIGHT))

    # Render labels
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", True, WHITE)
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", True, WHITE)
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", True, WHITE)

    # Blit labels
    win.blit(time_label, (10, 10))
    win.blit(hits_label, (WIDTH // 2 - hits_label.get_width() // 2, 10))
    win.blit(lives_label, (WIDTH - lives_label.get_width() - 10, 10))

# Function to display the end screen when the game is over
def end_screen(win, elapsed_time, targets_pressed, clicks):
    # End screen GUI
    win.fill(BG_COLOR)
    end_text = LABEL_FONT.render("Game Over!", True, WHITE)
    win.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 3))

    # Results
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", True, WHITE)
    win.blit(hits_label, (WIDTH // 2 - hits_label.get_width() // 2, HEIGHT // 2))

    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(
        f"Accuracy: {accuracy}%", True, WHITE)
    win.blit(accuracy_label, (WIDTH // 2 - accuracy_label.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.update()

    # Wait for quit event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Main function where the game loop resides
def main():
    # Initialize variables
    run = True
    targets = []
    clock = pygame.time.Clock()
    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    # Initialize window
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aim Trainer")

    # Timer for generating new targets
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    # Main game loop
    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        # Update targets
        for target in targets:
            target.update()
            if target.size <= 0:
                targets.remove(target)
                misses += 1
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        # End condition
        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        # Draw everything
        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
