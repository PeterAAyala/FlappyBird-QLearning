import sys 
import pygame
import numpy.random as npr
import math 
import numpy as np

from FBRedone import *

class Learner(object):

    def __init__(self):
        self.last_state = None
        self.last_action = None
        self.last_reward = None 
        self.previous_state = None

        self.alpha = 0.2
        self.gamma = 0.2

        self.action_space = [0,1]
        self.position_space = [-1, 0, 1]
        self.vel_space = [-1, 1]

        self.q = {}
        for k in self.action_space:
            for i in self.position_space:
                for j in self.vel_space:
                    self.q[((i, j), k)] = 0


    def reset(self):
        self.last_state = None
        self.last_action = None
        self.last_reward = None

    def action_callback(self, state):
        
        b_top = state["bird"]["top"]
        b_bot = state['bird']['bottom']
        b_mid = (b_top + b_bot) / 2
        pipe_top = state["pipe"]["top"]
        pipe_bot = state["pipe"]["bottom"]
        pipe_mid = (pipe_top + pipe_bot) / 2
        pipe_bott = (pipe_mid + pipe_bot) / 2
        pipe_topt = (pipe_top + pipe_mid) / 2
        b_velo = state['bird']['displacement']
        pipe_dist = state['pipe']['distance']


        current_state = (0,0)
        if b_bot <= pipe_bott:
            current_state = (-1, current_state[1])
        elif b_top >= pipe_topt:
            current_state = (1, current_state[1])
        else:
            current_state = (0, current_state[1])


        if b_velo <= 0:
            current_state = (current_state[0], -1)
        else:
            current_state = (current_state[0], 1)


        if self.last_reward:
            future = self.alpha * (self.last_reward + self.gamma * np.max([self.q[(current_state, k)] for k in self.action_space]))
            self.q[(self.previous_state, self.last_action)] = (1-self.alpha) * self.q[(self.previous_state, self.last_action)] + future

        self.last_action = self.action_space[np.argmax([self.q[(current_state, k)] for k in self.action_space])]

        self.last_state  = state
        self.previous_state = current_state

        return self.last_action

    def reward_callback(self, reward):
        self.last_reward = reward 


def run_games(learner, iters = 2, tick_speed= 480):

    for i in range(iters):
        jumpy = FlappyBird(
            action_callback = learner.action_callback,
            reward_callback = learner.reward_callback,
            tick_speed= tick_speed)

        while jumpy.game_loop():
            pass

        learner.reset()
    pygame.quit()
    return

if __name__ == '__main__':
    agent = Learner()
    run_games(agent, iters = 5)
