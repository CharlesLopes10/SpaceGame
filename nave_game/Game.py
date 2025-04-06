import pygame
import sys
import random

from pygame.examples.music_drop_fade import draw_text_line

pygame.init()

# set window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 40)

# uploads image
ship_img1 = pygame.image.load("nave1.png")
ship_img2 = pygame.image.load("nave2.png")
bg1 = pygame.image.load("bg1.jpg")
bg2 = pygame.image.load("bg2.jpg")
enemy_img = pygame.image.load("enemy.png")

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship_img1
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 5

    def update(self, level):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if level == 2:
            self.image = ship_img2

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH-20), -40))
        self.speed = random.randint(3, 6)

    def update(text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        rect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, rect)

    def game_loop():
        player = Player()
        enemies = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group(player)

        for _ in range(5):
            e = Enemy()
            enemies.add(e)
            all_sprites.add(e)

        score = 0
        level = 1
        running = True

        while running:
            clock.tick(60)
            screen.blit(bg1 if level == 1 else bg2, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            all_sprites.update()
            player.update()

            # Collision and points
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    score += 1
                    enemy.rect.y = -40
                    enemy.rect.x = random.randint(20, WIDTH - 20)

            if score >= 10:
                level = 2

            all_sprites.draw(screen)
            draw_text_line(f'Score: {score}', font, WHITE, screen, 70, 30)
            draw_text_line(f'Level: {level}', font, WHITE, screen, WIDTH - 100, 30)
            pygame.display.flip()

    def main_menu():
        while True:
            screen.fill(BLACK)
            draw_text_line('SPACE GAME', font, WHITE, screen, WIDTH//2, HEIGHT//3)
            draw_text_line('Press ENTER to Start (Player 1)', font, WHITE, screen, WIDTH//2, HEIGHT//2)
            draw_text_line('Press ESC to Exit', font, WHITE, screen, WIDTH//2, HEIGHT//2 + 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            clock.tick(60)

    # START SPACE GAME
    main_menu()