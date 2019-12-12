

"""
    Main script
"""

import BoardScript


if __name__ == '__main__':
    my_board = BoardScript.Board(dimensions=10, obstacles=3, disappearing_obstacles=True, bonuses=3, bonus_value=10, reward_value=100)
    my_board.initialize_board()
    my_board.draw_board()
    while True:
        x = input()
        my_board.move(x)
        my_board.draw_board()
        print()
        print(my_board.number_of_moves, my_board.total_score)
        print()
