import pygame
import sys
pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_VIRUS_RATE = 25
laser_img = pygame.image.load('laser_bricks.png')
laser_img_rect = laser_img.get_rect()
laser_img_rect.left = 0
spikes_img = pygame.image.load('spikes_bricks.png')
spikes_img_rect = spikes_img.get_rect()
spikes_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Corvi')


class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()


class Corvi:
    corvi_velocity = 10

    def __init__(self):
        self.corvi_img = pygame.image.load('corvi.png')
        self.corvi_img_rect = self.corvi_img.get_rect()
        self.corvi_img_rect.width -= 10
        self.corvi_img_rect.height -= 10
        self.corvi_img_rect.top = WINDOW_HEIGHT/2
        self.corvi_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.corvi_img, self.corvi_img_rect)
        if self.corvi_img_rect.top <= laser_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.corvi_img_rect.bottom >= spikes_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.corvi_img_rect.top -= self.corvi_velocity
        elif self.down:
            self.corvi_img_rect.top += self.corvi_velocity


class Virus:
    virusx_velocity = 20

    def __init__(self):
        self.virusx = pygame.image.load('virus.png')
        self.virusx_img = pygame.transform.scale(self.virusx, (20, 20))
        self.virusx_img_rect = self.virusx_img.get_rect()
        self.virusx_img_rect.right = corvi.corvi_img_rect.left
        self.virusx_img_rect.top = corvi.corvi_img_rect.top + 30


    def update(self):
        canvas.blit(self.virusx_img, self.virusx_img_rect)

        if self.virusx_img_rect.left > 0:
            self.virusx_img_rect.left -= self.virusx_velocity


class SuperDoc:
    velocity = 10

    def __init__(self):
        self.superdoc_img = pygame.image.load('superdoc.png')
        self.superdoc_img_rect = self.superdoc_img.get_rect()
        self.superdoc_img_rect.left = 20
        self.superdoc_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.superdoc_img, self.superdoc_img_rect)
        if self.superdoc_img_rect.top <= laser_img_rect.bottom:
            game_over()
            if SCORE > self.superdoc_score:
                self.superdoc_score = SCORE
        if self.superdoc_img_rect.bottom >= spikes_img_rect.top:
            game_over()
            if SCORE > self.superdoc_score:
                self.superdoc_score = SCORE
        if self.up:
            self.superdoc_img_rect.top -= 10
        if self.down:
            self.superdoc_img_rect.bottom += 10


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('superdoc_dies.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('end.png')
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
    canvas.fill(BLACK)
    pygame.mixer.music.load('superhero_theme.wav')
    pygame.mixer.music.play(-1, 0.0)
    start_img = pygame.image.load('start.png')
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
        laser_img_rect.bottom = 3
        spikes_img_rect.top = WINDOW_HEIGHT - 3
        LEVEL = 1
    elif SCORE in range(10, 20):
        laser_img_rect.bottom = 50
        spikes_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 2
    elif SCORE in range(20, 30):
        laser_img_rect.bottom = 80
        spikes_img_rect.top = WINDOW_HEIGHT - 80
        LEVEL = 3
    elif SCORE in range(30, 40):
        laser_img_rect.bottom = 120
        spikes_img_rect.top = WINDOW_HEIGHT - 120
        LEVEL = 4
    elif SCORE > 50:
        laser_img_rect.bottom = 180
        spikes_img_rect.top = WINDOW_HEIGHT - 180
        LEVEL = 5
        


def game_loop():
    while True:
        global corvi
        corvi = Corvi()
        virusx = Virus()
        superdoc = SuperDoc()
        add_new_virusz_counter = 0
        global SCORE
        SCORE = 0
        global  HIGH_SCORE
        virusx_list = []
        pygame.mixer.music.load('superhero_theme.wav')
        pygame.mixer.music.play(-1, 0.0)
        while True:
            canvas.fill(BLACK)
            check_level(SCORE)
            corvi.update()
            add_new_virusz_counter += 1

            if add_new_virusz_counter == ADD_NEW_VIRUS_RATE:
                add_new_virusz_counter = 0
                new_virusz = Virus()
                virusx_list.append(new_virusz)
            for f in virusx_list:
                if f.virusx_img_rect.left <= 0:
                    virusx_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        superdoc.up = True
                        superdoc.down = False
                    elif event.key == pygame.K_DOWN:
                        superdoc.down = True
                        superdoc.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        superdoc.up = False
                        superdoc.down = True
                    elif event.key == pygame.K_DOWN:
                        superdoc.down = True
                        superdoc.up = False

            score_font = font.render('Score:'+str(SCORE), True, GREEN)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (200, laser_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Level:'+str(LEVEL), True, GREEN)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (500, laser_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render('Top Score:'+str(topscore.high_score),True,GREEN)
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (800, laser_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font, top_score_font_rect)

            canvas.blit(laser_img, laser_img_rect)
            canvas.blit(spikes_img, spikes_img_rect)
            superdoc.update()
            for f in virusx_list:
                if f.virusx_img_rect.colliderect(superdoc.superdoc_img_rect):
                    game_over()
                    if SCORE > superdoc.superdoc_score:
                        superdoc.superdoc_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()


