import cv2
import mediapipe as mp
from math import hypot
import numpy as np

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    max_num_hands=2,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)

Draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    raise RuntimeError("Camera could not be opened. Check macOS camera permissions.")

finger_tip_ids = [4, 8, 12, 16, 20]

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Failed to read frame from camera.")
        break

    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    Process = hands.process(frameRGB)

    brightness_values = []

    if Process.multi_hand_landmarks:
        for handlm in Process.multi_hand_landmarks:
            height, width, color_channels = frame.shape

            landmarkList = []

            for _id, landmarks in enumerate(handlm.landmark):
                x = int(landmarks.x * width)
                y = int(landmarks.y * height)
                landmarkList.append([_id, x, y])

            Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)

            if len(landmarkList) >= 21:
                thumb_x, thumb_y = landmarkList[4][1], landmarkList[4][2]

                distances = []

                for tip_id in finger_tip_ids:
                    x, y = landmarkList[tip_id][1], landmarkList[tip_id][2]

                    cv2.circle(frame, (x, y), 7, (0, 255, 0), cv2.FILLED)

                    if tip_id != 4:
                        cv2.line(frame, (thumb_x, thumb_y), (x, y), (0, 255, 0), 2)
                        distance = hypot(x - thumb_x, y - thumb_y)
                        distances.append(distance)

                if distances:
                    average_distance = sum(distances) / len(distances)

                    brightness_percent = int(np.interp(average_distance, [15, 220], [0, 100]))
                    brightness_percent = max(0, min(100, brightness_percent))

                    brightness_values.append(brightness_percent)

    if brightness_values:
        final_brightness = int(sum(brightness_values) / len(brightness_values))
    else:
        final_brightness = 0

    cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)

    bar_height = int(np.interp(final_brightness, [0, 100], [400, 150]))
    cv2.rectangle(frame, (50, bar_height), (85, 400), (0, 255, 0), cv2.FILLED)

    cv2.putText(
        frame,
        f"{final_brightness}%",
        (35, 440),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()