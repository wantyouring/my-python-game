# 똥피하기게임

import pygame
import random
from time import sleep

BLACK = (0, 0, 0)
RED = (255, 0, 0)
#게임화면 크기
PAD_WIDTH = 480
PAD_HEIGHT = 640
#똥크기
ddong_width = 26
ddong_height = 26
#사람크기
man_width = 36
man_height = 38

def playgame(gamepad,man,ddong,clock):
    end_game = False
    man_x = PAD_WIDTH * 0.5
    man_y = PAD_HEIGHT * 0.9
    ddong_x, ddong_y = [], []
    ddong_speed = 10
    ddong_total_cnt = 10
    score = 0

    #초기 똥 추가
    for i in range(ddong_total_cnt):
        ddong_x.append(random.randrange(0,PAD_WIDTH - man_width))
        ddong_y.append(random.randrange(-PAD_HEIGHT,0))

    dx = 0
    #계속 키입력 받으며 게임 진행.
    while not end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 종료
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx -= 5
                elif event.key == pygame.K_RIGHT:
                    dx += 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    dx = 0

        gamepad.fill(BLACK)

        # 사람 이동
        man_x += dx
        if man_x < 0:
            man_x = 0
        elif man_x > PAD_WIDTH - man_width:
            man_x = PAD_WIDTH - man_width

        # 사람 그리기
        gamepad.blit(man, (man_x, man_y))

        # 똥 이동
        for index, value in enumerate(ddong_y):
            ddong_y[index] += ddong_speed
            # 똥 끝까지 떨어졌을 시 새로운 똥 ㄱㄱ
            if value > PAD_HEIGHT:
                ddong_x[index] = random.randrange(0,PAD_WIDTH - man_width)
                ddong_y[index] = -ddong_height
                score += 1

        # 똥 맞았는지 체크
        for index, value in enumerate(ddong_y):
            if abs(ddong_x[index] - man_x) < ddong_width and man_y - ddong_y[index] <  ddong_height:
                end_game = True

        # 똥 그리기
        for index, value in enumerate(ddong_y):
            gamepad.blit(ddong,(ddong_x[index],ddong_y[index]))

        # 점수표시
        font = pygame.font.SysFont(None, 30)
        text = font.render('Score: {}'.format(score),True,(255,255,255))
        gamepad.blit(text,(380,30))
        pygame.display.update()

        print()

        # FPS
        clock.tick(100)


if __name__ == "__main__":
    pygame.init()
    gamepad = pygame.display.set_mode((PAD_WIDTH, PAD_HEIGHT))
    pygame.display.set_caption('똥피하기')
    man = pygame.image.load('man.png')
    ddong = pygame.image.load('ddong.png')
    clock = pygame.time.Clock()
    while True:
        playgame(gamepad,man,ddong,clock)