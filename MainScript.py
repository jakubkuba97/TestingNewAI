

"""
    Main script
"""

import BoardScript


if __name__ == '__main__':
    my_board = BoardScript.Board(dimensions=10, obstacles=2, max_learning_value=100)
    my_board.initialize_board()
    print(my_board.board)