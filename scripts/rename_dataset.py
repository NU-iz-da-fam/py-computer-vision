import os
import cv2
import argparse
import natsort
import sys


'''
    This script is used to rename dataset images counting from 0, 
    - Input: dataset folder with image_2 and image_3 subfolders
    - Notes: before running this script, make sure the images are synchronized

'''


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Rename dataset images", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, default="", required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("[INFO] Rename dataset images")

    # initialize
    args = parse_arguments()
    input_path = args.input
    image2_path = os.path.join(input_path, "image_2")
    image3_path = os.path.join(input_path, "image_3")
    if not os.path.exists(image2_path) and not os.path.exists(image3_path):
        print("[ERROR] Invalid Input path")
        sys.exit(0)

    # process image paths
    limages = os.listdir(image2_path)
    limages = [os.path.join(image2_path, name) for name in limages]
    if not limages:
        print("[ERROR] No valid images 2")
        sys.exit(0)
    limages = natsort.natsorted(limages)
    rimages = os.listdir(image3_path)
    rimages = [os.path.join(image3_path, name) for name in rimages]
    if not rimages:
        print("[ERROR] No valid images 3")
        sys.exit(0)
    rimages = natsort.natsorted(rimages)

    # rename images, before performing this, make sure the images are synchronized
    for idx, (limg_path, rimg_path) in enumerate(zip(limages, rimages)):
        new_limg_path = os.path.join(image2_path, "{:06d}.png".format(idx))
        new_rimg_path = os.path.join(image3_path, "{:06d}.png".format(idx))
        os.rename(limg_path, new_limg_path)
        os.rename(rimg_path, new_rimg_path)
    print("Done")
