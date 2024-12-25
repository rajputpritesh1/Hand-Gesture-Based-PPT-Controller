import cv2
import mediapipe as mp
import pyautogui
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Initialize Hand Detection
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
def count_fingers(hand_landmarks):
    """
    Count raised fingers using landmark positions.
    """
    tips_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    fingers = []
    
    # Thumb
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
        fingers.append(1)  # Thumb is open
    else:
        fingers.append(0)
    
    # Other fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y:
            fingers.append(1)  # Finger is open
        else:
            fingers.append(0)
    
    return fingers.count(1)

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame to make it mirror-like
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process with Mediapipe
    result = hands.process(rgb_frame)
    
    # Draw Hand Landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Count Fingers
            num_fingers = count_fingers(hand_landmarks)
            print(f"Fingers Detected: {num_fingers}")
            
            # Simulate keypress for PowerPoint control
            if num_fingers == 1:  # One finger: Next slide
                pyautogui.press("right")
            elif num_fingers == 2:  # Two fingers: Previous slide
                pyautogui.press("left")

    # Display the Frame
    cv2.imshow("Hand Gesture PPT Controller", frame)
    
    # Break on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
