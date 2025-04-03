import os
import cv2
import argparse
import sys
import natsort
'''
    Create a txt file which contain names of all images from a folder.
    - Notes: before running this scripts, ensure that images are synchronized.
'''


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Create dummy txt name file", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_path', type=str, required=True)
    parser.add_argument('-f', '--folder_name', type=str, required=True)
    parser.add_argument('-t', '--txt_name', type=str, default="times.txt", required=False)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print('[INFO] Create dummy txt name file')

    # initialize
    args = parse_arguments()
    input_path = args.input_path
    folder_name = args.folder_name
    txt_name = args.txt_name
    folder_path = os.path.join(input_path, folder_name)
    if not os.path.exists(folder_path):
        print("[ERROR] Invalid Input Path")
        sys.exit(0)
    txt_path = os.path.join(input_path, txt_name)

    # process
    images = os.listdir(folder_path)
    images = [os.path.join(folder_name, name) for name in images]
    images = natsort.natsorted(images)

    with open(txt_path, 'w') as dummy_txt:
        for image in images:
            last_name = os.path.basename(image)
            last_name = last_name.split(".")[0]
            last_name = str(float(last_name)/1e9)
            dummy_txt.write(last_name + "\n")

    print("Done")
