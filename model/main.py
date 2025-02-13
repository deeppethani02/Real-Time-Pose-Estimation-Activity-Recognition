import cv2
import mediapipe as mp
import numpy as np

def detect_Activity(video_source=0):
    """
    Detect Activity(squats and pushups) in real-time or from a video file.
    Differentiates squats from push-ups by analyzing lower body motion.
    
    Args:
        video_source (int or str): Video source (0 for webcam, or file path for video).
    """
    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    # Function to calculate angle between three points
    def calculate_angle(a, b, c):
        a = np.array(a)  # First point
        b = np.array(b)  # Mid point
        c = np.array(c)  # End point

        #Calculating angles using
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    # Open video or webcam
    cap = cv2.VideoCapture(video_source)
    Squatting_count = 0
    push_up_count = 0
    prev_state = "Standing"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB for MediaPipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Process the frame
        results = pose.process(image)

        # Convert back to BGR for OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

             # Extract required landmarks
            landmarks = results.pose_landmarks.landmark
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # Calculate key angles
            knee_angle = calculate_angle(hip, knee, ankle)
            torso_angle = calculate_angle(right_shoulder, hip, knee)
            right_elbow_angle = calculate_angle(right_shoulder, right_elbow, wrist)
            left_elbow_angle = calculate_angle(left_shoulder, left_elbow, wrist)
            right_shoulder_angle = calculate_angle(left_shoulder,right_shoulder,right_elbow)
            left_shoulder_angle = calculate_angle(right_shoulder,left_shoulder,left_elbow,)


            # Detect squat state 
            if left_elbow_angle < 80 and right_elbow_angle < 80:  # Squatting
              if  knee_angle < 140  or torso_angle < 170 : 
                state = "Squatting"
            elif right_shoulder_angle >=  160 and right_shoulder_angle >= 160 : # push-up
              if 180 > knee_angle > 150 or torso_angle > 170:  
                state = "push-up"
            else :  # Standing
                state = "Standing"

            # Count repetitions
            if prev_state == "Squatting" and state == "Standing":
                Squatting_count += 1
            elif prev_state == "push-up" and state == "Standing":
                push_up_count += 1
            elif state == "Standing":
                pass
            prev_state = state

            # Display information
            cv2.putText(image, f"State: {state}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Squatting_count: {Squatting_count}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"push_up_count: {push_up_count}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


        # Display the frame
        cv2.imshow('Activity Detection', image)

        # Break on 'q' key
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




# video_source = 0 for webcam || video_source = 'video link' for any video
detect_Activity(video_source='squat.mp4') 