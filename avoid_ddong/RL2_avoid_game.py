# 똥피하기게임

import pygame
import random
import pylab
import numpy as np
import os
import sys
from time import sleep
from collections import deque
from cnn_doubleDQN import DoubleDQNAgent

##### 게임 variable
BLACK = (0, 0, 0)
RED = (255, 0, 0)
#게임화면 크기
PAD_WIDTH = 480
PAD_HEIGHT = 640
#똥크기
ddong_width = 40
ddong_height = 40
#사람크기
man_width = 40
man_height = 40

####미니게임화면(학습용)
#게임화면 크기
MINI_PAD_WIDTH = 12
MINI_PAD_HEIGHT = 16
#똥크기
MINI_ddong_width = 1
MINI_ddong_height = 1
#사람크기
MINI_man_width = 1
MINI_man_height = 1

##### 학습 variable
EPISODES = 5000000
LOAD_MODEL = False
RENDER = False # rendering하며 model play

TOTAL_DDONG = 8

state_size = (MINI_PAD_HEIGHT,MINI_PAD_WIDTH,1)  # 화면 정보 state list로 넘겨주기.
action_size = 3  # 정지,좌,우
global_step = 0
max_score = 0
episodes, scores, avg_q_max_record, scores30 = [], [], [], []
score_deque = deque(maxlen=30)


if RENDER == False:
    os.environ["SDL_VIDEODRIVER"] = "dummy" # rendering없이 pygame실행하기.

# state구성. 똥 255, 사람 180, 빈칸 0.
def reshape_to_state(ddong_x, ddong_y, man_x, man_y):
    mini_ddong_x, mini_ddong_y = [], []
    for i in range(TOTAL_DDONG):
        mini_ddong_x.append(int(ddong_x[i] / 40))
        mini_ddong_y.append(int(ddong_y[i] / 40))

    state = [[0]*MINI_PAD_WIDTH for _ in range(MINI_PAD_HEIGHT)]

    for i in range(TOTAL_DDONG):
        for j in range(MINI_ddong_height):
            for k in range(MINI_ddong_width):
                if mini_ddong_y[i] >= 0 and mini_ddong_y[i] + j < MINI_PAD_HEIGHT:
                    state[mini_ddong_y[i] + j][mini_ddong_x[i] + k] = 255

    for i in range(MINI_man_height):
        for j in range(MINI_man_width):
            state[int(man_y / 40) + i][int(man_x / 40) + j] = 180
    return np.reshape([state],(1,MINI_PAD_HEIGHT,MINI_PAD_WIDTH,1))

