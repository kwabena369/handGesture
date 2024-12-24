import cv2 as cv

class Score:
    def __init__(self, initial_score=0):
        self.score = initial_score

    def increase(self, amount=1):
        self.score += amount

    def decrease(self, amount=1):
        if self.score > 0:
            self.score -= amount

    def reset(self):
        self.score = 0

    def display(self, frame, position=(10, 90), font=cv.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 255, 255), thickness=2):
        cv.putText(frame, f'Score: {self.score}', position, font, font_scale, color, thickness, cv.LINE_AA)