import cv2
import os
import argparse
import sys
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=" Webcam Background Removal", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_background', type=str, default= "",required=True)
    parser.add_argument('-n', '--name', type=str, default= "", required=False)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    print("[INFO] Webcam Background Removal")

    # initialize
    args = parse_arguments()
    background_dir = args.input_background
    video_name = args.name

    # open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Can not open webcam")
        exit()
    
    # camera setting
    fwidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fheight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    init_rect = False
    des_x = 300;   des_y = 400
    x1 = (fwidth - des_x) // 2
    y1 = (fheight - des_y)
    rect = (x1, y1, des_x, des_y)
    mask = np.zeros((fheight, fwidth), np.uint8)
    bg_model = None
    fg_model = None
    while True:
        bg_image = cv2.imread(background_dir, cv2.IMREAD_UNCHANGED)
        bg_image = cv2.resize(bg_image, (fwidth, fheight))

        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read webcam frame")
            break
        
        if not init_rect:
            # mask = np.zeros((fheight, fwidth), np.uint8)
            bg_model = np.zeros((1, 65), np.float64)
            fg_model = np.zeros((1, 65), np.float64)
            cv2.grabCut(frame, mask, rect, bg_model, fg_model, iterCount=1,
                    mode=cv2.GC_INIT_WITH_RECT)
        else:
            cv2.grabCut(frame, mask, None, bg_model, fg_model, iterCount=1,
                    mode=cv2.GC_EVAL)
        
        init_rect = True
        mask2 = np.where((mask == 0) | (mask == 2), 0, 1).astype("uint8")
        # print("Unique values:", np.unique(mask))
        mask2 = cv2.GaussianBlur(mask2, (7, 7), 0)
        
        foreground = cv2.bitwise_and(frame, frame, mask=mask2)
        bg_image = cv2.bitwise_and(bg_image, bg_image, mask=(1 - mask2))
        result = cv2.add(foreground, bg_image)
        result = result.astype("uint8")

        cv2.imshow("Nuizafam Webcam", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Done")


