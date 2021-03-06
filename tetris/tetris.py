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
        self.num = random.randrange(1,8) # 7종류 블록
        self.pos_i = 0 # 맨 위
        self.pos_j = 5 # 가운데에서 생성
        #self.left_most
        #self.right_most # 가장 오른쪽 블록 index체크. 벽 못 넘어가게 방지하기 위해서.
        self.speed = 1 # 블록 떨어지는 속도. 현재 작을수록 빠르게 떨어짐.
        self.stop = False
        # self.list : 각 블록의 turn별로 list정보 저장. [turn][i][j] 3차원 리스트.
        self.list = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] for _ in range(4)] # 3차원 list 초기화
        if self.num == 1: # O block
            self.list = [[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]] for _ in range(4)]
            self.left_most = [1,1,1,1]
            self.right_most = [2,2,2,2]
        elif self.num == 2: # I block
            self.list[0] = [[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]]
            self.list[1] = [[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]]
            self.list[2] = [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]
            self.list[3] = [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]
            self.left_most = [2,0,2,0]
            self.right_most = [2,3,2,3]
        elif self.num == 3: # S block
            self.list[0] = [[0,0,0,0],[0,0,1,1],[0,1,1,0],[0,0,0,0]]
            self.list[1] = [[0,0,1,0],[0,0,1,1],[0,0,0,1],[0,0,0,0]]
            self.list[2] = [[0, 0, 0, 0], [0, 0, 1, 1], [0, 1, 1, 0], [0, 0, 0, 0]]
            self.list[3] = [[0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0]]
            self.left_most = [1,2,1,2]
            self.right_most = [3,3,3,3]
        elif self.num == 4: # Z block
            self.list[0] = [[0,0,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,0]]
            self.list[1] = [[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,0,0,0]]
            self.list[2] = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 0]]
            self.list[3] = [[0, 0, 0, 1], [0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 0, 0]]
            self.left_most = [1,2,1,2]
            self.right_most = [3,3,3,3]
        elif self.num == 5: # L block
            self.list[0] = [[0,0,0,0],[0,1,1,1],[0,1,0,0],[0,0,0,0]]
            self.list[1] = [[0,0,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,0]]
            self.list[2] = [[0,0,0,1],[0,1,1,1],[0,0,0,0],[0,0,0,0]]
            self.list[3] = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]
            self.left_most = [1,2,1,1]
            self.right_most = [3,3,3,2]
        elif self.num == 6: # J block
            self.list[0] = [[0,0,0,0],[0,1,1,1],[0,0,0,1],[0,0,0,0]]
            self.list[1] = [[0,0,1,1], [0,0,1,0], [0,0,1,0], [0,0,0,0]]
            self.list[2] = [[0,1,0,0], [0,1,1,1], [0,0,0,0], [0,0,0,0]]
            self.list[3] = [[0,0,1,0], [0,0,1,0], [0,1,1,0], [0,0,0,0]]
            self.left_most = [1,2,1,1]
            self.right_most = [3,3,3,2]
        elif self.num == 7: # T block
            self.list[0] =[[0,0,0,0],[0,1,1,1],[0,0,1,0],[0,0,0,0]]
            self.list[1] = [[0,0,1,0], [0,0,1,1], [0,0,1,0], [0,0,0,0]]
            self.list[2] = [[0,0,1,0], [0,1,1,1], [0,0,0,0], [0,0,0,0]]
            self.list[3] = [[0,0,1,0], [0,1,1,0], [0,0,1,0], [0,0,0,0]]
            self.left_most = [1,2,1,1]
            self.right_most = [3,3,3,2]

    def turn_block(self,clockwise):
        if clockwise:
            self.turn = (self.turn + 1) % 4
        else:
            self.turn = (self.turn + 3) % 4

    def move_block(self, dir): #왼:-1 오:1 아래:0 (코딩용)위:2
        if dir == -1:
            self.pos_j -= 1
        elif dir == 1:
            self.pos_j += 1
        elif dir == 0:
            self.pos_i += 1
        elif dir == 2:
            self.pos_i -= 1

# GUI
class Gui:
    def __init__(self,pygame):
        self.BLOCK_SIZE = 30
        self.PAD_WIDTH = BLOCK_SIZE * 12
        self.PAD_HEIGHT = BLOCK_SIZE * 22
        self.block_img = pygame.image.load('block.png')
        self.block2_img = pygame.image.load('block2.png')
        self.empty_img = pygame.image.load('empty.png')
        pygame.display.set_caption('tetris')
        self.gamepad = pygame.display.set_mode((self.PAD_WIDTH,self.PAD_HEIGHT))

    def update_pad(self,pad,score):
        for i in range(22):
            for j in range(12):
                if pad[i][j] == 9:
                    self.gamepad.blit(self.block2_img,(j*BLOCK_SIZE,i*BLOCK_SIZE))
                elif pad[i][j] == 0:
                    self.gamepad.blit(self.empty_img,(j*BLOCK_SIZE,i*BLOCK_SIZE))
                else:
                    self.gamepad.blit(self.block_img,(j*BLOCK_SIZE,i*BLOCK_SIZE))
        text = pygame.font.SysFont(None, 30).render('Score : {}'.format(score), True, (255, 255, 255))
        self.gamepad.blit(text,(240,30))
        pygame.display.update()


