import cv2
import apriltag
import os
import natsort
import argparse
import sys
'''
    1. Load, sort, read images.
    2. Check if images are valid with defined aprilTag.
    3. Copy images to destination folder. 
'''


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Check valid AprilTag images", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_path', type=str, required=True)
    parser.add_argument('-o', '--output_path', type=str, required=True)
    parser.add_argument('-tw', '--tag_width', type=int, required=True)
    parser.add_argument('-th', '--tag_height', type=int, required=True)
    parser.add_argument('-d', '--debug', type=str, default="False", required=False)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("Check valid AprilTag images")

    # initialize
    args = parse_arguments()
    input_path = args.input_path
    output_path = args.output_path
    total_tags = args.tag_width * args.tag_height
    debug_mode = False if args.debug == "False" else True
    # check
    if not os.path.exists(input_path):
        print("ERROR: Invalid Input Path")
        sys.exit(0)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    images = [os.path.join(input_path, name) for name in os.listdir(input_path)]
    if not images:
        print("ERROR: Empty Folder, quit program")
        sys.exit(0)
    images = natsort.natsorted(images)

    detector = apriltag.Detector()
    for img in images:
        cv_img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        if cv_img is None:
            print("ERROR: Can not read image {}".format(img))
            continue
        tags = detector.detect(cv_img)
        if len(tags) != total_tags:
            print("Not enough recognized tags in image {}".format(img))
            continue

        valid_signal = True
        for idx, tag in enumerate(tags):
            if len(tag.corners) != 4:
                print(f"Not enough corners at tag {idx}")
                valid_signal = False
                break

        if valid_signal:
            output_file_name = os.path.join(output_path, os.path.basename(img))
            print("Output: {}".format(output_file_name))
            cv2.imwrite(output_file_name, cv_img)
            if debug_mode:
                cv2.imshow("Valid AprilTag Image", cv_img)
                cv2.waitKey(1)

    cv2.destroyAllWindows()
