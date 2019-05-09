# dodge

import pygame
import random
from time import sleep
import copy
import sys

# constants
MAN_SIZE = 20
ENEMY_SIZE = 10
PAD_WIDTH = 600
PAD_HEIGHT = 600


# GUI
class Gui:
    def __init__(self,pygame,width,height,man_size,enemy_size):
        self.PAD_WIDTH = width
        self.PAD_HEIGHT = height
        self.char_img = pygame.image.load('character.png')
        self.char_img = pygame.transform.scale(self.char_img,(man_size,man_size))
        self.enemy_img = pygame.image.load('enemy.png')
        self.enemy_img = pygame.transform.scale(self.enemy_img, (enemy_size, enemy_size))
        pygame.display.set_caption('dodge')
        self.gamepad = pygame.display.set_mode((self.PAD_WIDTH,self.PAD_HEIGHT))
        #pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))
        pygame.mouse.set_visible(False)
    def update_pad(self,man_x,man_y,enemies,score):
        self.gamepad.fill((255,255,255)) # init display
        text = pygame.font.SysFont(None, 30).render('Score : {}'.format(round(score,1)), True, (0, 0, 0))
        self.gamepad.blit(text,(240,30))
        self.gamepad.blit(self.char_img,(man_x,man_y))
        for enem in enemies:
            self.gamepad.blit(self.enemy_img, (enem.x, enem.y))
        pygame.display.update()

# enemy class
class enemy:
    def __init__(self,side):
        # 0:up, 1:down, 2:left, 3:right (from u,d,l,r)
        self.x = random.randrange(0,600)
        self.y = random.randrange(0,600)
        if side == 0:
            self.y = 0
            self.dir_x = random.uniform(-1,1) # -1 ~ 1
            self.dir_y = random.random() # 0 ~ 1
        elif side == 1:
            self.y = 600
            self.dir_x = random.uniform(-1, 1)  # -1 ~ 1
            self.dir_y = -1 * random.random()  # -1 ~ 0
        elif side == 2:
            self.x = 0
            self.dir_x = random.random()
            self.dir_y = random.uniform(-1, 1)
        elif side == 3:
            self.x = 600
            self.dir_x = -1 * random.random()
            self.dir_y = random.uniform(-1, 1)
        self.speed = 1 #random.randrange(1,3)

    # move 1 timestep
    def move(self):
        self.x = (self.x + self.dir_x * self.speed) % 600
        self.y = (self.y + self.dir_y * self.speed) % 600

# if crashed, return True.
def check_crash(enemies, man_x, man_y):
    for enem in enemies:
        # crash condition : man_x - ENEMY_SIZE < enem.x < man_x + MAN_SIZE. (y is same)
        if (enem.x > man_x - ENEMY_SIZE and
            enem.x < man_x + MAN_SIZE and
            enem.y > man_y - ENEMY_SIZE and
            enem.y < man_y + MAN_SIZE):
            return True
    return False


# main game function
def playgame():
    pygame.init()
    gui = Gui(pygame,PAD_WIDTH,PAD_HEIGHT,MAN_SIZE,ENEMY_SIZE) # GUI 객체
    clock = pygame.time.Clock()
    end_game = False
    step = 0

    # init enemies
    enemies = []
    for _ in range(100):
        enemies.append(enemy(random.randrange(0,4))) # 4 sides random enemies

    # playing game
    while not end_game:
        step += 1
        # take mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 종료
                pygame.quit()

            man_x,man_y = pygame.mouse.get_pos()
            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    a # key down
            '''
        # move enemies
        for enem in enemies:
            enem.move()

        # check crash
        if check_crash(enemies,man_x,man_y):
            end_game = True

        gui.update_pad(man_x,man_y,enemies,step/60)
        # FPS
        clock.tick(60)


if __name__ == "__main__":
    playgame()