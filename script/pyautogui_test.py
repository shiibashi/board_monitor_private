#from PIL import ImageGrab
#from PIL import Image
#from PIL import ImageDraw, ImageFont
import datetime
import numpy
import cv2
import time
import os
import pandas

#import predict
import pyautogui
import sys


def main():
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')

def test():
    pyautogui.click(x=505, y=567)


if __name__ == "__main__":
    #main()
    test()