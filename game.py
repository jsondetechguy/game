import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)

# Game variables
GRAVITY = 0.25
BIRD_JUMP = -6.5
PIPE_GAP = 150
PIPE_WIDTH = 60
PIPE_SPEED = 3
FPS = 60

# Bird settings
bird_img = pygame.image.load("flappybird.png") 
if pygame.image.get_extended():
    bird_img = pygame.transform.scale(bird_img, (34, 24)) 
pygame.draw.ellipse(bird_img, (255, 255, 0), [0, 0, 34, 24])
bird_rect = bird_img.get_rect(center=(80, HEIGHT // 2))

# Font
font = pygame.font.SysFont(None, 48)

def draw_text(text, x, y):
    img = font.render(text, True, (255, 0, 0))
    SCREEN.blit(img, (x, y))

def create_pipe():
    height = random.randint(100, HEIGHT - PIPE_GAP - 100)
    top = pygame.Rect(WIDTH, 0, PIPE_WIDTH, height)
    bottom = pygame.Rect(WIDTH, height + PIPE_GAP, PIPE_WIDTH, HEIGHT - height - PIPE_GAP)
    return top, bottom

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= PIPE_SPEED
    return [pipe for pipe in pipes if pipe.right > 0]

def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        return True
    return False

def main():
    clock = pygame.time.Clock()
    bird = bird_rect.copy()
    bird_movement = 0
    pipes = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1200)
    score = 0
    running = True
    game_active = True
    bird_img.blit(bird_img, bird)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_movement = BIRD_JUMP
                if event.type == SPAWNPIPE:
                    top, bottom = create_pipe()
                    pipes.extend([top, bottom])
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    main()
                    return

        if game_active:
            bird_movement += GRAVITY
            bird.centery += int(bird_movement)

            pipes = move_pipes(pipes)

            # Score
            for pipe in pipes:
                if pipe.centerx == bird.centerx and pipe.y == 0:
                    score += 1

            game_active = not check_collision(bird, pipes)

        # Drawing
        SCREEN.fill(BLUE)
        SCREEN.blit(bird_img, bird)
        for pipe in pipes:
            pygame.draw.rect(SCREEN, GREEN, pipe)
        draw_text(str(score), WIDTH // 2 - 20, 20)

        if not game_active:
            draw_text("Game Over", WIDTH // 2 - 100, HEIGHT // 2 - 40)
            draw_text("Press SPACE", WIDTH // 2 - 120, HEIGHT // 2 + 10)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()