import cv2
import os
import argparse
import copy



FPS = 5

def test():
    mp4_filepath = "test_video_2020-03-22.mp4"
    output_dirpath = "test_output"
    
    os.system("rm -rf {}".format(output_dirpath))
    os.makedirs(output_dirpath, exist_ok=True)
    
    cap = cv2.VideoCapture(mp4_filepath)
    n = 0
    while True:
        n += 1
        ret, frame = cap.read()
        #if ret and n == 3000:
        if ret:
            cv2.imwrite('{}/test.jpg'.format(output_dirpath), frame)
            break


def main(args):
    mp4_filepath = args.mp4_filepath
    #mp4_filepath = "video_2020-05-01.mp4"
    filename_without_suffix = mp4_filepath.split(".")[0]
    output_dirpath = "output/{}".format(filename_without_suffix)
    
    os.system("rm -rf {}".format(output_dirpath))
    os.makedirs(output_dirpath, exist_ok=True)
    
    cap = cv2.VideoCapture(mp4_filepath)
    
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    before_frame = None
    n = 0
    while True:
        n += 1
        ret, frame = cap.read()
        if ret and n % (FPS * 60) == 0:
        #flag = is_same_img(frame, before_frame)
        #if ret and not flag:
        #if ret:
            cv2.imwrite('{}/{}_{}.jpg'.format(
                output_dirpath, filename_without_suffix, str(n).zfill(digit)), frame)
        before_frame = copy.deepcopy(frame)
        if not ret:
            break
        

def is_same_img(img, before_img):
    if img is None or before_img is None:
        return False
    return (img == before_img).all()

def _arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mp4_filepath")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    #test()
    args = _arg_parse()
    main(args)