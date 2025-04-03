import os
import cv2
import argparse
import natsort
import sys
import numpy as np
''' Stereo
    1. Load all images from folders
    2. List and sort file paths of left and right
    3. Find pairs which satisfies requirements
    4. Create and save video: horizontal and vertical
'''


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Create video from stereo images", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-il', '--input_left', type=str, default="", required=True)
    parser.add_argument('-ir', '--input_right', type=str, default="", required=True)
    parser.add_argument('-o', '--output', type=str, default="", required=True)
    parser.add_argument('-n', '--name', type=str, default="", required=True)
    parser.add_argument('-f', '--fps', type=int, default=30, required=False)
    parser.add_argument('-s', '--stack', type=str, default="horizontal", required=False)
    parser.add_argument('--width', type=int, default=640, required=False)
    parser.add_argument('--height', type=int, default=480, required=False)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("Create Video From Stereo Images")

    # initialize
    args = parse_arguments()
    input_left = args.input_left
    input_right = args.input_right
    fps = args.fps
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    img_size = (2 * args.width, args.height)
    if args.stack == "vertical":
        img_size = (args.width, args.height * 2)

    video_path = os.path.join(args.output, args.name + ".avi")
    print(video_path)
    video = cv2.VideoWriter(video_path, fourcc, fps, img_size)
    # check input path
    if not os.path.exists(input_left):
        print("[ERROR] Invalid Input path")
        sys.exit(0)
    if not os.path.exists(input_right):
        print("[ERROR] Invalid Input path")
        sys.exit(0)

    # process image paths
    limages = os.listdir(input_left)
    limages = [os.path.join(input_left, name) for name in limages]
    if not limages:
        print("No valid left images")
        sys.exit(0)
    limages = natsort.natsorted(limages)
    rimages = os.listdir(input_right)
    rimages = [os.path.join(input_right, name) for name in rimages]
    if not rimages:
        print("No valid right image")
        sys.exit(0)
    rimages = natsort.natsorted(rimages)

    count_pair = 0
    for limg_path in limages:
        lname = os.path.basename(limg_path)
        check_rpath = os.path.join(input_right, lname)
        if check_rpath not in rimages:
            continue

        cv_limg = cv2.imread(limg_path)
        cv_rimg = cv2.imread(check_rpath)
        if cv_limg is None or cv_rimg is None:
            print("Can not read pair frames")
            continue

        stereo_img = np.hstack([cv_limg, cv_rimg])
        if args.stack == "vertical":
            stereo_img = np.vstack([cv_limg, cv_rimg])
        video.write(stereo_img)
        cv2.imshow("Stereo Image CV", stereo_img)
        cv2.waitKey(1)
        count_pair += 1

    print("There are {} pairs".format(count_pair))
    # close
    video.release()
    cv2.destroyAllWindows()
