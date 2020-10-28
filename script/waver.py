import time
import numpy as np            # install : conda install numpy
from scipy.io import wavfile  # install : conda install scipy
from pygame import mixer      # pip install pygame

def make():
    # パラメータ
    FREQ = 261.626          # 生成するサイン波の周波数（note#60 C4 ド）
    SAMPLE_RATE = 44100     # サンプリングレート
    # 16bitのwavファイルを作成
    wavfile.write("do.wav", SAMPLE_RATE,
                  (np.sin(np.arange(SAMPLE_RATE) * FREQ * np.pi * 2 / SAMPLE_RATE) * 32767.0).astype(np.int16))
    # wavファイルをロードして再生
    mixer.init()  # mixerを初期化
    mixer.music.load("do.wav")  # wavをロード
    mixer.music.play(1)  # wavを1回再生
    # 1秒（音がおわるまで）待つ
    time.sleep(1)


mixer.init()  # mixerを初期化
mixer.music.load("wave/do.wav")  # wavをロード

def sound(n=10):
    mixer.music.play(n)