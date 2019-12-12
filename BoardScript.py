
"""
    Create and draw a playable maze
"""


class Board:
    def __init__(self, dimensions: int = 10, obstacles: int = 2, max_learning_value: int = 100) -> None:
        self.dimensions = dimensions
        self.obstacles = obstacles
        self.max_learning_value = max_learning_value
        self.board = []     # column, row, trophy, player, obstacle, worth

    def initialize_board(self) -> None:
        self.create_board()
        self.add_objects()
        self.actualise_worth()

    def create_board(self) -> None:
        for y in range(self.dimensions):
            row = []
            for x in range(self.dimensions):
                row.append([x, y, 0, 0, 0, 0])
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
        self.board[trophy_coordinates[1]][trophy_coordinates[0]][2] = 1
        self.board[player_coordinates[1]][player_coordinates[0]][3] = 1
        for coordinate in obstacle_coordinates:
            self.board[coordinate[1]][coordinate[0]][4] = 1

    def actualise_worth(self) -> None:
        for row_index, row in enumerate(self.board):
            for column_index, value in enumerate(row):
                if value[2] == 1:
                    self.board[row_index][column_index][5] = self.max_learning_value
                elif value [4] == 1:
                    self.board[row_index][column_index][5] = -self.max_learning_value
