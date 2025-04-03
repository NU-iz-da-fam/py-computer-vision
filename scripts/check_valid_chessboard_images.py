import os
import sys
import argparse
import cv2
import natsort

'''
    1. Load, sort, read images.
    2. Check if images are valid with defined calib patterns.
    3. Copy images to destination folder. 
'''


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check valid images for calibration", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-t', '--type', type=str,
                        default='chessboard', required=True, help="chessboard | chessboardSB")
    parser.add_argument('-cw', '--chessboard_width',
                        type=int, default=0, required=True)
    parser.add_argument('-ch', '--chessboard_height',
                        type=int, default=0, required=True)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("Check valid calibration images")

    # initialize
    args = parse_args()
    input_path = args.input
    output_path = args.output
    calib_type = args.type
    psize = (args.chessboard_width, args.chessboard_height)
    if not os.path.exists(input_path):
        print("ERROR: Invalid input path")
        sys.exit(0)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    assert (calib_type in ["chessboard", "chessboardSB"]
            ), "Invalid supported patterns"

    # processing
    images = [os.path.join(input_path, name) for name in os.listdir(input_path)]
    if not images:
        print("ERROR: No valid images")
        sys.exit(0)
    images = natsort.natsorted(images)
    print("[Input] There are {} images".format(len(images)))
    print("[Phase 1] Choose images which satisty loose conditions")
    for idx, image in enumerate(images):
        if idx % 100 == 0:
            print("Processing: {}/{}".format(idx, len(images)))
        frame = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        if frame is None:
            print("[Phase 1] Can not read frame {}".format(image))
            continue

        ret = False
        corners = None
        if calib_type == "chessboard":
            ret, corners = cv2.findChessboardCorners(frame, psize)
        elif calib_type == "chessboardSB":
            ret, corners = cv2.findChessboardCornersSB(frame, psize)

        if not ret or len(corners) != (psize[0]*psize[1]):
            continue

        new_image_name = os.path.join(output_path, os.path.basename(image))
        cv2.imwrite(new_image_name, frame)

    phase1_images = [os.path.join(output_path, name)
                     for name in os.listdir(output_path)]
    print("[Phase 2] Choose final valid images from {} images".format(len(phase1_images)))
    valid_count = 0
    for idx, image in enumerate(phase1_images):
        if idx % 100 == 0:
            print("Processing: {}/{}".format(idx, len(phase1_images)))
        frame = cv2.imread(image, cv2.IMREAD_UNCHANGED)
        if frame is None:
            print("[Phase 2] Can not read frame {}".format(image))
            continue

        ret = False
        corners = None
        if calib_type == "chessboard":
            ret, corners = cv2.findChessboardCorners(
                frame, psize, flags=cv2.CALIB_CB_ACCURACY)
        elif calib_type == "chessboardSB":
            ret, corners = cv2.findChessboardCornersSB(
                frame, psize, flags=cv2.CALIB_CB_ACCURACY)

        if not ret or len(corners) != (psize[0]*psize[1]):
            os.remove(image)
            continue

        valid_count += 1
    print("[Result] Choose {} valid images".format(valid_count))
