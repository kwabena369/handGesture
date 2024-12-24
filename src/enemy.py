import random
import cv2 as cv
import numpy as np
class Enemy:
    def __init__(self, screen_width, screen_height, size=30):
        self.screen_width = int ( screen_width - 50)
        self.screen_height = screen_height
        self.size = size
        self.x_position = random.randint(0, screen_width)
        self.y_position = random.randint(0, screen_height)

    def draw(self, frame, color):
        cv.circle(frame, (self.x_position, self.y_position), self.size, color, -1)

    def reset_position(self):
        self.x_position = random.randint(0, self.screen_width)
        self.y_position = random.randint(0, self.screen_height)

    def is_finger_in_circle(self, finger_x, finger_y):
        distance = np.sqrt((finger_x - self.x_position) ** 2 + (finger_y - self.y_position) ** 2)
        return distance < self.size