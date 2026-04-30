import cv2
import mediapipe as mp 

mp_face_mesh = mp.solutions.face_mesh  # having predefined face model
# drawing utils -> used for drawing landmarks
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,  # detect one face at a time
    refine_landmarks=True,
    min_detection_confidence=0.5,  # min conf to detect the faces
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

while True:
    flag, frame = cap.read()
    if not flag:
        break

    # mediapipe expects rgb
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # process frame through mediapipe model
    results = face_mesh.process(rgb_frame)

    # Drawing landmarks
    if results.multi_face_landmarks:
        # Loop through detected faces (only 1 here)
        for face_landmarks in results.multi_face_landmarks:
            drawing_spec = mp_drawing.DrawingSpec(
                color=(255, 0, 0),  # BLUE
                thickness=1,
                circle_radius=1
            )
            # draw full face mesh
            mp_drawing.draw_landmarks(
                image=frame,  # image to draw
                landmark_list=face_landmarks,  # detected landmarks
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec

            )

    cv2.imshow("MediaPipe", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()