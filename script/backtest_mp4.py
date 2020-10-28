import cv2
import os
import argparse
import copy
FPS = 5


def main():
    mp4_filepath = "video_2020-03-18.mp4"
    filename_without_suffix = mp4_filepath.split(".")[0]
    output_dirpath = "output/{}".format(filename_without_suffix)
    
    #os.system("rm -rf {}".format(output_dirpath))
    #os.makedirs(output_dirpath, exist_ok=True)
    
    cap = cv2.VideoCapture(mp4_filepath)
    
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    before_frame = None
    n = 0
    while True:
        n += 1
        ret, frame = cap.read()
        if not ret:
            break
        
    
if __name__ == "__main__":
    main()