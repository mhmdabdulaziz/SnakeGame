import pygame, random, sys

# Initialize the game
pygame.init()
pygame.mixer.init()

# Set up the screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = "#000000"
LIGHT_GREEN = "#41644A"
DARK_GREEN = "#263A29"
BROWN = "#B8621B"
RED = "#F45050"
WHITE = "#FFFFFF"
ORANGE = "#E86A33"
BLUE = "#1A5F7A"
YELLOW = "#F9D949"
GRAY = "#F0F0F0"

# Define the Snake class
class Snake:
    def __init__(self):
        self.size = 1 #set the size of the snake as 1 (the head only)
        self.segments = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)] #set the position of the snake in the center of the screen
        
        #set the direction of the snake to the right
        self.DIR_X = 1
        self.DIR_Y = 0

    def move(self):
        POS_X, POS_Y = self.segments[0]
        POS_X += self.DIR_X * CELL_SIZE 
        POS_Y += self.DIR_Y * CELL_SIZE
        self.segments.insert(0, (POS_X, POS_Y))
        if len(self.segments) > self.size:
            self.segments.pop()

    def change_direction(self, DIR_X, DIR_Y):
        if DIR_X * -1 != self.DIR_X or DIR_Y * -1 != self.DIR_Y:
            self.DIR_X = DIR_X
            self.DIR_Y = DIR_Y

    def draw(self):
        for i, segment in enumerate(self.segments):
            POS_X, POS_Y = segment

            if i == 0:  # Head segment
                pygame.draw.circle(screen, BROWN, (POS_X + CELL_SIZE / 2, POS_Y + CELL_SIZE / 2), 10)
            elif i == len(self.segments) - 1:  # Tail segment
                pygame.draw.circle(screen, DARK_GREEN, (POS_X + CELL_SIZE / 2, POS_Y + CELL_SIZE / 2), 5)
            else:  # Body segment
                pygame.draw.circle(screen, LIGHT_GREEN, (POS_X + CELL_SIZE / 2, POS_Y + CELL_SIZE / 2), 10)
                pygame.draw.circle(screen, DARK_GREEN, (POS_X + CELL_SIZE / 2, POS_Y + CELL_SIZE / 2), 3)


    def check_collision(self):
        POS_X, POS_Y = self.segments[0]
        if POS_X < 0 or POS_X >= SCREEN_WIDTH or POS_Y < 0 or POS_Y >= SCREEN_HEIGHT:
            return True
        for segment in self.segments[1:]:
            if segment == (POS_X, POS_Y):
                return True
        return False

