import os
import cv2
import argparse
import sys
import numpy as np
from copy import deepcopy

'''
    Concepts:
        1. Load Video
        2. Define an initial bounding box
        3. Initialize tracker
        4. Perform tracking
        5. Save output video
'''


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="object tracking opencv", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_source', type=str, default="", required=True)
    parser.add_argument('-o', '--output', type=str, default="", required=True)
    parser.add_argument('-t', '--tracker_id', type=int, default=0, required=True)
    args = parser.parse_args()
    return args


def draw_rectangle(frame, bbox):
    '''x, y : top left | x + w, y + h : bottom right'''
    x, y, w, h = bbox
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


def display_rectangle(frame, bbox):
    draw_rectangle(frame, bbox)
    copy_frame = deepcopy(frame)
    cv2.imshow("Object Tracking", copy_frame)


def draw_text(frame, txt, location, color=(50, 170, 50)):
    cv2.putText(frame, txt, location, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)


def choose_tracker(tracker_id: str = ""):
    if tracker_id == "MIL":
        return cv2.TrackerMIL_create()
    elif tracker_id == "KCF":
        return cv2.TrackerKCF_create()
    elif tracker_id == "CSRT":
        return cv2.TrackerCSRT_create()


if __name__ == "__main__":
    print("Object tracking using opencv")
    # initialize
    args = parse_arguments()
    input_path = args.input_source
    output_path = args.output
    id = args.tracker_id

    # tracker collections
    tracker_types = [
        "MIL",
        "KCF",
        "CSRT",
    ]
    # change trackger
    tracker_id = tracker_types[id]
    tracker = choose_tracker(tracker_id)
    print("[INFO] Using tracker: ", tracker_id)

    video = cv2.VideoCapture(input_path)
    if not video.isOpened():
        print("[ERROR] Invalid Input Path, please check")
        sys.exit(1)

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # create output path
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print("[INFO] Output path created")
    name = os.path.basename(input_path).split(".")[0]
    name = name + "_" + tracker_id + ".avi"
    output_video_path = os.path.join(output_path, name)
    vid = cv2.VideoWriter(output_video_path,
                          cv2.VideoWriter_fourcc(*"XVID"), 10, (width, height))

    # define an initial bounding box
    bbox = (1300, 405, 160, 120)
    ret, frame = video.read()
    display_rectangle(frame, bbox)

    # initialize tracker
    ret = tracker.init(frame, bbox)
    if ret is not None:
        print("[ERROR] Tracker initialization failed")
        sys.exit(0)

    while (True):
        ret, frame = video.read()
        if not ret:
            print("[INFO] Video ended")
            break

        ok, bbox = tracker.update(frame)
        if ok:
            display_rectangle(frame, bbox)
        else:
            draw_text(frame, "Tracking failure detected", (100, 200), (0, 0, 255))

        # write frame
        vid.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Exiting...")
            break

    video.release()
    vid.release()
    cv2.destroyAllWindows()
