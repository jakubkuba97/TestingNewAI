

"""
    Main controller
"""

import EnvironmentScript


class DeepIntelligence:
    def __init__(self, debug: bool = True) -> None:
        self.debug = debug
        self.special_episode = True
        # env variables
        self.env_episodes = 1000
        self.env_show_every = 50
        self.env_move_penalty = 2
        self.env_max_reward_value = 100
        self.env_bonus_value = 10
        self.env_epsilon = 0.5
        self.env_epsilon_decay = 0.9999
        self.env_learning_rate = 0.1
        self.env_discount = 0.95
        # board variables
        self.board_number_of_bonuses = 3
        self.board_disappearing_obstacles = True
        self.board_number_of_obstacles = 3
        self.board_size_of_board = 10

    def train_singularly(self) -> None:
        for episode in range(self.env_episodes):
            if self.debug:
                print('\tEpisode %i starting...\n' % episode)
            if self.special_episode:
                draw_this_one = True
            else:
                draw_this_one = False
            game_1 = EnvironmentScript.Env(draw=draw_this_one, dimensions=self.board_size_of_board, obstacles=self.board_number_of_obstacles, disappearing_obstacles=self.board_disappearing_obstacles,
                                           bonuses=self.board_number_of_bonuses, bonus_value=self.env_bonus_value, reward_value=self.env_max_reward_value)
            game_1.start_game()
            game_1.board.total_score += game_1.board.number_of_moves * -self.env_move_penalty
            self.env_epsilon *= self.env_epsilon_decay
            if episode % self.env_show_every == 0:
                self.special_episode = True
            else:
                self.special_episode = False


if __name__ == '__main__':
    ai = DeepIntelligence()
    ai.train_singularly()
