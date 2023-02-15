import pygame
import random
import os

WIDTH = 600
HEIGHT = 450
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarWars")
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

ship_menu_1 = pygame.image.load(os.path.join(img_folder, 'ship1g.png'))
exit_menu = pygame.image.load(os.path.join(img_folder, 'exit.png'))
ship_img = pygame.image.load(os.path.join(img_folder, 'ship.png'))
fon_img = pygame.image.load(os.path.join(img_folder, 'space.jpg'))
enemy_img = pygame.image.load(os.path.join(img_folder, 'enemy.png'))
bullet_img = pygame.image.load(os.path.join(img_folder, 'missiles.png'))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shield = 100
        self.image = ship_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10

    def update(self):
        x_pl, y_pl = pygame.mouse.get_pos()
        self.rect.x = x_pl - ship_img.get_width()/2
        self.rect.y = y_pl - ship_img.get_height()/2

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

def new_enemy():
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)

for i in range(5):
    new_enemy()

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0, 255, 0), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

def show_go_screen():
    screen.blit(fon_img, (0, 0))
    draw_text(screen, "Game Over!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Управляй и стреляй мышкой", 22,
              WIDTH / 2, HEIGHT / 1.9)
    draw_text(screen, "Нажми любую клавишу, чтобы начать", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def start_menu():
    global menu, ship_menu, running
    screen.blit(fon_img, (0, 0))
    sh1 = screen.blit(ship_menu_1, (WIDTH *0.15, HEIGHT *0.2))
    ex =  screen.blit(exit_menu, (WIDTH *0.6, HEIGHT *0.4))
    draw_text(screen, "Нажми на корабль для старта, EXIT - для выхода", 22,  WIDTH / 2, HEIGHT * 0.1)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if sh1.collidepoint(pos):
                    menu = False
                    waiting = False
                elif ex.collidepoint(pos):
                    running = False
                    waiting = False

score = 0

menu = True
game_over = False
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(5):
            new_enemy()
        score = 0
        menu = True

    if menu:
        start_menu()


    clock.tick(FPS)
    screen.blit(fon_img, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot()


    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 1
        new_enemy()

    hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    if hits:
        player.shield -= 25
        new_enemy()
        if player.shield <= 0:
            game_over = True


    
    all_sprites.update()
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH*0.09 , 10)
    draw_shield_bar(screen, 5, 40, player.shield)
    pygame.display.flip()

pygame.quit()
