# tetris

import pygame
import random
from time import sleep
import copy
import sys

'''
매번 사용자 입력 체크해 벽돌 좌우 옮기기
몇번 루프마다 블록 아래로 한 칸 내리기
블록 더이상 못내려가면 블록 고정.
'''

# 블록 class
class Block:
    def __init__(self):
        self.turn = random.randrange(0,4) # 4방향
        self.num = 1#random.randrange(1,8) # 7종류 블록
        self.pos_i = 0 # 맨 위
        self.pos_j = 5 # 가운데에서 생성
        self.speed = 1 # 블록 떨어지는 속도. 현재 작을수록 빠르게 떨어짐.
        self.stop = False
        # self.list : 각 블록의 turn별로 list정보 저장. [turn][i][j] 3차원 리스트.
        self.list = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] for _ in range(4)] # 3차원 list 초기화
        if self.num == 1: # ㅁ블럭
            self.list = [[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]] for _ in range(4)]
        elif self.num == 2: # ㅡ블럭
            self.list[0] = [[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]]
            self.list[1] = [[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]]
            self.list[2] = [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]
            self.list[3] = [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]
        # @@@@@@@@@@@@@@@@@@@@나머지 블록 추가하기.

    def turn_block(self):
        self.turn = (self.turn + 1) % 4

    #@@@@@@@@@@@끝이면 더 못가게.
    def move_block(self, dir): #왼:-1 오:1 아래:0 (코딩용)위:2
        if dir == -1:
            self.pos_j -= 1
        elif dir == 1:
            self.pos_j += 1
        elif dir == 0:
            self.pos_i += 1
        elif dir == 2:
            self.pos_i -= 1

# 라인클리어
def clear_line(pad):
    for i in range(1,21):
        if 0 in pad[i]: # 빈 칸 있으면 패스
            continue
        pad[i][1] = 8 # 비울 줄 체크
    for i in range(20,0,-1):
        if pad[i][1] == 8:
            for j in range(i,0,-1):
                for k in range(1,11):
                    pad[j][k] = pad[j-1][k]
    return pad

# 패드에 현재 블록 위치 쓰기.(실제 pad에는 안씀)
def block_to_pad(pad,block):
    gamepad = copy.deepcopy(pad)
    for i in range(4):
        for j in range(4):
            if block.list[block.turn][i][j] != 0:
                gamepad[block.pos_i + i][block.pos_j + j] = block.list[block.turn][i][j]
    return gamepad

# 메인 게임 함수
def playgame(clock):
    end_game = False
    new_block = True
    step = 0

    # gamepad 초기화
    gamepad = [[0] * 12 for _ in range(22)]
    for i in range(12):
        gamepad[21][i] = 9
    for i in range(22):
        gamepad[i][0] = 9
        gamepad[i][11] = 9


    #계속 키입력 받으며 게임 진행.
    while not end_game:
        step += 1
        # 새 블록 필요하면 블록 생성
        if new_block == True:
            block = Block()
            new_block = False

        # 키보드 입력 받기
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 종료
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    block.move_block(-1)
                elif event.key == pygame.K_RIGHT:
                    block.move_block(1)
                elif event.key == pygame.K_DOWN:
                    block.move_block(0)
                elif event.key == pygame.K_UP:
                    block.turn_block()

        # 블록 한 칸 내리기
        if step % block.speed == 0:
            block.move_block(0)
            # 더 내릴 수 없으면 블록 고정 후 gamepad에 쓰기
            for i in range(4):
                for j in range(4):
                    if block.list[block.turn][i][j] != 0 and gamepad[block.pos_i+i][block.pos_j+j] != 0:
                        block.stop = True
            if block.stop == True:
                block.move_block(2)
                new_block = True
                for i in range(4):
                    for j in range(4):
                        if block.list[block.turn][i][j] != 0:
                            gamepad[block.pos_i+i][block.pos_j+j] = block.num

                # 없앨 줄 있으면 클리어하기.
                gamepad = clear_line(gamepad)

        # 현재 블록 gamepad에 쓰기(임시 보이기용 pad)
        tmp_pad = block_to_pad(gamepad,block)
        #print('step:{}'.format(step),end='\r')
        print('block.stop:{}'.format(block.stop))
        for i in range(22):
            print('\r{}'.format(tmp_pad[i]))
        sys.stdout.flush()
        #print('test')
        # FPS
        clock.tick(1)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('tetris')
    clock = pygame.time.Clock()
    playgame(clock)