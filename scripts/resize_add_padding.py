import os
import glob
import cv2
import argparse
import natsort
import sys


def parse_arguments():
    ''''''
    parser = argparse.ArgumentParser(
        description="Resize, keep ratio and add padding", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, default="", required=True)
    parser.add_argument('-o', '--output', type=str, default="", required=True)
    parser.add_argument('-p', '--prefix', type=str, default="", required=False)
    parser.add_argument('--height', type=int, default=480, required=False)
    parser.add_argument('--width', type=int, default=640, required=False)
    parser.add_argument('-d', '--debug', type=bool, default=False)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("Resize, keep ratio and add padding")
    args = parse_arguments()

    # initialize params
    input_path = args.input
    output_path = args.output
    prefix = args.prefix
    dh = args.height
    dw = args.width
    debug_mode = args.debug
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    #
    images = glob.glob(input_path + "/{}*.png".format(prefix))
    images = natsort.natsorted(images)
    if not images:
        print("Empty folder, quit program")
        sys.exit(0)

    ref_img = cv2.imread(images[0], cv2.IMREAD_UNCHANGED)
    h, w = ref_img.shape[:2]

    ratio = max(h/dh, w/dw)  # could be float
    print("Ratio: ", ratio)

    for img in images:
        cv_img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
        if cv_img is None:
            print("Invalid Image {}".format(img))
            continue
        new_w = int(w/ratio)
        new_h = int(h/ratio)
        resize_img = cv2.resize(cv_img, (new_w, new_h),
                                interpolation=cv2.INTER_LINEAR)

        # padding
        pad_top = int((dh - new_h)/2)
        pad_bottom = dh - new_h - pad_top
        pad_left = int((dw - new_w)/2)
        pad_right = dw - new_w - pad_left
        padded_image = cv2.copyMakeBorder(
            resize_img, pad_top, pad_bottom, pad_left, pad_right,
            borderType=cv2.BORDER_CONSTANT, value=(0, 0, 0)
        )
        padded_image_name = os.path.join(output_path, os.path.basename(img))
        cv2.imwrite(padded_image_name, padded_image)
        if debug_mode:
            cv2.imshow("Resized & Padding Image", padded_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
