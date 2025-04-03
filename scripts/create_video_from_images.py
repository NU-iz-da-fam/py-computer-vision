import os
import cv2
import argparse
import natsort
import sys

''' Mono
    1. Load all images from folder
    2. List and sort file paths
    3. Create and save video
'''


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Create video from images", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, default="", required=True)
    parser.add_argument('-o', '--output', type=str, default="", required=True)
    parser.add_argument('-n', '--name', type=str, default="", required=True)
    parser.add_argument('-f', '--fps', type=int, default=30, required=False)
    parser.add_argument('--width', type=int, default=640, required=False)
    parser.add_argument('--height', type=int, default=480, required=False)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("Create Video From Images")
    # initialize
    args = parse_arguments()
    input_path = args.input
    fps = args.fps
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    img_size = (args.width, args.height)
    video_path = os.path.join(args.output, args.name + ".avi")
    print(video_path)
    video = cv2.VideoWriter(video_path, fourcc, fps, img_size)
    #
    if not os.path.exists(input_path):
        sys.exit(0)

    images = os.listdir(input_path)
    images = [os.path.join(input_path, name) for name in images]
    images = natsort.natsorted(images)
    for img_path in images:
        cv_img = cv2.imread(img_path)
        video.write(cv_img)
        cv2.imshow("Image CV", cv_img)
        cv2.waitKey(1)

    # close
    video.release()
    cv2.destroyAllWindows()
