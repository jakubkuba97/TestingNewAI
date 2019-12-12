
"""
    Create a playable maze and teach a reinforcement AI to play it using worth assignment
"""


class Board:
    def __init__(self, dimensions: int = 10, obstacles: int = 2) -> None:
        self.dimensions = dimensions
        self.obstacles = obstacles
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
        print(trophy_coordinates, player_coordinates, obstacle_coordinates)

    def actualise_worth(self) -> None:
        pass
