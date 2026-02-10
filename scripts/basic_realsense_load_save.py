import os 
import cv2
import argparse
import natsort
import numpy as np
import pyrealsense2 as rs

def parse_arguments():
    parser = argparse.ArgumentParser(description="load realsense, then save", 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output', type=str, default="", required=True)
    args = parser.parse_args()
    
    return args


if __name__ == "__main__":
    print("Load realsense camera, then save image as required")
    args = parse_arguments()

    # initialize 
    output_path = args.output
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    img_id = 0
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # start camera
    profile = pipeline.start(config)
    device = profile.get_device()
    camera_name = device.get_info(rs.camera_info.name)
    print("Starting realsense camera ", camera_name)

    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imshow('RealSense Camera', color_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            file_name = os.path.join(output_path, str(img_id) + ".png")
            cv2.imwrite(file_name, color_image)
            print(f"Save successfully: {file_name}")
            img_id += 1
            
        elif key == ord('q') or key == 27:
            print("Close camera")
            break
    
    pipeline.stop()
    cv2.destroyAllWindows()
