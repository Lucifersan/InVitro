import argparse
import os
import sys
import time
import numpy as np
import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import FileVideoStream, VideoStream
from scipy.spatial import distance as dist
from eyeware.client import TrackerClient
import multiprocessing as mp

<<<<<<< Updated upstream
=======
<<<<<<< HEAD
#uwu

=======
>>>>>>> 4c8b8c9addfcc2959ecef57ba22fd95c4ef8efe5
>>>>>>> Stashed changes
import params

def start_blink_loop():
    print("start_blink_loop", detector)
    open("shared_int", "w").write("True")
    p = mp.Process(target=eye_state_loop, args=(detector, predictor, lStart, lEnd, rStart, rEnd))
    p.start()

detector, predictor, lStart, lEnd, rStart, rEnd, tracker = None, None, None, None, None, None, None,

def init(args):
    print("Received", args)
    global detector, predictor, lStart, lEnd, rStart, rEnd, tracker
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    print(detector)
    predictor = dlib.shape_predictor(args["shape_predictor"])
    assert(detector is not None)

    lStart, lEnd = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    rStart, rEnd = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    
    tracker = TrackerClient()
    print("Finished loading items")

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def get_eye_state(frame, gray, detector, predictor, lStart, lEnd, rStart, rEnd):
    """
    Returns whether or not eyes are closed.
        0: Closed
        1: Open
    """
    rects = detector(gray, 0)

    if rects:
        focus = rects[0] # take one pair of eyes

        shape = predictor(gray, focus)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0
        return ear > params.EYE_AR_THRESH

eye_reading_queue = [True for _ in range(params.BLINK_SMOOTHING)]

def get_eye_state_smoothed(frame, gray, detector, predictor, lStart, lEnd, rStart, rEnd):
    """
    Return a smoothed version of get_eye_state.
        0: Open
        1: Closed
    """
    global eye_reading_queue
    reading = get_eye_state(frame, gray, detector, predictor, lStart, lEnd, rStart, rEnd)

    if reading is not None:
        eye_reading_queue = [reading] + eye_reading_queue[:-1]

    return 2 * sum(eye_reading_queue) > len(eye_reading_queue)

def eye_state_loop(detector, predictor, lStart, lEnd, rStart, rEnd):

    print("[INFO] starting video stream thread...") 
    #vs = FileVideoStream(args["video"]).start() # TODO: investigate error here (in cpp??) 
    #fileStream = True
    vs = VideoStream(src=0).start()
    #fileStream = False

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        v = get_eye_state_smoothed(frame, gray, detector, predictor, lStart, lEnd, rStart, rEnd)
        open("shared_int", "w").write(str(v))

def pull_gaze_info():
    if tracker.connected:
        return tracker.get_screen_gaze_info()
    
def pull_blink_state():
    return open("shared_int", "r").read() == "True"
