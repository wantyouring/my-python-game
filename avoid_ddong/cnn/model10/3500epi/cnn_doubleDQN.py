# DoubleDQN Agent.
# https://github.com/rlcode/reinforcement-learning/blob/master/2-cartpole/2-double-dqn/cartpole_ddqn.py
import numpy as np
import random
from collections import deque
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from keras.models import Sequential

class DoubleDQNAgent:
    def __init__(self, state_size, action_size):
        self.render = False

        self.state_size = state_size
        self.action_size = 3 # 시작 action 1은 제외.

        # DDQN 하이퍼 파라미터
        self.discount_factor = 0.99
        self.learning_rate = 0.0001
        self.epsilon = 1.0
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
        self.batch_size = 32
        self.train_start = 1000
        self.update_target_rate = 500
        self.memory = deque(maxlen=10000)
        self.avg_q_max = 0 # 학습 잘 되는지 확인.

        # 학습모델, 타겟모델 두 개 생성.
        self.model = self.build_model()
        self.target_model = self.build_model()

        # 타겟모델 초기화.
        self.update_target_model()

    # 모델 load
    def load_model(self):
        self.model.load_weights("./ddqn.h5")

    # 모델 생성.
    # cnn사용
    def build_model(self):
        model = Sequential()
        #model.add(Conv2D(8, (8, 8), strides=(8, 8), activation='relu', input_shape=self.state_size))
        model.add(Conv2D(8, (4, 4), strides=(2, 2), activation='relu', input_shape=self.state_size))
        #model.add(MaxPooling2D(pool_size=(2,2)))
        #model.add(Conv2D(16,(4,4),strides=(2,2),activation='relu'))
        model.add(Conv2D(16,(2,2),strides=(1,1),activation='relu'))
        model.add(Flatten())
        model.add(Dense(256,activation='relu'))
        model.add(Dense(self.action_size))
        model.summary()
        model.compile(loss='mse',optimizer=Adam(lr=self.learning_rate))
        return model

    # 타겟모델에 학습모델 복사.
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    # 입실론 그리디 정책으로 action 구하기.
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            q_value = self.model.predict(state)
            return np.argmax(q_value[0])

    # replay memory에 s,a,r,s' 저장
    def append_sample(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    # 모델 학습하기.
    def train_model(self):
        # memory에서 minibatch 크기만큼 s,a,r,s',(d)가져와 학습.
        if len(self.memory) < self.train_start:
            return
        batch_size = min(self.batch_size, len(self.memory))
        mini_batch = random.sample(self.memory, batch_size)

        update_input = np.zeros((batch_size, self.state_size[0], self.state_size[1], self.state_size[2]))
        update_target = np.zeros((batch_size, self.state_size[0], self.state_size[1], self.state_size[2]))
        action, reward, done = [], [], []

        for i in range(batch_size):
            update_input[i] = mini_batch[i][0]
            action.append(mini_batch[i][1])
            reward.append(mini_batch[i][2])
            update_target[i] = mini_batch[i][3]
            done.append(mini_batch[i][4])

        target = self.model.predict(update_input)   # s에 대한 학습모델 예측값
        target_next = self.model.predict(update_target) # s`에 대한 학습모델 예측값
        target_val = self.target_model.predict(update_target)   # s`에 대한 타겟모델 예측값

        for i in range(self.batch_size):
            # like Q Learning, get maximum Q value at s'
            # But from target model
            if done[i]:
                target[i][action[i]] = reward[i]
            else:
                # 모델에서 action선택. update할 때는 타겟모델의 값을 가져오고 reward더해 update.
                a = np.argmax(target_next[i])
                # Q-Target = r + γQ(s’,argmax(Q(s’,a,ϴ),ϴ’))
                # ϴ : 학습모델(model), ϴ’: 타겟모델(target_model)
                target[i][action[i]] = reward[i] + self.discount_factor * (target_val[i][a])

        # state에 대한 새로 얻은 Q값들로 학습모델 fit.
        self.model.fit(update_input, target, batch_size=self.batch_size, epochs=1, verbose=0)