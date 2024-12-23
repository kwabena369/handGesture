
import random
import cv2 as cv
import numpy as np
import mediapipe as mp

# Create the mediapipe hands object
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize random circle position
x_position = random.randint(0, 640)
y_position = random.randint(0, 480)

# Circle properties
size_of_circle = 30

# Function to draw the circle
def draw_circle(frame, color):
    cv.circle(frame, (x_position, y_position), size_of_circle, color, -1)

# Function to check if the finger tip is inside the circle
def is_finger_in_circle(finger_x, finger_y, circle_x, circle_y, circle_radius):
    distance = np.sqrt((finger_x - circle_x) ** 2 + (finger_y - circle_y) ** 2)
    return distance < circle_radius

# Get the webcam feed
video = cv.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("No frame captured")
            break

        frame = cv.cvtColor(cv.flip(frame, 1), cv.COLOR_BGR2RGB)
        results = hands.process(frame)
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            color_value = (0, 255, 0)  # Green color for hand detected
            for hand_landmarks in results.multi_hand_landmarks:
                second_finger_tip = hand_landmarks.landmark[8]
                #  but  you would ask why we did the int conversion and the second_finger_tip.x * frame.shape[1]?
                #  The reason is that the landmark coordinates are normalized values between 0 and 1.
                #  i don't still get it what is meant by normalized values between 0 and 1
                #  well it means that the x and y values of the landmarks are between 0 and 1.
                #  To get the actual pixel values, we need to multiply the x and y values with the width and height of the frame respectively.
                # SO LIKE LET ME GIVE YOU  A real world example
                #  let's say we have a frame of 640x480 pixels. If the x value of a landmark is 0.5, it means that the landmark is at 320 pixels (0.5 * 640) from the left of the frame.
                second_finger_tip_x = int(second_finger_tip.x * frame.shape[1])
                second_finger_tip_y = int(second_finger_tip.y * frame.shape[0])

                # Draw a small circle at the tip of the second finger
                cv.circle(frame, (second_finger_tip_x, second_finger_tip_y), 15, (255, 10, 0), -1)

                # Check if the tip of the second finger is in the circle
                if is_finger_in_circle(second_finger_tip_x, second_finger_tip_y, x_position, y_position, size_of_circle):
                    x_position = random.randint(0, 640)
                    y_position = random.randint(0, 480)

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else:
            color_value = (0, 0, 255)  # Red color for no hand detected

        draw_circle(frame, color_value)
        cv.imshow("Hand Tracking", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

video.release()
cv.destroyAllWindows()
