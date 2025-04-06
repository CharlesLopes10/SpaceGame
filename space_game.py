
import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

ship_img1 = pygame.image.load("nave1.png")
ship_img2 = pygame.image.load("nave2.png")
bg1 = pygame.image.load("bg1.jpg")
bg2 = pygame.image.load("bg2.jpg")
enemy_img = pygame.image.load("inimigo.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship_img1
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 5
        self.lives = 3

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
        self.speed = random.randint(2, 4)
        self.shoot_delay = random.randint(60, 180)
        self.shoot_timer = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = -40
            self.rect.x = random.randint(20, WIDTH-20)
        self.shoot_timer += 1

    def can_shoot(self):
        return self.shoot_timer >= self.shoot_delay

    def reset_shoot_timer(self):
        self.shoot_timer = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color=WHITE):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = direction * 8

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    rect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, rect)

def draw_lives(surface, lives, x, y):
    for i in range(lives):
        pygame.draw.rect(surface, RED, (x + 30 * i, y, 20, 20))

def game_loop():
    player = Player()
    enemies = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    for _ in range(6):
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
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top, -1)
                    player_bullets.add(bullet)
                    all_sprites.add(bullet)

        all_sprites.update()
        player.update(level)

        # Tiros inimigos
        for enemy in enemies:
            if enemy.can_shoot():
                bullet = Bullet(enemy.rect.centerx, enemy.rect.bottom, 1, RED)
                enemy_bullets.add(bullet)
                all_sprites.add(bullet)
                enemy.reset_shoot_timer()

        # Colisão tiro jogador -> inimigo
        hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
        for hit in hits:
            score += 1
            e = Enemy()
            enemies.add(e)
            all_sprites.add(e)

        # Colisão tiro inimigo -> jogador
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            player.lives -= 1
            if player.lives <= 0:
                draw_text('GAME OVER', font, RED, screen, WIDTH//2, HEIGHT//2)
                pygame.display.flip()
                pygame.time.wait(2000)
                return

        if score >= 10:
            level = 2

        all_sprites.draw(screen)
        draw_text(f'Score: {score}', font, WHITE, screen, 70, 30)
        draw_text(f'Level: {level}', font, WHITE, screen, WIDTH - 100, 30)
        draw_lives(screen, player.lives, WIDTH // 2 - 50, 10)

        pygame.display.flip()

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text('SPACE GAME', font, WHITE, screen, WIDTH//2, HEIGHT//3)
        draw_text('Press ENTER to Start (Player 1)', font, WHITE, screen, WIDTH//2, HEIGHT//2)
        draw_text('Press ESC to Exit', font, WHITE, screen, WIDTH//2, HEIGHT//2 + 50)

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

main_menu()