def playgame(gamepad,man,ddong,clock,agent):
    global global_step, episodes, scores, avg_q_max_record, max_score
    end_game = False
    man_x = 0
    man_y = int(PAD_HEIGHT * 15/16)
    ddong_x, ddong_y = [], []
    fixed_ddong_x = [8, 7, 4, 2, 5, 9, 0, 1, 3, 6, 3, 7, 3, 3, 4, 9, 0, 1, 5, 6, 8, 8, 9, 5, 6, 1, 2, 2, 4, 5]
    fixed_ddong_y = [8, 10, 8, 1, 0, 0, 17, 12, 1, 5, 7, 13, 9, 19, 0, 1, 3, 12, 13, 15, 8, 13, 15, 8, 10, 11, 13, 16, 6, 5]

    ddong_speed = 40
    man_speed = 40
    score = 0
    # 학습 variable
    epi_step = 0
    agent.avg_q_max = 0

    # 초기 똥 추가
    for i in range(TOTAL_DDONG):
        #ddong_x.append(int(random.randrange(0,PAD_WIDTH - man_width) / 48) * 48) # 특정 위치에서만 똥 떨어지게 환경 단순화.
        #ddong_y.append(random.randrange(-PAD_HEIGHT,0)) # 640 / 20 = 32

        ddong_x.append(int(fixed_ddong_x[i] * 40))
        ddong_y.append(int(fixed_ddong_y[i] * -40))

    # 초기 state
    state = reshape_to_state(ddong_x, ddong_y, man_x, man_y)
    action = 0
    dx = 0
    # 게임 진행.
    while not end_game:
        if RENDER == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # 종료
                    pygame.quit()

        reward = 1
        epi_step += 1
        global_step += 1
        action = agent.get_action(state)

        # action에 따른 위치변화.
        if action == 1:
            dx = -1 * man_speed
        elif action == 2:
            dx = man_speed
        elif action == 0:
            dx = 0

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
                #ddong_x[index] = int(random.randrange(0,PAD_WIDTH - man_width) / 48) * 48
                ddong_y[index] = -ddong_height
                score += 1

        # 똥 맞았는지 체크
        for index, value in enumerate(ddong_y):
            if abs(ddong_x[index] - man_x) < ddong_width and man_y - ddong_y[index] <  ddong_height:
                end_game = True
                reward = -1 # 똥 맞으면 패널티

        # 배경, 사람, 똥 그리기, 점수표시
        if RENDER == True:
            gamepad.fill(BLACK) # 배경
            gamepad.blit(man, (man_x, man_y)) # 사람
            for index, value in enumerate(ddong_y): # 똥
                gamepad.blit(ddong,(ddong_x[index],ddong_y[index]))
            # 점수표시
            font = pygame.font.SysFont(None, 30)
            text = font.render('Score: {}'.format(score), True, (255, 255, 255))
            gamepad.blit(text, (380, 30))
            pygame.display.update()



        # ---여기까지 해당 action에 대해 step끝남
        if max_score < score and RENDER == False:
            max_score = score
            agent.model.save_weights("./max_score_model.h5")

        agent.avg_q_max += np.amax(agent.model.predict(state)[0])
        #if epi_step % 4 == 0 or end_game: # 4단위로 frame skip, 끝나는 상황은 체크
        next_state = reshape_to_state(ddong_x, ddong_y, man_x, man_y)
        agent.append_sample(state, action, reward, next_state, end_game)
        if global_step % 5: # 5step마다 학습하기.
            agent.train_model()
        state = next_state

        if global_step % agent.update_target_rate == 0:
            agent.update_target_model()

        if end_game or score >= 200:
            avg_q_max_record.append(agent.avg_q_max / float(epi_step))
            return epi_step, score

        # FPS
        if RENDER == True:
            clock.tick(30)
        else:
            clock.tick(100000000000000)
        #clock.tick(100000000000000)
        #clock.tick(10)


if __name__ == "__main__":
    #global state_size, action_size
    pygame.init()
    gamepad = pygame.display.set_mode((PAD_WIDTH, PAD_HEIGHT),pygame.RESIZABLE)
    pygame.display.set_caption('똥피하기')
    man = pygame.image.load('man.png')
    ddong = pygame.image.load('ddong.png')
    # resize
    man = pygame.transform.scale(man,(man_width,man_height))
    ddong = pygame.transform.scale(ddong,(ddong_width,ddong_height))
    clock = pygame.time.Clock()

    agent = DoubleDQNAgent(state_size, action_size)
    if LOAD_MODEL == True:
        agent.load_model() #@@@@@@@@@모델 로드
        agent.epsilon = agent.epsilon_min
    if RENDER == True:
        agent.epsilon = -1

    for e in range(EPISODES):
        epi_step, score = playgame(gamepad,man,ddong,clock,agent)
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
            if avg >= 200:
                print("학습끝")
                sys.exit()


        episodes.append(e)
        print("epi : {}. score : {}. epi_step : {}. memory len : {}. epsilon : {}.".format(e,score,epi_step,len(agent.memory),agent.epsilon))
        if e % 50 == 0 and RENDER == False:
            pylab.figure(1)
            pylab.plot(episodes, scores, 'k')
            pylab.plot(episodes, scores30, 'y')
            pylab.savefig("./ddqn.png")

            pylab.figure(2)
            pylab.plot(episodes, avg_q_max_record)
            pylab.savefig("./avg_q_max.png")
            agent.model.save_weights("./ddqn.h5")
