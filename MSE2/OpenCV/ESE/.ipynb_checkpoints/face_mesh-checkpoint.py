# import cv2
# import mediapipe as mp 

# mp_face_mesh = mp.solutions.face_mesh  # having predefined face model
# # drawing utils -> used for drawing landmarks
# mp_drawing = mp.solutions.drawing_utils

# face_mesh = mp_face_mesh.FaceMesh(
#     static_image_mode=False,
#     max_num_faces=1,  # detect one face at a time
#     refine_landmarks=True,
#     min_detection_confidence=0.5,  # min conf to detect the faces
#     min_tracking_confidence=0.5
# )

# cap = cv2.VideoCapture(0)

# while True:
#     flag, frame = cap.read()
#     if not flag:
#         break

#     # mediapipe expects rgb
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # process frame through mediapipe model
#     results = face_mesh.process(rgb_frame)

#     # Drawing landmarks
#     if results.multi_face_landmarks:
#         # Loop through detected faces (only 1 here)
#         for face_landmarks in results.multi_face_landmarks:
#             drawing_spec = mp_drawing.DrawingSpec(
#                 color=(255, 0, 0),  # BLUE
#                 thickness=1,
#                 circle_radius=1
#             )
#             # draw full face mesh
#             mp_drawing.draw_landmarks(
#                 image=frame,  # image to draw
#                 landmark_list=face_landmarks,  # detected landmarks
#                 connections=mp_face_mesh.FACEMESH_TESSELATION,
#                 landmark_drawing_spec=drawing_spec,
#                 connection_drawing_spec=drawing_spec

#             )

#     cv2.imshow("MediaPipe", frame)

#     key = cv2.waitKey(1) & 0xFF
#     if key == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()





# # eye
# import cv2
# import mediapipe as mp 

# mp_face_mesh = mp.solutions.face_mesh  # having predefined face model
# # drawing utils -> used for drawing landmarks
# mp_drawing = mp.solutions.drawing_utils

# face_mesh = mp_face_mesh.FaceMesh(
#     static_image_mode=False,
#     max_num_faces=1,  # detect one face at a time
#     refine_landmarks=True,
#     min_detection_confidence=0.5,  # min conf to detect the faces
#     min_tracking_confidence=0.5
# )

# cap = cv2.VideoCapture(0)

# while True:
#     flag, frame = cap.read()
#     if not flag:
#         break

#     # mediapipe expects rgb
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # process frame through mediapipe model
#     results = face_mesh.process(rgb_frame)

#     # Drawing landmarks
#     if results.multi_face_landmarks:
#         # Loop through detected faces (only 1 here)
#         for face_landmarks in results.multi_face_landmarks:
#             h, w, _=frame.shape
#             # left eye-> 33
#             # right eye-> 263
#             point = face_landmarks.landmark[263]
#             # convert normalized coordinators-> Pixel coordinates
#             x=int(point.x*w)
#             y=int(point.y*h)

#             cv2.circle(frame, (x,y), 10, (0,255,0),1)

#     cv2.imshow("MediaPipe", frame)

#     key = cv2.waitKey(1) & 0xFF
#     if key == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()


import cv2
import mediapipe as mp
import numpy as np
import os

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=7,
    refine_landmarks=True
)

# Load assets safely
script_dir = os.path.dirname(os.path.abspath(__file__))

sunglasses = cv2.imread(os.path.join(script_dir, "sunglass1.png"), cv2.IMREAD_UNCHANGED)
hat = cv2.imread(os.path.join(script_dir, "hat.png"), cv2.IMREAD_UNCHANGED)

if sunglasses is None:
    raise FileNotFoundError("sunglass1.png not found")
if hat is None:
    raise FileNotFoundError("hat.png not found")

print("Sunglasses shape:", sunglasses.shape)

# Overlay function (handles RGB + RGBA)
def overlay_png(frame, overlay, x_offset, y_offset):
    fh, fw = frame.shape[:2]
    oh, ow = overlay.shape[:2]

    x1c = max(0, x_offset)
    y1c = max(0, y_offset)
    x2c = min(fw, x_offset + ow)
    y2c = min(fh, y_offset + oh)

    sx1 = x1c - x_offset
    sy1 = y1c - y_offset
    sx2 = sx1 + (x2c - x1c)
    sy2 = sy1 + (y2c - y1c)

    if x2c <= x1c or y2c <= y1c:
        return

    roi = frame[y1c:y2c, x1c:x2c]
    patch = overlay[sy1:sy2, sx1:sx2]

    # Handle RGB vs RGBA
    if patch.shape[2] == 4:
        ov_img = patch[:, :, :3]
        mask = patch[:, :, 3]
    else:
        ov_img = patch
        gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    mask_inv = cv2.bitwise_not(mask)

    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    fg = cv2.bitwise_and(ov_img, ov_img, mask=mask)

    frame[y1c:y2c, x1c:x2c] = cv2.add(bg, fg)


# Toggle states
show_glasses = True
show_hat = True

cap = cv2.VideoCapture(0)

while True:
    flag, frame = cap.read()
    if not flag:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape

            # ── SUNGLASSES ─────────────────────────
            if show_glasses:
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]

                x1, y1 = int(left_eye.x * w), int(left_eye.y * h)
                x2, y2 = int(right_eye.x * w), int(right_eye.y * h)

                glasses_width = int(np.hypot(x2 - x1, y2 - y1) * 1.8)-20
                glasses_height = int(glasses_width * 0.5)-20

                if glasses_width > 0 and glasses_height > 0:
                    resized_sg = cv2.resize(sunglasses, (glasses_width, glasses_height))

                    x_center = (x1 + x2) // 2
                    y_center = (y1 + y2) // 2

                    overlay_png(
                        frame,
                        resized_sg,
                        int(x_center - glasses_width / 2),
                        int(y_center - glasses_height / 2)
                    )

            # ── HAT ────────────────────────────────
            if show_hat:
                lm_left = face_landmarks.landmark[234]
                lm_right = face_landmarks.landmark[454]
                lm_forehead = face_landmarks.landmark[10]

                fl_x = int(lm_left.x * w)
                fl_y = int(lm_left.y * h)
                fr_x = int(lm_right.x * w)
                fr_y = int(lm_right.y * h)
                fh_y = int(lm_forehead.y * h)

                face_width = int(np.hypot(fr_x - fl_x, fr_y - fl_y))
                hat_width = int(face_width * 1.5)

                hat_h, hat_w = hat.shape[:2]
                hat_height = int(hat_width * hat_h / hat_w)

                if hat_width > 0 and hat_height > 0:
                    resized_hat = cv2.resize(hat, (hat_width, hat_height))

                    hx_center = (fl_x + fr_x) // 2
                    hat_x = int(hx_center - hat_width / 2)
                    hat_y = int(fh_y - hat_height + hat_height * 0.3)

                    overlay_png(frame, resized_hat, hat_x, hat_y)

    cv2.imshow("Face Mesh AR", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break
    elif key == ord('g'):
        show_glasses = not show_glasses
    elif key == ord('h'):
        show_hat = not show_hat
    elif key == ord('a'):
        show_glasses = not show_glasses
        show_hat = not show_hat

cap.release()
cv2.destroyAllWindows()