# 한줄 라인클리어
def clear_line(pad):
    clear = False
    for i in range(1,21):
        if 0 in pad[i]: # 빈 칸 있으면 패스
            continue
        pad[i][1] = 8 # 비울 줄 체크
        clear = True
        break
    for i in range(20,0,-1):
        if pad[i][1] == 8:
            for j in range(i,0,-1):
                for k in range(1,11):
                    pad[j][k] = pad[j-1][k]
            break
    return pad, clear

# 패드에 현재 블록 위치 쓰기.(실제 pad에는 안씀)
def block_to_pad(pad,block):
    gamepad = copy.deepcopy(pad)
    for i in range(4):
        for j in range(4):
            if block.list[block.turn][i][j] != 0:
                gamepad[block.pos_i + i][block.pos_j + j] = block.list[block.turn][i][j]
    return gamepad

def block_crash(gamepad,block):
    # 블록끼리 crash 판단
    for i in range(4):
        for j in range(4):
            if block.list[block.turn][i][j] != 0 and gamepad[block.pos_i + i][block.pos_j + j] != 0:
                return 1

    # 벽에 박힘 crash 판단
    if block.pos_j + block.left_most[block.turn] < 1 or block.pos_j + block.right_most[block.turn] > 10:
        return 2

    return 0


# 메인 게임 함수
def playgame():
    pygame.init()
    gui = Gui(pygame) # GUI 객체
    clock = pygame.time.Clock()
    end_game = False
    new_block = True
    hard_drop = False
    step = 0
    score = 0

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

        # 키보드 입력 받고 블록 이동가능한지 체크.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 종료
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #if block.pos_j + block.left_most[block.turn] > 1: # 블록 벽 넘는지 체크하고 move
                    block.move_block(-1)
                    if block_crash(gamepad,block) != 0:
                        block.move_block(1)
                elif event.key == pygame.K_RIGHT:
                    #if block.pos_j + block.right_most[block.turn] < 10:
                    block.move_block(1)
                    if block_crash(gamepad, block) != 0:
                        block.move_block(-1)
                elif event.key == pygame.K_DOWN:
                    block.move_block(0)
                    if block_crash(gamepad, block) != 0:
                        block.move_block(2)
                elif event.key == pygame.K_UP:
                    block.turn_block(True)
                    if block_crash(gamepad,block) == 1: # 블록crash로 못돌리는 상황이면 돌리기 취소
                        block.turn_block(False)
                    if block_crash(gamepad,block) == 2: # 벽에 붙어 못 돌리는 상황이면 돌린 block 벽에 붙여놓는 것으로 바꾸기.
                        if block.pos_j + block.left_most[block.turn] < 1:
                            block.pos_j = 1 - block.left_most[block.turn]
                        elif block.pos_j + block.right_most[block.turn] > 10:
                            block.pos_j = 10 - block.right_most[block.turn]
                elif event.key == pygame.K_SPACE:
                    hard_drop = True


        # 블록 한 칸 내리기
        if step % block.speed == 0 or hard_drop == True:
            while True:
                block.move_block(0)
                # 더 내릴 수 없으면 블록 고정 후 gamepad에 쓰기
                for i in range(4):
                    for j in range(4):
                        if block.list[block.turn][i][j] != 0 and gamepad[block.pos_i+i][block.pos_j+j] != 0:
                            block.stop = True
                if block.stop == True:
                    block.move_block(2)
                    new_block = True
                    # 게임 종료
                    if block.pos_i < 1:
                        end_game = True
                        break
                    # gamepad에 블록 쓰기
                    for i in range(4):
                        for j in range(4):
                            if block.list[block.turn][i][j] != 0:
                                gamepad[block.pos_i+i][block.pos_j+j] = block.num

                    # 없앨 줄 있으면 클리어하기.(최대 4줄이므로 4번)
                    for _ in range(4):
                        gamepad, clear = clear_line(gamepad)
                        if clear:
                            score += 1
                    hard_drop = False
                if hard_drop == False:
                    break

        # 현재 블록 gamepad에 쓰기(tmp_pad : 임시 보이기용 pad)
        tmp_pad = block_to_pad(gamepad,block)
        gui.update_pad(tmp_pad,score)

        # FPS
        clock.tick(5)


if __name__ == "__main__":
    playgame()