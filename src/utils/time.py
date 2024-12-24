import time

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def is_time_up(self):
        if self.start_time is None:
            return False
        elapsed_time = time.time() - self.start_time
        return elapsed_time >= self.duration

    def reset(self):
        self.start_time = None

    def get_remaining_time(self):
        if self.start_time is None:
            return self.duration
        elapsed_time = time.time() - self.start_time
        return max(0, self.duration - elapsed_time)

    def has_expired(self):
        return self.get_remaining_time() <= 0