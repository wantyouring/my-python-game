# 똥피하기게임

import pygame
import random
import pylab
import numpy as np
import os
from time import sleep
from collections import deque
from doubleDQN import DoubleDQNAgent

os.environ["SDL_VIDEODRIVER"] = "dummy" # rendering없이 pygame실행하기.

##### 학습 variable
EPISODES = 50000
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

def playgame(gamepad,man,ddong,clock,agent):
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
    agent.avg_q_max = 0

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
        action = agent.get_action(state)

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
                reward = 1 # 똥 안맞으면 reward
                score += 1

        # 똥 맞았는지 체크
        for index, value in enumerate(ddong_y):
            if abs(ddong_x[index] - man_x) < ddong_width and man_y - ddong_y[index] <  ddong_height:
                end_game = True
                reward = -100 # 똥 맞으면 패널티

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

        agent.avg_q_max += np.amax(agent.model.predict(state)[0])
        next_state = reshape_to_state(ddong_x, ddong_y, man_x, man_y)
        agent.append_sample(state, action, reward, next_state, end_game)
        agent.train_model()
        state = next_state

        if global_step % agent.update_target_rate == 0:
            agent.update_target_model()

        if end_game:
            avg_q_max_record.append(agent.avg_q_max / float(epi_step))
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

    agent = DoubleDQNAgent(state_size, action_size)
    #agent.load_model() #@@@@@@@@@모델 로드

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

        episodes.append(e)
        print("epi : {}. score : {}. epi_step : {}. memory len : {}. epsilon : {}.".format(e,score,epi_step,len(agent.memory),agent.epsilon))
        if e % 50 == 0:
            pylab.figure(1)
            pylab.plot(episodes, scores, 'b')
            pylab.plot(episodes, scores30, 'r')
            pylab.savefig("./ddqn2.png")

            pylab.figure(2)
            pylab.plot(episodes, avg_q_max_record)
            pylab.savefig("./avg_q_max2.png")
            agent.model.save_weights("./ddqn.h5")
