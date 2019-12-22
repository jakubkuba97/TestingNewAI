
"""
    Environment and AI logic
"""

import BoardScript
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory


class Env:
    def __init__(self, draw: bool = False,
                 dimensions: int = 10, obstacles: int = 2, disappearing_obstacles: bool = False, bonuses: int = 2, bonus_value: int = 10, reward_value: int = 100, obstacle_ends: bool = False) -> None:
        self.board = BoardScript.Board(dimensions=dimensions, obstacles=obstacles, disappearing_obstacles=disappearing_obstacles, bonuses=bonuses,
                                       bonus_value=bonus_value, reward_value=reward_value, obstacle_ends=obstacle_ends)
        self.board.initialize_board()
        self.draw = draw
        self.no_obstacles = True if obstacles <= 0 else False
        self.no_bonuses = True if bonuses <= 0 else False
        self.file_name = 'deep_maze_ai.pkl'
        # player visibility
        self.offset_to_trophy = []
        self.offset_to_obstacles = [[]]
        self.offset_to_bonuses = [[]]
        self.offset_to_corners = [[]]
        # player actions
        self.possible_actions = ['up', 'down', 'left', 'right']
        # model
        try:
            with open(self.file_name, 'rb') as file:
                self.model = pickle.load(file)
        except FileNotFoundError:
            self.model = Sequential()
            self.model.add(Flatten(input_shape=(1, dimensions*dimensions)))
            self.model.add(Dense(dimensions * len(self.possible_actions)))
            self.model.add(Dense(dimensions))
            self.model.add(Activation('relu'))
            self.model.add(Dense(len(self.possible_actions)))
            self.model.add(Activation('linear'))
        # print(self.model.summary())

    def save_model(self) -> None:
        with open(self.file_name, 'wb') as file:
            pickle.dump(self.model, file, protocol=pickle.HIGHEST_PROTOCOL)

    def actualize_offsets(self) -> None:
        if not self.no_obstacles:
            self.offset_to_obstacles = [[]]
            for obstacle in self.board.obstacle_coordinates:
                self.offset_to_obstacles.append([self.board.player_coordinates[0] - obstacle[0], self.board.player_coordinates[1] - obstacle[1]])
        else:
            self.offset_to_obstacles = [[0, 0], [0, 0]]
        if not self.no_bonuses:
            self.offset_to_bonuses = [[]]
            for bonus in self.board.bonus_coordinates:
                self.offset_to_bonuses.append([self.board.player_coordinates[0] - bonus[0], self.board.player_coordinates[1] - bonus[1]])
        else:
            self.offset_to_bonuses = [[0, 0], [0, 0]]
        self.offset_to_trophy = [self.board.player_coordinates[0] - self.board.trophy_coordinates[0], self.board.player_coordinates[1] - self.board.trophy_coordinates[1]]
        self.offset_to_corners = [[self.board.player_coordinates[0] - self.board.borders_coordinates[0][0], self.board.player_coordinates[1] - self.board.borders_coordinates[0][1]],
                                  [self.board.player_coordinates[0] - self.board.borders_coordinates[1][0] + 1, self.board.player_coordinates[1] - self.board.borders_coordinates[1][1] + 1]]

    def start_game(self) -> None:
        from time import sleep
        wait_time = 0.5
        self.actualize_offsets()
        if self.draw:
            self.board.draw_board()
            print('Total moves: %i, total score: %i' % (self.board.number_of_moves, self.board.total_score))
            sleep(wait_time)
        while not self.board.finished:
            pass

    def start_manual_game(self) -> None:
        self.board.draw_board()
        print('Total moves: %i, total score: %i' % (self.board.number_of_moves, self.board.total_score))
        while not self.board.finished:
            left = 'a'
            right = 'd'
            down = 's'
            up = 'w'
            conversion = {left: 'left', right: 'right', down: 'down', up: 'up'}
            movement = input()
            try:
                self.board.move(conversion[movement])
            except KeyError:
                self.board.move(' ')
            self.board.draw_board()
            self.actualize_offsets()
            print()
            print('Total moves: %i, total score: %i' % (self.board.number_of_moves, self.board.total_score))
            print()
