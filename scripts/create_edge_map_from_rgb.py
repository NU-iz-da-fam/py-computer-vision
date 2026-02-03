import os
import cv2
import argparse
import natsort
import sys
import numpy as np

'''
1. Load RGB
2. Convert to grayscale
3. Apply canny edge detection
'''

def parse_argument():
    parser = argparse.ArgumentParser(
        description="Create video from stereo images", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_image', type=str, default="", required=True)
    parser.add_argument('-o', '--output_path', type=str, default="", required=True)
    parser.add_argument('-n', '--name', type=str, default="", required=True)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    print("Create edge map from RGB image")

    # initialize 
    args = parse_argument()
    input_path = args.input_image 
    output_path = args.output_path
    output_name = args.name + ".png"
    output_name = os.path.join(output_path, output_name)

    # check 
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(input_path):
        print("ERROR: Invalid Input Path")
        sys.exit(0)
    
    image = cv2.imread(input_path)
    intensity_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # edge detection
    lower_threshold = 50
    upper_threshold = 100
    edges_canny = cv2.Canny(intensity_image, lower_threshold, upper_threshold)
    edges_canny = 255 - edges_canny # negative

    # concat and show
    concat_image = np.hstack([intensity_image, edges_canny])
    concat_resize = cv2.resize(concat_image, (1280,480))
    cv2.imshow("RGB & Edge Map", concat_resize)
    cv2.waitKey(0)

    # save image
    cv2.imwrite(output_name, edges_canny)
    cv2.destroyAllWindows()