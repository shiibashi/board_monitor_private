from PIL import ImageGrab
from PIL import Image
from PIL import ImageDraw, ImageFont
import datetime
import numpy
import cv2
import time
import os

SHAPE =(1000, 810)
FPS = 5
BOX_AREA = (0, 140, 1000, 950) # x1, y1, x2, y2

FROM_TIME = "08-30-00"
TO_TIME = "15-00-00"


def main():
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    today = datetime.datetime.today()
    hms = today.strftime("%Y-%m-%d")
    video = cv2.VideoWriter('test_video_{}.mp4'.format(hms), fourcc, FPS, SHAPE)
    before_img = None
    #wait()
    for i in range(10):
        time.sleep(1)
        print(i)
        img = get_screen_shot()
        img = cv2.resize(img, SHAPE)
        #if before_img is None or not is_same_img(img, before_img):
        time_png = get_time_img()
        png = Image.fromarray(img)
        png.paste(time_png, (png.size[0] - time_png.size[0], 0))
        img_pasted = numpy.array(png)
        video.write(img_pasted)
        before_img = img
        #else:
        #    pass
        #if not market_time():
        #    break
    video.release()
    #os.system("shutdown -s -t 5")

def main_1():
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    today = datetime.datetime.today()
    hms = today.strftime("%Y-%m-%d")
    video = cv2.VideoWriter('video_{}_1.mp4'.format(hms), fourcc, FPS, SHAPE)
    before_img = None
    wait()
    for i in range(390*60):
        time.sleep(1)
        print(i)
        img = get_screen_shot()
        img = cv2.resize(img, SHAPE)
        #if before_img is None or not is_same_img(img, before_img):
        time_png = get_time_img()
        png = Image.fromarray(img)
        png.paste(time_png, (png.size[0] - time_png.size[0], 0))
        img_pasted = numpy.array(png)
        video.write(img_pasted)
        before_img = img
        #else:
        #    pass
        if not market_time():
            break
    video.release()


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

def is_same_img(img, before_img):
    return (img == before_img).all()

def get_screen_shot():
    img = ImageGrab.grab(bbox=BOX_AREA)
    img_array = numpy.array(img)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    #png = Image.fromarray(img_array_rgb)
    return img_array


if __name__ == "__main__":
    main()