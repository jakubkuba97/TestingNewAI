
"""
    Environment and AI logic
"""

import BoardScript
# import pickle
# from keras.models import Sequential
# from keras.layers import Dense, Activation, Flatten
# from keras.optimizers import Adam
#
# from rl.agents.dqn import DQNAgent
# from rl.policy import EpsGreedyQPolicy
# from rl.memory import SequentialMemory


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
        self.player_visibility = [self.offset_to_trophy, self.offset_to_obstacles, self.offset_to_bonuses, self.offset_to_corners]
        # player actions
        self.possible_actions = ['up', 'down', 'left', 'right']
        # model
    #     try:
    #         with open(self.file_name, 'rb') as file:
    #             self.dqn = pickle.load(file)
    #     except FileNotFoundError:
    #         model = Sequential()
    #         model.add(Flatten(input_shape=(1, dimensions*dimensions)))
    #         model.add(Dense(dimensions * len(self.possible_actions)))
    #         model.add(Dense(dimensions))
    #         model.add(Activation('relu'))
    #         model.add(Dense(len(self.possible_actions)))
    #         model.add(Activation('linear'))
    #         # print(self.model.summary())
    #
    #         policy = EpsGreedyQPolicy()
    #         memory = SequentialMemory(limit=50000, window_length=1)
    #         self.dqn = DQNAgent(model=model, nb_actions=len(self.possible_actions), memory=memory, nb_steps_warmup=10, target_model_update=1e-2, policy=policy)
    #         self.dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    #
    #         # self.save_model()
    #
    # def save_model(self) -> None:
    #     with open(self.file_name, 'wb') as file:
    #         pickle.dump(self.dqn, file, protocol=pickle.HIGHEST_PROTOCOL)

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
        self.player_visibility = [self.offset_to_trophy, self.offset_to_obstacles, self.offset_to_bonuses, self.offset_to_corners]

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
