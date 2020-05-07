# Flappy Bird through Q-learning

## Introduction

This application was an attempt to implement a reinforcement learning algorithm on the game Flappy Bird. The game was recreated with Pygame in Python. Specifically, the agent is trained using Q-learning ([wikipedia link here](https://en.wikipedia.org/wiki/Q-learning)), with the following formula:

<img src="https://latex.codecogs.com/svg.latex?Q^{new}(s_t,&space;a_t)&space;\leftarrow&space;Q(s_t,&space;a_t)&space;&plus;&space;\alpha&space;\cdot&space;\Big(&space;r_t&space;&plus;&space;\gamma&space;\cdot&space;argmax\{&space;Q(s_{t&plus;1},&space;a_t)\}&space;-&space;Q(s_t,&space;a_t)&space;\Big)" title="Q^{new}(s_t, a_t) \leftaroow Q(s_t, a_t) + \alpha \cdot \Big( r_t + \gamma \cdot argmax\{ Q(s_{t+1}, a_t)\} - Q(s_t, a_t) \Big)" />

### Installation and Usage

1. Run `pip install -r requirements.txt`
2. Run `python QLearning.py`
3. If you want to play the game yourself, run `python Flappy_Bird_game.py` Press spacebar to jump.  





