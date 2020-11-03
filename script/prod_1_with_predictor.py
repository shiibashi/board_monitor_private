from PIL import ImageGrab
from PIL import Image
from PIL import ImageDraw, ImageFont
import datetime
import numpy
import cv2
import time
import os
import pandas

import predict
import rl
import waver

SHAPE =(1000, 810)
FPS = 5
BOX_AREA = (0, 140, 1000, 950) # x1, y1, x2, y2

FROM_TIME = "08-30-00"
TO_TIME = "15-00-00"

        
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
    "under_13_player", "under_14_player", "under_15_player", "under_16_player",
    
    "volume_sum"
]

TODAY = datetime.datetime.today()
YMD = TODAY.strftime("%Y-%m-%d")

def main():
    rlbotter = rl.RLBotter()
    ocr = predict.OCR("model/model.hdf5")
    data_list = []
    
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    video = cv2.VideoWriter('daily_output/video_{}.mp4'.format(YMD), fourcc, FPS, SHAPE)
    wait()
    timing = rl.get_trade_timing()
    trade_hms = timing.pop(0)
    trade_history = []
    for i in range(390*60):
        time.sleep(1)
        print(i)
        png, img_pasted = img_for_video()
        video.write(img_pasted)

        today = datetime.datetime.today()
        t = today.strftime("%Y-%m-%d-%H-%M-%S")
        hms = today.strftime("%H-%M-%S")

        ocr_data = ocr.predict(png)
        print("{}_{}_{}_{}_{}".format(rlbotter.status, ocr_data["over"], ocr_data["under"], ocr_data["upper_price"], ocr_data["downer_price"]), flush=True)
        data = [t] + [ocr_data[col] for col in DATA_COLUMNS]
        data_list.append(data) # 最後のfeatureで推論する
        
        if not market_time():
            break
        
        try:
            if hms >= trade_hms and len(data_list) > 300 and len(timing) > 0:
                print("trade_hms_{}".format(trade_hms))
                trade_hms = timing.pop(0)
                df_origin = pandas.DataFrame(data_list, columns=["time"]+DATA_COLUMNS)
                df_processed = rlbotter.origin_to_processed(df_origin)
                df_extracted = rlbotter.processed_to_extracted(df_processed, YMD)
                df_feature = rlbotter.extracted_to_feature(df_extracted).tail(1).reset_index(drop=True)
                rlbotter.feature_to_action(df_feature)
                
                if rlbotter.status == "buy":
                    waver.sound(n=10)
                    trade_history.append(hms)

        except Exception as e:
            print("ERROR")
            pass
            
        #if not market_time():
        #    break
    video.release()
    df_origin = pandas.DataFrame(data_list, columns=["time"]+DATA_COLUMNS)
    df_origin.to_csv("daily_output/log_{}.csv".format(YMD), index=False)
    df_processed = rlbotter.origin_to_processed(df_origin)
    df_processed.to_csv("daily_output/log_processed_{}.csv".format(YMD), index=False)
    # df_processed->df_extractedの変換はapiでやるようにする
    df_extracted = rlbotter.processed_to_extracted(df_processed, YMD)
    df_extracted.to_csv("daily_output/log_extracted_{}.csv".format(YMD), index=False)
    #os.system("shutdown -s -t 5")
    print(trade_history)

def wait():
    for i in range(390*60):
        time.sleep(1)
        #print("wait")
        if market_time():
            break

def market_time():
    today = datetime.datetime.today()
    hms = today.strftime("%H-%M-%S")
    return FROM_TIME <= hms <= TO_TIME

def get_time_img():
    time_text_position = (5, 25)
    mask = Image.new("RGB", (150, 50), 0)
    draw = ImageDraw.Draw(mask)
    today = datetime.datetime.today()
    message = today.strftime("%Y-%m-%d-%H-%M-%S")
    draw.text(time_text_position, message, fill=(255, 255, 255))
    mask_2 = mask.resize((300, 100))
    return mask_2


def get_screen_shot():
    img = ImageGrab.grab(bbox=BOX_AREA)
    img_array = numpy.array(img)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    #png = Image.fromarray(img_array_rgb)
    return img_array

def img_for_video():
    img = get_screen_shot()
    img = cv2.resize(img, SHAPE)
    time_png = get_time_img()
    png = Image.fromarray(img)
    png.paste(time_png, (png.size[0] - time_png.size[0], 0))
    img_pasted = numpy.array(png)
    return png, img_pasted

def test():
    rlbotter = rl.RLBotter()
    ocr = predict.OCR("model/model.hdf5")
    data_list = []
    
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    today = datetime.datetime.today()
    video = cv2.VideoWriter('video_{}.mp4'.format(YMD), fourcc, FPS, SHAPE)
    
    timing = rl.get_trade_timing()
    trade_hms = timing.pop(0)
    for i in range(60 * 6):
        time.sleep(1)
        print(i)
        png, img_pasted = img_for_video()
        video.write(img_pasted)
        
        today = datetime.datetime.today()
        t = today.strftime("%Y-%m-%d-%H-%M-%S")
        hms = today.strftime("%H-%M-%S")
        
        ocr_data = ocr.predict(png)
        print("{}_{}_{}_{}_{}".format(
            hms, ocr_data["over"], ocr_data["under"], ocr_data["upper_price"], ocr_data["downer_price"]), flush=True)
        data = [t] + [ocr_data[col] for col in DATA_COLUMNS]
        data_list.append(data)

        
        if hms >= trade_hms and len(data_list) > 10 and len(timing) > 0:
            print("trade_hms_{}".format(trade_hms))
            trade_hms = timing.pop(0)
            df_origin = pandas.DataFrame(data_list, columns=["time"]+DATA_COLUMNS)
            df_processed = rlbotter.origin_to_processed(df_origin)
            df_extracted = rlbotter.processed_to_extracted(df_processed, YMD)
            df_feature = rlbotter.extracted_to_feature(df_extracted).tail(1).reset_index(drop=True)
            rlbotter.feature_to_action(df_feature)
            
            if rlbotter.status == "buy":
                waver.sound(n=10)
        #if not market_time():
        #    break
        print(rlbotter.status)
    video.release()
    df = pandas.DataFrame(data_list, columns=["time"]+DATA_COLUMNS)
    df.to_csv("test.csv".format(YMD), index=False)

def main_log_processed_to_extracted():
    DTYPE_2 = {
        "time": object,
        "over": int,
        "under": int,
        "upper_price": int,
        "downer_price": int,
        "over_under": float,
        "hms": object,
        "volume_sum": int
    }
    rlbotter = rl.RLBotter()
    filepath_list = os.listdir("daily_output")
    for filepath in filepath_list:
        if "log_processed" not in filepath:
            continue
        ymd = filepath.split("_")[2].split(".")[0]
        df_processed = pandas.read_csv("daily_output/{}".format(filepath), dtype=DTYPE_2)
        if "volume_sum" not in df_processed.columns:
            continue
        csv_path = "daily_output/log_extracted_{}.csv".format(ymd)
        if os.path.exists(csv_path):
            continue
        print(filepath)
        df_extracted = rlbotter.processed_to_extracted(df_processed, ymd)
        df_extracted.to_csv(csv_path, index=False)

if __name__ == "__main__":
    main()
    #test()
    #main_log_processed_to_extracted()