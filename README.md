## Computer Vision with Python Scripts

### Introduction
- This repository contains many ready-to-go python scripts which are often used in computer vision tasks.
- They can be used as necessary tools across calibration, image pre-processing, etc, ...
- Tested environments:
    - Ubuntu 20.04
    - Ubuntu 22.04

### Installation
- Clone source, and navigate to stored folder.
  ```
  git clone https://github.com/NU-iz-da-fam/py-computer-vision
  ```
- Create virtual environment.
    ```
    python3 -m venv .pycv 
    source .pycv/bin/activate
    ```
- Install required packages.
    ```
    python3 -m pip install -r requirements.txt
    ```
### Execution
- Currently, repository has below functions.
- Assume you are at *py-computer-vision/scripts*
- Exact input arguments are described well in each script.

| Name 	| Notes | 
|---	|---	|
|create_video_from_images.py|  Used to create video from bundle of images.
|create_video_from_stereo_images.py|  Used to create video from stereo pairs, could be stack vertically or horizontally.
|resize_add_padding.py|  Resize images, keep ratio, and add padding.
|increase_brightness.py| Increase brightness of images within ranges.
|check_valid_chessboard_images.py| Check if images are valid for calibration, support chessboard, chessboardSB.
|check_valid_april_images.py|Check if images are valid for calibration using aprilTag.
|create_timestamps.py| Create dummy txt file which represent name of all images.
|rename_dataset.py| Rename images in folder with numerical order.
|image_alignment.py| Transfrom images from arbitrary to desired view.
|object_tracking.py| Object tracking using opencv.
|webcam_background_removal.py| Live webcam with custom background.
|create_edge_map_from_rgb.py| Get edge map from RGB image.
|basic_realsense_load_save.py| Load realsense, then save by keyboard.

### Certificate
- [OpenCV Bootcamp Cerfitiface](https://courses.opencv.org/certificates/d02d352f07bd4f7da09c223a59dd6c85)
### About me:
- Email: nguyenbku97@gmail.com 
- Leave me a star :dizzy: if it helps 
