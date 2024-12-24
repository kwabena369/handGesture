class LifeSystem:
    def __init__(self, initial_lives=5):
        self.lives = initial_lives

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0

    def reset(self):
        self.lives = 5