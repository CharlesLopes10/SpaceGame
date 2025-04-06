import pygame
import sys
import random

pygame.init()

# Configurações
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 120, 255)
RED = (255, 0, 0)

# Fontes
font_big = pygame.font.SysFont("arial", 60)
font_small = pygame.font.SysFont("arial", 36)

# Imagens
nave1 = pygame.image.load("nave1.png")
nave2 = pygame.image.load("nave2.png")
inimigo_img = pygame.image.load("inimigo.png")
bg1 = pygame.image.load("bg1.png")
bg2 = pygame.image.load("bg2.png")

# Musicas
def tocar_musica(caminho):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play(-1)

# Classes
class Nave:
    def __init__(self):
        self.image = nave1
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 5
        self.bullets = []
        self.score = 0
        self.level = 1
        self.lives = 3

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = pygame.Rect(self.rect.centerx - 2, self.rect.top, 4, 10)
        self.bullets.append(bullet)

    def draw(self):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(screen, WHITE, bullet)

class Inimigo:
    def __init__(self):
        self.image = inimigo_img
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), -50))
        self.speed = 3
        self.bullets = []

    def update(self):
        self.rect.y += self.speed
        if random.randint(0, 100) < 2:
            self.shoot()

    def shoot(self):
        bullet = pygame.Rect(self.rect.centerx - 2, self.rect.bottom, 4, 10)
        self.bullets.append(bullet)

    def draw(self):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(screen, RED, bullet)

# Menu
def draw_button(text, rect, hovered):
    color = BLUE if hovered else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = font_small.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def main_menu():
    global play_button, exit_button
    clock = pygame.time.Clock()
    while True:
        screen.blit(menu_bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse_pos):
                    return
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit(); sys.exit()

        screen.blit(menu_bg, (0, 0))

        title = font_big.render("SPACE GAME", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))

        play_button = pygame.Rect(WIDTH // 2 - 100, 280, 200, 60)
        exit_button = pygame.Rect(WIDTH // 2 - 100, 370, 200, 60)

        draw_button("New Game", play_button, play_button.collidepoint(mouse_pos))
        draw_button("Exit", exit_button, exit_button.collidepoint(mouse_pos))

        pygame.display.flip()
        clock.tick(60)

# Jogo
def game_loop():
    clock = pygame.time.Clock()
    player = Nave()
    inimigos = []

    background = bg1
    running = True

    while running:
        screen.blit(background, (0, 0))

        # movimento da nave com as setas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= player.speed
        if keys[pygame.K_RIGHT]:
            player.rect.x += player.speed
        if keys[pygame.K_UP]:
            player.rect.y -= player.speed
        if keys[pygame.K_DOWN]:
            player.rect.y += player.speed

        # movimento da nave com A, W, S, D
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.rect.x -= player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.rect.x += player.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.rect.y -= player.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.rect.y += player.speed

        # Impede que a nave saia da tela
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > HEIGHT:
            player.rect.bottom = HEIGHT

        #Eventos
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Atualizar jogador
        player.update(keys)
        for bullet in player.bullets[:]:
            bullet.y -= 8
            if bullet.y < 0:
                player.bullets.remove(bullet)

        # Criar inimigos
        if random.randint(0, 30) < 2:
            inimigos.append(Inimigo())

        # Atualizar inimigos
        for inimigo in inimigos[:]:
            inimigo.update()
            if inimigo.rect.top > HEIGHT:
                inimigos.remove(inimigo)

            for bullet in inimigo.bullets[:]:
                bullet.y += 5
                if bullet.colliderect(player.rect):
                    inimigo.bullets.remove(bullet)
                    player.lives -= 1
                    if player.lives <= 0:
                        pygame.time.delay(1000)
                        return  # volta para o menu

                elif bullet.y > HEIGHT:
                    inimigo.bullets.remove(bullet)

        # Colisão jogador vs inimigo
        for inimigo in inimigos[:]:
            for bullet in player.bullets:
                if bullet.colliderect(inimigo.rect):
                    player.score += 10
                    inimigos.remove(inimigo)
                    if bullet in player.bullets:
                        player.bullets.remove(bullet)

        # Troca de nível
        if player.score >= 100 and player.level == 1:
            player.image = nave2
            background = bg2
            player.level = 2
            tocar_musica("level2.mp3")

        if player.level == 1:
            level_text = font_small.render("Level 1", True, WHITE)
            screen.blit(level_text, (WIDTH - 150, 10))

        if player.level == 2:
            level_text = font_small.render("Level 2", True, WHITE)
            screen.blit(level_text, (WIDTH - 150, 10))

        # Desenhar
        player.draw()
        for inimigo in inimigos:
            inimigo.draw()

        # HUD
        score_text = font_small.render(f"Score: {player.score}", True, WHITE)
        lives_text = font_small.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)




# Executar menu e jogo
while True:
    menu_bg = pygame.image.load("menu_bg.png").convert()
    tocar_musica("menu.mp3")
    main_menu()
    tocar_musica("level1.mp3")
    game_loop()