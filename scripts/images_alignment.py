import os
import cv2
import argparse
import natsort
import sys
import numpy as np
from copy import deepcopy


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="align images, using homography", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-is', '--input_source', type=str, default="", required=True)
    parser.add_argument('-it', '--input_target', type=str, default="", required=True)
    parser.add_argument('-o', '--output', type=str, default="", required=True)
    parser.add_argument('-mf', '--max_features', type=int, default=500, required=False)
    parser.add_argument('-pm', '--percent_good', type=int, default=15, required=False)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("Align images, transfrom source image to target image")
    args = parse_arguments()

    # initialize params
    source_path = args.input_source
    target_path = args.input_target
    output_path = args.output
    MAX_FEATURES = args.max_features
    PERCENT_GOOD_MATCHES = float(args.percent_good) / 100
    if not os.path.exists(source_path) and not os.path.exists(target_path):
        print("[ERROR] Invalid Input Path, please check")
        sys.exit(0)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print("[INFO] Output path created")

    # load images
    simg = cv2.imread(source_path, cv2.IMREAD_COLOR)
    simg = cv2.cvtColor(simg, cv2.COLOR_BGR2RGB)
    timg = cv2.imread(target_path, cv2.IMREAD_COLOR)
    timg = cv2.cvtColor(timg, cv2.COLOR_BGR2RGB)
    # convert to gray
    simg_gray = cv2.cvtColor(simg, cv2.COLOR_BGR2GRAY)
    timg_gray = cv2.cvtColor(timg, cv2.COLOR_BGR2GRAY)

    # orb features, and compute descriptors
    orb = cv2.ORB_create(MAX_FEATURES)
    kp1, des1 = orb.detectAndCompute(simg_gray, None)
    kp2, des2 = orb.detectAndCompute(timg_gray, None)

    # match features
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = list(matcher.match(des1, des2, None))
    matches.sort(key=lambda x: x.distance, reverse=False)

    # keep only good matches
    num_good_matches = int(len(matches) * PERCENT_GOOD_MATCHES)
    matches = matches[:num_good_matches]

    # find homography matrix
    src_pts = np.zeros((len(matches), 2), dtype=np.float32)
    dst_pts = np.zeros((len(matches), 2), dtype=np.float32)
    for i, match in enumerate(matches):
        src_pts[i, :] = kp1[match.queryIdx].pt
        dst_pts[i, :] = kp2[match.trainIdx].pt

    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)

    # wrap images
    h, w, c = simg.shape
    timg_warped = cv2.warpPerspective(simg, H, (w, h))
    timg_warped = cv2.cvtColor(timg_warped, cv2.COLOR_BGR2RGB)

    # save image
    cv2.imwrite(os.path.join(output_path, "aligned.jpg"), timg_warped)

    # show all images
    timg_show = deepcopy(timg)
    timg_show = cv2.resize(timg_show, dsize=None, fx=0.5, fy=0.5)
    timg_warped_show = deepcopy(timg_warped)
    timg_warped_show = cv2.resize(timg_warped_show, dsize=None, fx=0.5, fy=0.5)
    cv2.imshow("Target Image", timg_show)
    cv2.imshow("Wrapped Image", timg_warped_show)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
