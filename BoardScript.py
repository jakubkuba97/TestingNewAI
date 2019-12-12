
"""
    Create, draw a playable maze and move around it
"""


class Board:
    def __init__(self, dimensions: int = 10, obstacles: int = 2, disappearing_obstacles: bool = False, bonuses: int = 2, bonus_value: int = 10, reward_value: int = 100) -> None:
        self.dimensions = dimensions
        self.obstacles = obstacles
        self.disappearing_obstacles = disappearing_obstacles
        self.bonuses = bonuses
        self.reward_value = reward_value
        self.bonus_value = bonus_value
        self.player_coordinates = []
        self.number_of_moves = 0
        self.total_score = 0
        self.board = []     # column, row, trophy, player, obstacle, bonus, worth

    def initialize_board(self) -> None:
        self.create_board()
        self.add_objects()
        self.actualise_worth()

    def create_board(self) -> None:
        for y in range(self.dimensions):
            row = []
            for x in range(self.dimensions):
                row.append([x, y, 0, 0, 0, 0, 0])
            self.board.append(row)

    def add_objects(self) -> None:
        from random import randint as rd
        trophy_coordinates = [rd(0, self.dimensions - 1), rd(0, self.dimensions - 1)]
        player_coordinates = [rd(0, self.dimensions - 1), rd(0, self.dimensions - 1)]
        while player_coordinates == trophy_coordinates:
            player_coordinates = [rd(0, self.dimensions - 1), rd(0, self.dimensions - 1)]
        obstacle_coordinates = []
        for _ in range(self.obstacles):
            coordinates = [rd(0, self.dimensions - 1), rd(0, self.dimensions - 1)]
            while coordinates == trophy_coordinates or coordinates == player_coordinates or coordinates in obstacle_coordinates:
                coordinates = [rd(0, self.dimensions - 1), rd(0, self.dimensions - 1)]
            obstacle_coordinates.append(coordinates)
        bonuses_coordinates = []
        for _ in range(self.bonuses):
            coordinates = [rd(0, self.dimensions - 1), rd(0, self.dimensions - 1)]
            while coordinates == trophy_coordinates or coordinates == player_coordinates or coordinates in obstacle_coordinates or coordinates in bonuses_coordinates:
                coordinates = [rd(0, self.dimensions - 1), rd(0, self.dimensions - 1)]
            bonuses_coordinates.append(coordinates)
        self.player_coordinates = player_coordinates
        self.board[trophy_coordinates[1]][trophy_coordinates[0]][2] = 1
        self.board[player_coordinates[1]][player_coordinates[0]][3] = 1
        for coordinate in obstacle_coordinates:
            self.board[coordinate[1]][coordinate[0]][4] = 1
        for coordinate in bonuses_coordinates:
            self.board[coordinate[1]][coordinate[0]][5] = 1

    def actualise_worth(self) -> None:
        for row_index, row in enumerate(self.board):
            for column_index, value in enumerate(row):
                if value[2] == 1:
                    self.board[row_index][column_index][6] = self.reward_value
                elif value [4] == 1:
                    self.board[row_index][column_index][6] = -self.reward_value
                elif value [5] == 1:
                    self.board[row_index][column_index][6] = self.bonus_value

    def draw_board(self) -> None:
        spaces = '\t'
        for row in self.board:
            print(spaces, end='')
            for value in row:
                if value[3] == 1:
                    print('P', end='')
                elif value[2] == 1:
                    print('T', end='')
                elif value[4] == 1:
                    print('O', end='')
                elif value[5] == 1:
                    print('x', end='')
                else:
                    print('.', end='')
                print(spaces, end='')
            print()

    def move(self, direction: str) -> None:
        if direction == 'up' and self.player_coordinates[1] != 0:
            self.board[self.player_coordinates[1]][self.player_coordinates[0]][3] = 0
            self.board[self.player_coordinates[1] - 1][self.player_coordinates[0]][3] = 1
            self.player_coordinates = [self.player_coordinates[0], self.player_coordinates[1] - 1]
        elif direction == 'down' and self.player_coordinates[1] != self.dimensions - 1:
            self.board[self.player_coordinates[1]][self.player_coordinates[0]][3] = 0
            self.board[self.player_coordinates[1] + 1][self.player_coordinates[0]][3] = 1
            self.player_coordinates = [self.player_coordinates[0], self.player_coordinates[1] + 1]
        elif direction == 'left' and self.player_coordinates[0] != 0:
            self.board[self.player_coordinates[1]][self.player_coordinates[0]][3] = 0
            self.board[self.player_coordinates[1]][self.player_coordinates[0] - 1][3] = 1
            self.player_coordinates = [self.player_coordinates[0] - 1, self.player_coordinates[1]]
        elif direction == 'right' and self.player_coordinates[0] != self.dimensions - 1:
            self.board[self.player_coordinates[1]][self.player_coordinates[0]][3] = 0
            self.board[self.player_coordinates[1]][self.player_coordinates[0] + 1][3] = 1
            self.player_coordinates = [self.player_coordinates[0] + 1, self.player_coordinates[1]]
        self.total_score += self.board[self.player_coordinates[1]][self.player_coordinates[0]][6]
        if self.board[self.player_coordinates[1]][self.player_coordinates[0]][5] == 1:
            self.board[self.player_coordinates[1]][self.player_coordinates[0]][5] = 0
        if self.disappearing_obstacles and self.board[self.player_coordinates[1]][self.player_coordinates[0]][4] == 1:
            self.board[self.player_coordinates[1]][self.player_coordinates[0]][4] = 0
        self.number_of_moves += 1
        self.actualise_worth()
