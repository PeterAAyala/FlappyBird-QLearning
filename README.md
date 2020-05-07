# Flappy Bird through Q-learning

## Introduction

This application was an attempt to implement a reinforcement learning algorithm on the game Flappy Bird. The game was recreated with Pygame in Python. Specifically, the agent is trained using Q-learning, with the following formula:

```
<img src="https://latex.codecogs.com/svg.latex?\Large&space;Q^{new}(s_t, a_t) \leftaroow Q(s_t, a_t) + \alpha \cdot \Big( r_t + \gamma \cdot argmax\{ Q(s+{t+1}, a)\} - Q(s_t, a_t) \Big)" title="Q^{new}(s_t, a_t) \leftaroow Q(s_t, a_t) + \alpha \cdot \Big( r_t + \gamma \cdot argmax\{ Q(s+{t+1}, a)\} - Q(s_t, a_t)" />
```

### Installation and Usage

1. Run `pip install -r requirements.txt`
2. Run `python QLearning.py`
3. If you want to play the game yourself, run `python Flappy_Bird_game.py` Press spacebar to jump.  





