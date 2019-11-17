## 파일 정리  
- RL1_avoid_game.py : doubleDQN 1개 모델 사용. state 똥 위치 x,y값, 사람 위치 x,y값 좌표 리스트로 전달. 똥 위치 일정하게.  
- RL2_avoid_game.py : cnn_doubleDQN 한 모델 사용. state 픽셀 width*height크기 그림정보로 전달. 똥 위치 일정하게.
- RL2_avoid_game_multi_agent.py : 30 step별로 모델 나눠 학습. cnn_doubleDQN 모델 사용. 똥 위치 일정하게.
- random_act.py : 랜덤 액션으로 게임 진행.
- random_avoid_game.py : cnn_doubleDQN 모델 사용. state 픽셀 그림정보로 전달. 똥 위치 random하게 떨어지는 환경.
- ~~(random_avoid_game2.py : cnn_doubleDQN2 모델 사용. state 픽셀 그림정보로 전달. 똥 위치 random하게 떨어지는 환경. (random_avoid_game.py와 거의 똑같. 파라미터만 바뀐거))~~

- doubleDQN.py : doubleDQN 모델
- cnn_doubleDQN.py : cnn double DQN 모델
- ~~(cnn_doubleDQN2.py : 파라미터만 조금 바꿈)~~