# Define the Food class
class Food:
    def __init__(self):
        self.POS_X = random.randint(0, SCREEN_WIDTH // CELL_SIZE - 1) * CELL_SIZE
        self.POS_Y = random.randint(0, SCREEN_HEIGHT // CELL_SIZE - 1) * CELL_SIZE
        self.shape = random.choice(['circle', 'rectangle', 'triangle'])  # Randomly select the shape

    def draw(self):
        if self.shape == 'circle':
            pygame.draw.circle(screen, ORANGE, (self.POS_X + CELL_SIZE // 2, self.POS_Y + CELL_SIZE // 2), CELL_SIZE // 2)
        elif self.shape == 'rectangle':
            pygame.draw.rect(screen, BLUE, (self.POS_X, self.POS_Y, CELL_SIZE, CELL_SIZE))
        elif self.shape == 'triangle':
            triangle_points = [
                (self.POS_X + CELL_SIZE // 2, self.POS_Y),
                (self.POS_X, self.POS_Y + CELL_SIZE),
                (self.POS_X + CELL_SIZE, self.POS_Y + CELL_SIZE)
            ]
            pygame.draw.polygon(screen, RED, triangle_points)

# Set up game variables
CELL_SIZE = 20
snake = Snake()
food = Food()
clock = pygame.time.Clock()
game_over = False
game_start = True
game_pause = False
game_quit = False
score = 0

#Load the sounds
pygame.mixer.music.load("./sounds/bg.mp3")
eat_sound = pygame.mixer.Sound("./sounds/eat.mp3")
collision_sound = pygame.mixer.Sound("./sounds/collision.mp3")

def pause_screen():
    screen.fill(BLACK)

    # Calculate the square dimensions
    square_size = min(SCREEN_WIDTH, SCREEN_HEIGHT) - 50
    square_x = (SCREEN_WIDTH - square_size) // 2
    square_y = (SCREEN_HEIGHT - square_size) // 2

    # Set the border color and thickness
    border_color = BROWN
    border_thickness = 5

    # Set the border radius
    border_radius = 10

    # Draw the rounded borders of the square
    pygame.draw.rect(screen, border_color, (square_x, square_y, square_size, square_size), border_thickness, border_radius)

    draw_text("Paused", 150, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60, BLUE)
    draw_text("Press SPACE to resume", 72, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, WHITE)

pygame.display.update()


# Define text rendering function
def draw_text(text, font_size, x, y, color):
    font = pygame.font.Font("./fonts/game_over.ttf", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Helper function to render score text
def render_score(score):
    # Load a font
    font = pygame.font.Font("./fonts/game_over.ttf", 100)
    score_text = "Score: " + str(score)
    score_surface = font.render(score_text, True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    screen.blit(score_surface, score_rect)

# Game loop
while not game_over: 
    while game_start:
        screen.fill(BLACK)

        # Calculate the square dimensions
        square_size = min(SCREEN_WIDTH, SCREEN_HEIGHT) - 50
        square_x = (SCREEN_WIDTH - square_size) // 2
        square_y = (SCREEN_HEIGHT - square_size) // 2

        # Set the border color and thickness
        border_color = BROWN
        border_thickness = 5

        # Set the border radius
        border_radius = 10

        # Draw the rounded borders of the square
        pygame.draw.rect(screen, border_color, (square_x, square_y, square_size, square_size), border_thickness, border_radius)
        
        draw_text("Snake Game", 150, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, ORANGE)
        draw_text("Press SPACE to start", 70, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_start = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_start = False

    while game_pause:
        pause_screen()

        # Stop the background music when the game is over
        pygame.mixer.music.pause()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_pause = False
                game_start = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_pause = False
                elif event.key == pygame.K_ESCAPE:
                    game_over = False
                    game_start = False
                    game_quit = True

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(0, -1)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(0, 1)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(1, 0)
            elif event.key == pygame.K_SPACE:
                game_pause = True
            elif event.key == pygame.K_ESCAPE:
                game_over = False
                game_start = False
                game_quit = True

    if not game_pause:
        # Start playing the background music if it's not already playing
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # -1 indicates looping indefinitely

        # Move the snake
        snake.move()

        # Check for collision with food
        if snake.segments[0] == (food.POS_X, food.POS_Y):
            snake.size += 1
            food = Food()
            score += 1
            eat_sound.play()

        # Check for collision with walls or itself
        if snake.check_collision():
            game_over = True

            # Play sound effect for collision
            collision_sound.play()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the snake and food
    snake.draw()
    food.draw()

    # Draw the score
    draw_text("Score: " + str(score), 24, 50, 20, WHITE)

    if game_over:
        # Stop the background music when the game is over
        pygame.mixer.music.stop()

        screen.fill(BLACK)

        # Calculate the square dimensions
        square_size = min(SCREEN_WIDTH, SCREEN_HEIGHT) - 60
        square_x = (SCREEN_WIDTH - square_size) // 2
        square_y = (SCREEN_HEIGHT - square_size) // 2

        # Set the border color and thickness
        border_color = BLUE
        border_thickness = 5

        # Set the border radius
        border_radius = 10

        # Draw the rounded borders of the square
        pygame.draw.rect(screen, border_color, (square_x, square_y, square_size, 400), border_thickness, border_radius)

        draw_text("Score: " + str(score), 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, WHITE)
        draw_text("Game Over", 200, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, RED)
        draw_text("Press SPACE to play again", 70, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
        draw_text("Press ESC to exit", 70, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30, WHITE)
        
        pygame.display.update()

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        snake = Snake()
                        food = Food()
                        score = 0
                        game_over = False
                        game_start = True
                    elif event.key == pygame.K_ESCAPE:
                        game_over = False
                        game_start = False
                        game_quit = True

    if game_quit:
        pygame.quit()
        sys.exit()

    if game_pause:
        pause_screen()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(10)


# Quit the game
pygame.quit()
