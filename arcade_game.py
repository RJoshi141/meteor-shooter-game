import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # Yellow color for the score number
NEON_BLUE = (0, 255, 255)  # Neon blue for both the rectangle and square
METEOR_COLORS = [(128, 128, 128), (169, 169, 169), (192, 192, 192)]  # Different shades of gray
FPS = 60
MAX_MISSED_METEORS = 10

# Load retro font
font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 16)
font_large = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 48)  # Adjusted size

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Shooter")

# Game Variables
gun_pos = [WIDTH // 2, HEIGHT - 50]
bullets = []
meteors = []
score = 0
missed_meteors = 0

def draw_gun():
    # Gun rectangle (body) with increased height
    pygame.draw.rect(screen, NEON_BLUE, pygame.Rect(gun_pos[0], gun_pos[1] + 20, 60, 20))
    # Gun square (top) with the same color
    pygame.draw.rect(screen, NEON_BLUE, pygame.Rect(gun_pos[0] + 20, gun_pos[1], 20, 20))

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, pygame.Rect(bullet[0], bullet[1], 5, 10))

def draw_meteors():
    for meteor in meteors:
        pygame.draw.ellipse(screen, meteor['color'], pygame.Rect(meteor['x'], meteor['y'], meteor['size'], meteor['size']))

def draw_score():
    # Render score text parts
    score_label = font.render("Score: ", True, WHITE)
    score_value = font.render(str(score), True, YELLOW)
    
    # Positioning the texts
    label_rect = score_label.get_rect(midright=(WIDTH // 2 - 10, 50))
    value_rect = score_value.get_rect(midleft=(WIDTH // 2 + 10, 50))
    
    # Draw texts on the screen
    screen.blit(score_label, label_rect)
    screen.blit(score_value, value_rect)

def draw_game_over():
    game_over_text = font_large.render("GAME OVER", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    
    # Draw the "GAME OVER" text with a retro outline
    outline_color = BLACK
    outline_width = 2
    
    # Outline effect
    for dx in [-outline_width, 0, outline_width]:
        for dy in [-outline_width, 0, outline_width]:
            if dx != 0 or dy != 0:
                screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2 + dx, HEIGHT // 2 - 100 + dy))
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    
    # Draw restart text
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

def handle_bullets():
    global score
    for bullet in bullets:
        bullet[1] -= 10
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            for meteor in meteors:
                meteor_rect = pygame.Rect(meteor['x'], meteor['y'], meteor['size'], meteor['size'])
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
                if bullet_rect.colliderect(meteor_rect):
                    meteors.remove(meteor)
                    bullets.remove(bullet)
                    score += meteor['points']
                    break

def handle_meteors():
    global missed_meteors
    for meteor in meteors:
        meteor['y'] += 5
        if meteor['y'] > HEIGHT:
            meteors.remove(meteor)
            missed_meteors += 1

def reset_game():
    global gun_pos, bullets, meteors, score, missed_meteors
    gun_pos = [WIDTH // 2, HEIGHT - 50]
    bullets = []
    meteors = []
    score = 0
    missed_meteors = 0

def main():
    global gun_pos
    clock = pygame.time.Clock()
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if game_over:
            if keys[pygame.K_r]:
                reset_game()
                game_over = False
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
        else:
            if keys[pygame.K_LEFT] and gun_pos[0] > 0:
                gun_pos[0] -= 5
            if keys[pygame.K_RIGHT] and gun_pos[0] < WIDTH - 60:
                gun_pos[0] += 5
            if keys[pygame.K_SPACE]:
                bullets.append([gun_pos[0] + 22, gun_pos[1]])

            screen.fill(BLACK)
            draw_gun()
            draw_bullets()
            draw_meteors()
            draw_score()
            handle_bullets()
            handle_meteors()

            if random.random() < 0.02:
                size = random.randint(20, 50)  # Random size between 20 and 50
                points = size // 10  # Points based on size
                meteors.append({
                    'x': random.randint(0, WIDTH - size),
                    'y': 0,
                    'size': size,
                    'color': random.choice(METEOR_COLORS),
                    'points': points
                })
            
            if missed_meteors >= MAX_MISSED_METEORS:
                game_over = True

            pygame.display.flip()
            clock.tick(FPS)

        if game_over:
            screen.fill(BLACK)
            draw_game_over()
            pygame.display.flip()

if __name__ == "__main__":
    reset_game()
    main()
