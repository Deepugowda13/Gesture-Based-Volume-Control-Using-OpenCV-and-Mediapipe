import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize system volume interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol = volume_interface.GetVolumeRange()[:2]

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
            index_x, index_y = int(index_tip.x * width), int(index_tip.y * height)

            # Visual reference
            cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 0), -1)
            cv2.circle(frame, (index_x, index_y), 10, (255, 0, 0), -1)

            # Distance between fingers
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

            # Volume mapping
            min_distance, max_distance = 20, 200
            distance = max(min_distance, min(distance, max_distance))
            vol_percent = (distance - min_distance) / (max_distance - min_distance)
            volume_db = min_vol + (max_vol - min_vol) * vol_percent
            volume_interface.SetMasterVolumeLevel(volume_db, None)

            # Display blue volume bar with reduced width
            bar_x1, bar_x2 = 60, 75  # Reduced width
            bar_y1, bar_y2 = 150, 400
            cv2.rectangle(frame, (bar_x1, bar_y1), (bar_x2, bar_y2), (255, 0, 0), 2)
            filled = int((1 - vol_percent) * 250)
            cv2.rectangle(frame, (bar_x1, bar_y1 + filled), (bar_x2, bar_y2), (255, 0, 0), -1)

            # Display volume percentage
            volume_text = f'{int(vol_percent * 100)} %'
            cv2.putText(frame, volume_text, (40, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Popup if volume is 100%
            if int(vol_percent * 100) == 100:
                cv2.putText(frame, "High Volume!", (150, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("Gesture Volume Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
