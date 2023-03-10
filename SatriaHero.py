import pygame
import sys
pygame.init()

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_FLAME_RATE = 25
bg = pygame.image.load('langit.png')
bricks_img = pygame.image.load('bricks.png')
bricks_img_rect = bricks_img.get_rect()
bricks_img_rect.left = 0
fire_img = pygame.image.load('fire_bricks.png')
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Satria Hero')


class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()


class Alien:
    alien_velocity = 10

    def __init__(self):
        self.alien_img = pygame.image.load('baspalbot.png')
        self.alien_img_rect = self.alien_img.get_rect()
        self.alien_img_rect.width -= 10
        self.alien_img_rect.height -= 10
        self.alien_img_rect.top = WINDOW_HEIGHT/2
        self.alien_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.alien_img, self.alien_img_rect)
        if self.alien_img_rect.top <= bricks_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.alien_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.alien_img_rect.top -= self.alien_velocity
        elif self.down:
            self.alien_img_rect.top += self.alien_velocity


class Flames:
    flames_velocity = 20

    def __init__(self):
        self.flames = pygame.image.load('fireball.png')
        self.flames_img = pygame.transform.scale(self.flames, (40, 40))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = alien.alien_img_rect.left
        self.flames_img_rect.top = alien.alien_img_rect.top + 30


    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)

        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= self.flames_velocity


class Satria_hero:
    velocity = 10

    def __init__(self):
        self.satria_hero_img = pygame.image.load('hero.png')
        self.satria_hero_img = pygame.transform.scale(self.satria_hero_img, (80, 80))
        self.satria_hero_img_rect = self.satria_hero_img.get_rect()
        self.satria_hero_img_rect.left = 20
        self.satria_hero_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.satria_hero_img, self.satria_hero_img_rect)
        if self.satria_hero_img_rect.top <= bricks_img_rect.bottom:
            game_over()
            if SCORE > self.satria_hero_score:
                self.satria_hero_score = SCORE
        if self.satria_hero_img_rect.bottom >= fire_img_rect.top:
            game_over()
            if SCORE > self.satria_hero_score:
                self.satria_hero_score = SCORE
        if self.up:
            self.satria_hero_img_rect.top -= 10
        if self.down:
            self.satria_hero_img_rect.bottom += 10


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('satria_hero_dies.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('GameOper.png')
    game_over_img = pygame.transform.scale(game_over_img, (500, 300))
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()


def start_game():
    canvas.fill(GREEN)
    start_img = pygame.image.load('StartSatriaHero.png')
    start_img = pygame.transform.scale(start_img, (1200, 600))
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()


def check_level(SCORE):
    global LEVEL
    if SCORE in range(0, 10):
        bricks_img_rect.bottom = 50
        fire_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10, 20):
        bricks_img_rect.bottom = 100
        fire_img_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(20, 30):
        bricks_img_rect.bottom = 150
        fire_img_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE > 30:
        bricks_img_rect.bottom = 200
        fire_img_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4





def game_loop():
    while True:
        global alien
        alien = Alien()
        flames = Flames()
        satria_hero = Satria_hero()
        add_new_flame_counter = 0
        global SCORE
        SCORE = 0
        global  HIGH_SCORE
        flames_list = []
        pygame.mixer.music.load('bgmusic.wav')
        pygame.mixer.music.play(-1, 0.0)
        while True:
            canvas.fill(BLACK)
            canvas.blit(bg,(0,0))
            check_level(SCORE)
            alien.update()
            add_new_flame_counter += 1

            if add_new_flame_counter == ADD_NEW_FLAME_RATE:
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)
            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        satria_hero.up = True
                        satria_hero.down = False
                    elif event.key == pygame.K_DOWN:
                        satria_hero.down = True
                        satria_hero.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        satria_hero.up = False
                        satria_hero.down = True
                    elif event.key == pygame.K_DOWN:
                        satria_hero.down = True
                        satria_hero.up = False

            score_font = font.render('Score:'+str(SCORE), True, BLACK)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (200, bricks_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Level:'+str(LEVEL), True, BLACK)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (500, bricks_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render('Top Score:'+str(topscore.high_score),True,BLACK)
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (800, bricks_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font, top_score_font_rect)

            canvas.blit(bricks_img, bricks_img_rect)
            canvas.blit(fire_img, fire_img_rect)
            satria_hero.update()
            for f in flames_list:
                if f.flames_img_rect.colliderect(satria_hero.satria_hero_img_rect):
                    game_over()
                    if SCORE > satria_hero.satria_hero_score:
                        satria_hero.satria_hero_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()


