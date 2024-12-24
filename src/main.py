import cv2 as cv
import mediapipe as mp
import numpy as np
from utils.time import Timer
from enemy import Enemy
from life_system import LifeSystem

#  the initial dimension of the window
screen_width = 640
screen_height = 480

#   create  instance of the key component of the gamr
enemy = Enemy(screen_width, screen_height)
timer = Timer(10)  #  that 10 sec and the ball would change it possiiton 
life_system = LifeSystem()

# the mediapipe for the hand dectionand drawing the landmark
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Get the webcam feed
video = cv.VideoCapture(0)

# Start the timer
timer.start()

# Main loop
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        _, frame = video.read()
        if not _:
            print("No frame captured")
            break

        frame = cv.cvtColor(cv.flip(frame, 1), cv.COLOR_BGR2RGB)
        results = hands.process(frame)
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            color_value = (0, 255, 0)  # Green color for hand detected
            for hand_landmarks in results.multi_hand_landmarks:
                second_finger_tip = hand_landmarks.landmark[8]
                second_finger_tip_x = int(second_finger_tip.x * frame.shape[1])
                second_finger_tip_y = int(second_finger_tip.y * frame.shape[0])

                # Draw a small circle at the tip of the second finger
                cv.circle(frame, (second_finger_tip_x, second_finger_tip_y), 15, (255, 10, 0), -1)

                # Check if the tip of the second finger is in the circle
                if enemy.is_finger_in_circle(second_finger_tip_x, second_finger_tip_y):
                    enemy.reset_position()
                    timer.start()  # Restart the timer when the circle is touched

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else:
            color_value = (0, 0, 255)  # Red color for no hand detected

        # Check if the timer has expired
        if timer.has_expired():
            life_system.lose_life()
            if life_system.is_game_over():
                print("Game Over")
                break
            else:
                timer.start()  # Restart the timer for the next life

        enemy.draw(frame, color_value)
        cv.putText(frame, f'Time: {timer.get_remaining_time():.1f}s', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
        cv.putText(frame, f'Lives: {life_system.lives}', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
        cv.imshow("Hand Tracking", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

video.release()
cv.destroyAllWindows()