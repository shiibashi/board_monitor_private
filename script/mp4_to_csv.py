import cv2
import os
import argparse
import copy

from PIL import Image
import datetime
import numpy
import cv2
import time
import os
import pandas

import predict
import argparse
FPS = 5

DATA_COLUMNS = ["over", "under", "upper_price", "downer_price",
    "over_player", "over_1_player", "over_2_player", "over_3_player", "over_4_player",
    "over_5_player", "over_6_player", "over_7_player", "over_8_player",
    "over_9_player", "over_10_player", "over_11_player", "over_12_player",
    "over_13_player", "over_14_player", "over_15_player", "over_16_player",

    "over_sell", "over_1_sell", "over_2_sell", "over_3_sell", "over_4_sell",
    "over_5_sell", "over_6_sell", "over_7_sell", "over_8_sell",
    "over_9_sell", "over_10_sell", "over_11_sell", "over_12_sell",
    "over_13_sell", "over_14_sell", "over_15_sell", "over_16_sell",

    "under_buy", "under_1_buy", "under_2_buy", "under_3_buy", "under_4_buy",
    "under_5_buy", "under_6_buy", "under_7_buy", "under_8_buy",
    "under_9_buy", "under_10_buy", "under_11_buy", "under_12_buy",
    "under_13_buy", "under_14_buy", "under_15_buy", "under_16_buy",

    "under_player", "under_1_player", "under_2_player", "under_3_player", "under_4_player",
    "under_5_player", "under_6_player", "under_7_player", "under_8_player",
    "under_9_player", "under_10_player", "under_11_player", "under_12_player",
    "under_13_player", "under_14_player", "under_15_player", "under_16_player"
]


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
    ocr = predict.OCR("model/model.hdf5")
    data_list = []

    mp4_filepath = args.mp4_filepath #"video_2020-03-26.mp4"
    filename_without_suffix = mp4_filepath.split(".")[0]
    output_dirpath = "output_csv/{}".format(filename_without_suffix)
    
    #os.system("rm -rf {}".format(output_dirpath))
    #os.makedirs(output_dirpath, exist_ok=True)
    
    cap = cv2.VideoCapture(mp4_filepath)
    
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    before_frame = None
    n = 0
    t = 0
    while True:
        n += 1
        ret, frame = cap.read()
        if ret:
            png = Image.fromarray(frame)
            ocr_data = ocr.predict(png)
            #print(ocr_data)
            print("{}_{}_{}_{}".format(ocr_data["over"], ocr_data["under"], ocr_data["upper_price"], ocr_data["downer_price"]), flush=True)
            data = [n] + [ocr_data[col] for col in DATA_COLUMNS]
            data_list.append(data)
        else:
            break
    df = pandas.DataFrame(data_list, columns=["time"]+DATA_COLUMNS)
    #df = pandas.DataFrame(data_list, columns=["time", "over", "under", "upper_price", "downer_price"])
    df.to_csv("output_csv/{}.csv".format(filename_without_suffix), index=False)


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