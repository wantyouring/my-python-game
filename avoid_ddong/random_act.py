# 똥피하기게임

import pygame
import random
import pylab
import numpy as np
import os
from time import sleep
from collections import deque

os.environ["SDL_VIDEODRIVER"] = "dummy" # rendering없이 pygame실행하기.

##### 학습 variable
EPISODES = 5000
state_size = 22  # 똥 x좌표 10개 + 똥 y좌표 10개 + man x좌표 + man y좌표
action_size = 3  # 정지,좌,우
global_step = 0
episodes, scores, avg_q_max_record, scores30 = [], [], [], []
score_deque = deque(maxlen=30)
##### 게임 variable
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

# state구성. 똥좌표, 사람 좌표 붙여 구성.
def reshape_to_state(ddong_x, ddong_y, man_x, man_y):
    global state_size
    state = ddong_x + ddong_y
    state.append(man_x)
    state.append(man_y)
    return np.reshape(state, [1, state_size])

def playgame(gamepad,man,ddong,clock):
    global global_step, episodes, scores, avg_q_max_record
    end_game = False
    man_x = PAD_WIDTH * 0.5
    man_y = PAD_HEIGHT * 0.9
    ddong_x, ddong_y = [], []
    ddong_speed = 10
    ddong_total_cnt = 10
    score = 0
    # 학습 variable
    epi_step = 0

    # 초기 똥 추가
    for i in range(ddong_total_cnt):
        ddong_x.append(int(random.randrange(0,PAD_WIDTH - man_width) / 48) * 48) # 특정 위치에서만 똥 떨어지게 환경 단순화.
        ddong_y.append(random.randrange(-PAD_HEIGHT,0))

    # 초기 state
    state = reshape_to_state(ddong_x, ddong_y, man_x, man_y)
    action = 0
    dx = 0
    # 게임 진행.
    while not end_game:
        reward = 0
        epi_step += 1
        global_step += 1
        if epi_step % 4 == 0: #4단위 frameskip. 4step씩 같은 행동 취하기.
            action = random.randrange(0,3)

        # action에 따른 위치변화.
        if action == 1:
            dx -= 5
        elif action == 2:
            dx += 5
        # else action == 0:
        #   dx = dx

        # ---여기부터 해당 action에 대해 step
        # 사람 이동
        man_x += dx
        if man_x < 0:
            man_x = 0
        elif man_x > PAD_WIDTH - man_width:
            man_x = PAD_WIDTH - man_width

        # 똥 이동
        for index, value in enumerate(ddong_y):
            ddong_y[index] += ddong_speed
            # 똥 끝까지 떨어졌을 시 새로운 똥 ㄱㄱ
            if value > PAD_HEIGHT:
                ddong_x[index] = int(random.randrange(0,PAD_WIDTH - man_width) / 48) * 48
                ddong_y[index] = -ddong_height
                score += 1

        # 똥 맞았는지 체크
        for index, value in enumerate(ddong_y):
            if abs(ddong_x[index] - man_x) < ddong_width and man_y - ddong_y[index] <  ddong_height:
                end_game = True

        # 배경, 사람, 똥 그리기, 점수표시
        '''
        gamepad.fill(BLACK) # 배경
        gamepad.blit(man, (man_x, man_y)) # 사람
        for index, value in enumerate(ddong_y): # 똥
            gamepad.blit(ddong,(ddong_x[index],ddong_y[index]))
        # 점수표시
        font = pygame.font.SysFont(None, 30)
        text = font.render('Score: {}'.format(score), True, (255, 255, 255))
        gamepad.blit(text, (380, 30))
        pygame.display.update()
        '''

        # ---여기까지 해당 action에 대해 step끝남

        if epi_step % 4 == 0 or end_game: # 4단위로 frame skip, 끝나는 상황은 체크
            next_state = reshape_to_state(ddong_x, ddong_y, man_x, man_y)
            state = next_state

        if end_game:
            return epi_step, score

        # FPS
        clock.tick(100000000000000)
        #clock.tick(100000)


if __name__ == "__main__":
    #global state_size, action_size
    pygame.init()
    gamepad = pygame.display.set_mode((PAD_WIDTH, PAD_HEIGHT))
    pygame.display.set_caption('똥피하기')
    man = pygame.image.load('man.png')
    ddong = pygame.image.load('ddong.png')
    clock = pygame.time.Clock()

    for e in range(EPISODES):
        epi_step, score = playgame(gamepad,man,ddong,clock)
        scores.append(score)
        avg = 0
        if e < 30:
            score_deque.append(score)
            scores30.append(0)
        else:
            score_deque.append(score)
            for v in score_deque:
                avg += v
            avg /= float(30)
            scores30.append(avg)

        episodes.append(e)
        print("epi : {}. score : {}. epi_step : {}.".format(e,score,epi_step))
        if e % 50 == 0:
            pylab.figure(1)
            pylab.plot(episodes, scores, 'b')
            pylab.plot(episodes, scores30, 'r')
            pylab.savefig("./random_play.png")
