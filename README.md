# Real-Time Pose Estimation & Activity Recognition

## Overview
This project utilizes **MediaPipe's Pose Detection** module to recognize and track human movements in real-time, specifically detecting and counting **squats** and **push-ups**. By analyzing body joint angles, the system can differentiate between exercises and count repetitions automatically.

## Features
- **Real-time pose detection** using **MediaPipe**
- **Automatic detection of squats and push-ups**
- **Repetition counting** based on movement states
- **Accurate angle-based analysis** to differentiate activities
- **Works on both video files and webcam feed**

## Technologies Used
- **Python**
- **MediaPipe** (for pose estimation)
- **OpenCV** (for video processing)
- **NumPy** (for mathematical computations)

## How It Works
1. **Pose Detection:**
   - The system extracts key body landmarks from video frames using MediaPipe.
2. **Angle Calculation:**
   - Specific angles (knee, elbow, and torso) are computed based on key joint positions.
3. **Activity Differentiation:**
   - **Squats:** Identified based on knee bending and upright torso position.
   - **Push-ups:** Identified based on elbow bending and straight body posture.
4. **Repetition Counting:**
   - Movement transitions (e.g., standing → squatting → standing) trigger repetition counts.

## Angles Used for Detection

| **Activity** | **Key Angles Used**            | **Thresholds**        |
|--------------|--------------------------------|-----------------------|
| **Squat**    | **left_elbow_angle**           | < 80                  |
|              | **right_elbow_angle**          | < 80                  |
|              | **knee_angle**                 | < 140                 |
|              | **Torso_Angle**                | < 170                 |
| **Push-Up**  | **right_shoulder_angle**       | >=  160               |
|              | **left_shoulder_angle**        | >=  160               |
|              | **knee_angle**                 | between 150 to 180    |
|              | **Torso_Angle**                | > 170                 |


knee_angle = calculate_angle from (hip, knee, ankle)
torso_angle = calculate_angle from (right_shoulder, hip, knee)
right_elbow_angle = calculate_angle from (right_shoulder, right_elbow, wrist)
left_elbow_angle = calculate_angle from (left_shoulder, left_elbow, wrist)
right_shoulder_angle = calculate_angle from (left_shoulder,right_shoulder,right_elbow)
left_shoulder_angle = calculate_angle from (right_shoulder,left_shoulder,left_elbow)

## Future Improvements
- Support for additional activities (e.g., jumping jacks, lunges)
- Enhancing accuracy using machine learning models
- Adding a GUI for easier interaction



