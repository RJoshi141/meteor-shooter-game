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
NEON_BLUE = (0, 255, 255)  # Neon blue for both the rectangle and square
METEOR_COLORS = [(128, 128, 128), (169, 169, 169), (192, 192, 192)]  # Different shades of gray
FPS = 60

# Initialize the screen and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Shooter")
font = pygame.font.Font(None, 36)

# Game Variables
gun_pos = [WIDTH // 2, HEIGHT - 50]
bullets = []
meteors = []
score = 0

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
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

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
    for meteor in meteors:
        meteor['y'] += 5
        if meteor['y'] > HEIGHT:
            meteors.remove(meteor)

def main():
    global gun_pos
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
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
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
