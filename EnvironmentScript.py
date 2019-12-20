
"""
    Environment and AI logic
"""

import BoardScript
import pickle


class Env:
    def __init__(self, draw: bool = False,
                 dimensions: int = 10, obstacles: int = 2, disappearing_obstacles: bool = False, bonuses: int = 2, bonus_value: int = 10, reward_value: int = 100) -> None:
        self.board = BoardScript.Board(dimensions=dimensions, obstacles=obstacles, disappearing_obstacles=disappearing_obstacles, bonuses=bonuses, bonus_value=bonus_value, reward_value=reward_value)
        self.board.initialize_board()
        self.draw = draw
        self.no_obstacles = True if obstacles <= 0 else False
        self.no_bonuses = True if bonuses <= 0 else False
        # player visibility
        self.offset_to_trophy = []
        self.offset_to_obstacles = [[]]
        self.offset_to_bonuses = [[]]
        self.offset_to_corners = [[]]
        # player actions
        self.possible_actions = ['up', 'down', 'left', 'right']

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
        self.actualize_offsets()
        if self.draw:
            self.board.draw_board()
            print('Total moves: %i, total score: %i' % (self.board.number_of_moves, self.board.total_score))
        while not self.board.finished:
            x = input()
            self.board.move(x)
            self.board.draw_board()
            self.actualize_offsets()
            print()
            print('Total moves: %i, total score: %i' % (self.board.number_of_moves, self.board.total_score))
            print()
