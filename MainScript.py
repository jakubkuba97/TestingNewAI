

"""
    Main controller
"""

import EnvironmentScript


class DeepIntelligence:
    def __init__(self, episodes: int, show_every: int, debug: bool = True) -> None:
        self.debug = debug
        self.env_episodes = episodes
        self.special_episode = True
        self.show_every = show_every

    def train_singularly(self) -> None:
        for episode in range(self.env_episodes):
            if self.debug:
                print('\tEpisode %i starting...\n' % episode)
            if self.special_episode:
                game_1 = EnvironmentScript.Env(draw=True, dimensions=10, obstacles=3, disappearing_obstacles=True, bonuses=3, bonus_value=10, reward_value=100)
            else:
                game_1 = EnvironmentScript.Env(draw=False, dimensions=10, obstacles=3, disappearing_obstacles=True, bonuses=3, bonus_value=10, reward_value=100)
            game_1.start_game()
            if episode % self.show_every == 0:
                self.special_episode = True
            else:
                self.special_episode = False


if __name__ == '__main__':
    ai = DeepIntelligence(episodes=1000, show_every=50)
    ai.train_singularly()
