import subprocess
from datetime import time, datetime
from threading import Thread
from time import sleep

import csv
import cv2 as cv
import numpy as np
import mediapipe as mp
import utils
from subprocess import PIPE, run


# th = Thread(target=server.run)
# th.start()
# adb logcat -t 1 -s GPS
# def get_gps():
#     command = ['adb', 'logcat', '-m', '1', '-T', '1', '-s', 'GPS']
#     result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
#     return result
#
#
# print(get_gps())
# sleep(1)
# print(get_gps())
# sleep(1)
# print(get_gps())
# exit()
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

mp_face_mesh = mp.solutions.face_mesh

cap_face = cv.VideoCapture('./video/face/video.mp4')
cap_front = cv.VideoCapture(0)

# cap_face.set(cv.CAP_PROP_FRAME_WIDTH, 960)
# cap_face.set(cv.CAP_PROP_FRAME_HEIGHT, 540)
cap_front.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cap_front.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

out_face = cv.VideoWriter(f'./video/face_{datetime.now()}.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30,
                          (int(cap_face.get(3)), int(cap_face.get(4))))
out_front = cv.VideoWriter(f'./video/front_{datetime.now()}.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30,
                           (int(cap_front.get(3)), int(cap_front.get(4))))
k = 1
face_width = int(cap_face.get(3))
face_height = int(cap_face.get(4))
front_width = int(cap_front.get(3))
front_height = int(cap_front.get(4))

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
) as face_mesh:
    with open(f'csv/{datetime.now()}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'eye_left_x', 'eye_left_y', 'eye_right_x', 'eye_right_y'])
        while True:

            ret_face, frame_face = cap_face.read()
            ret_front, frame_front = cap_front.read()
            if not ret_face:
                break

            if not ret_front:
                break

            out_front.write(frame_front)

            rgb_frame_face = cv.cvtColor(frame_face, cv.COLOR_BGR2RGB)
            img_h, img_w = frame_face.shape[:2]
            results = face_mesh.process(rgb_frame_face)

            if results.multi_face_landmarks:
                mesh_points = np.array(
                    [np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in
                     results.multi_face_landmarks[0].landmark])

                (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)

                center_front = np.array([sum([l_cx / k, r_cx / k]) / 2, sum([l_cy / k, r_cy / k]) / 2], dtype=np.int32)

                d = np.hstack((center_left, center_right))
                writer.writerow(np.hstack((np.array(datetime.now()), d)))

                cv.circle(frame_front, center_front, int(l_radius), utils.GREEN, 2, cv.LINE_AA)

                cv.polylines(frame_face, [np.array([mesh_points[p] for p in LEFT_IRIS], dtype=np.int32)], True,
                             utils.YELLOW, 2,
                             cv.LINE_AA)
                cv.polylines(frame_face, [np.array([mesh_points[p] for p in RIGHT_IRIS], dtype=np.int32)], True,
                             utils.YELLOW, 2,
                             cv.LINE_AA)

            out_face.write(frame_face)
            frame_face = cv.resize(frame_face, (960, 540))
            frame_front = cv.resize(frame_front, (960, 540))

            cv.imshow('face', frame_face)
            cv.imshow('front', frame_front)

            key = cv.waitKey(1)

            if key == ord('q'):
                break

cap_face.release()
cap_front.release()
out_front.release()
out_face.release()
cv.destroyAllWindows()
