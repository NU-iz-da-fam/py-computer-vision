import os
import cv2
import argparse
import natsort
import sys
import numpy as np


def parse_arguments():
    ''''''
    parser = argparse.ArgumentParser(
        description="Increase brightness of images", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, default="", required=True)
    parser.add_argument('-b', '--brightness', type=int, default=50, required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("Increase brightness of images")
    args = parse_arguments()

    # initialize params
    input_path = args.input
    dbrightness = args.brightness

    if not os.path.exists(input_path):
        print("Invalid Input Path")
        sys.exit(0)

    # load images
    images = [os.path.join(input_path, name) for name in os.listdir(input_path)]
    images = natsort.natsorted(images)

    for img in images:
        cv_img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
        matrix = np.ones(cv_img.shape, dtype="uint8") * dbrightness

        # enhance brightness
        brighter_cv_img = cv2.add(cv_img, matrix)

        cv2.imshow("Enhanced Image", brighter_cv_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
