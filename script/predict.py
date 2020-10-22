import json
import os
import numpy
from PIL import Image

from keras import models
from keras.models import Model
from keras import Input
from keras.layers import Activation, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.callbacks import TensorBoard, ModelCheckpoint

import area_param

def make_model(feature_shape, label_num):
    activation = 'relu'

    model = models.Sequential()

    model.add(Conv2D(32, (3, 3), padding='same', name='conv1',
            input_shape=(feature_shape[0], feature_shape[1], feature_shape[2])))
    model.add(Activation(activation, name='act1'))
    model.add(MaxPooling2D((2, 2), name='pool1'))

    model.add(Conv2D(64, (3, 3), padding='same', name='conv2'))
    model.add(Activation(activation, name='act2'))
    model.add(MaxPooling2D((2, 2), name='pool2'))

    model.add(Conv2D(64, (3, 3), padding='same', name='conv3'))
    model.add(Activation(activation, name='act3'))

    model.add(Flatten(name='flatten'))
    model.add(Dense(64, name='dense4'))
    model.add(Activation(activation, name='act4'))
    model.add(Dense(label_num, name='dense5'))
    model.add(Activation('softmax', name='last_act'))
    return model

def make_model_4(feature_shape, label_num):
    activation = 'relu'

    model = models.Sequential()

    model.add(Conv2D(16, (3, 3), padding='same', name='conv1',
            input_shape=(feature_shape[0], feature_shape[1], feature_shape[2])))
    model.add(Activation(activation, name='act1'))
    model.add(MaxPooling2D((2, 2), name='pool1'))

    model.add(Conv2D(32, (3, 3), padding='same', name='conv2'))
    model.add(Activation(activation, name='act2'))
    model.add(MaxPooling2D((2, 2), name='pool2'))


    model.add(Flatten(name='flatten'))
    model.add(Dense(16, name='dense4'))
    model.add(Activation(activation, name='act4'))
    model.add(Dense(label_num, name='dense5'))
    model.add(Activation('softmax', name='last_act'))
    return model

def read_json(json_filepath):
    with open(json_filepath, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d

#def normalize_image(image):
#    img = image.convert("L").resize((20, 20))
#    arr = (numpy.array(img) / 255.0).reshape(20, 20, 1)
    return arr

def normalize_image(image):
    img = image.resize((20, 20))
    arr = (numpy.array(img) / 255.0).reshape(20, 20, 3)
    return arr

def read_jpg(jpg_filepath):
    img = Image.open(jpg_filepath)
    return img

def crop_annotation_region(image, p1, p2):
    cropped = image.crop((p1[0], p1[1], p2[0], p2[1]))
    return cropped

def convert_nn_input(image, area):
    arr_list = []
    for a in area:
        x = a["x"]
        y = a["y"]
        width = a["width"]
        height = a["height"]
        p1 = (x, y)
        p2 = (x+width, y+height)
        cropped_image = crop_annotation_region(image, p1, p2)
        arr = normalize_image(cropped_image)
        arr_list.append(arr)
    return numpy.array(arr_list)

def predict_nn(model, arr):
    pred = model.predict(arr)
    value = pred.argmax(axis=1)
    return value

def to_value(value_list):
    try:
        v = int("".join([str(v) for v in value_list if v not in [11, 10]]))
    except Exception:
        v = 0
    return v

class OCR(object):
    #model.load_weights("model.hdf5")
    def __init__(self, model_filepath):
        self.feature_shape = (20, 20, 3)
        self.label_num = 11
        self.model_filepath = model_filepath
        model = make_model_4(self.feature_shape, self.label_num)
        model.load_weights(self.model_filepath)
        self.model = model

    def _predict(self, image, area):
        area_arr = convert_nn_input(image, area)
        value_list = predict_nn(self.model, area_arr)
        value = to_value(value_list)
        return value

    def predict(self, image):
        over_value = self._predict(image, area_param.over_area)
        under_value = self._predict(image, area_param.under_area)
        upper_price_value = self._predict(image, area_param.upper_price_area)
        downer_price_value = self._predict(image, area_param.downer_price_area)
        
        data = {
            "over": self._predict(image, area_param.over_area),
            "under": self._predict(image, area_param.under_area),
            "upper_price": self._predict(image, area_param.upper_price_area),
            "downer_price": self._predict(image, area_param.downer_price_area),
            
            "over_player": self._predict(image, area_param.over_player_area),
            "over_1_player": self._predict(image, area_param.over_1_player_area),
            "over_2_player": self._predict(image, area_param.over_2_player_area),
            "over_3_player": self._predict(image, area_param.over_3_player_area),
            "over_4_player": self._predict(image, area_param.over_4_player_area),
            "over_5_player": self._predict(image, area_param.over_5_player_area),
            "over_6_player": self._predict(image, area_param.over_6_player_area),
            "over_7_player": self._predict(image, area_param.over_7_player_area),
            "over_8_player": self._predict(image, area_param.over_8_player_area),
            "over_9_player": self._predict(image, area_param.over_9_player_area),
            "over_10_player": self._predict(image, area_param.over_10_player_area),
            "over_11_player": self._predict(image, area_param.over_11_player_area),
            "over_12_player": self._predict(image, area_param.over_12_player_area),
            "over_13_player": self._predict(image, area_param.over_13_player_area),
            "over_14_player": self._predict(image, area_param.over_14_player_area),
            "over_15_player": self._predict(image, area_param.over_15_player_area),
            "over_16_player": self._predict(image, area_param.over_16_player_area),

            "over_sell": self._predict(image, area_param.over_sell_area),
            "over_1_sell": self._predict(image, area_param.over_1_sell_area),
            "over_2_sell": self._predict(image, area_param.over_2_sell_area),
            "over_3_sell": self._predict(image, area_param.over_3_sell_area),
            "over_4_sell": self._predict(image, area_param.over_4_sell_area),
            "over_5_sell": self._predict(image, area_param.over_5_sell_area),
            "over_6_sell": self._predict(image, area_param.over_6_sell_area),
            "over_7_sell": self._predict(image, area_param.over_7_sell_area),
            "over_8_sell": self._predict(image, area_param.over_8_sell_area),
            "over_9_sell": self._predict(image, area_param.over_9_sell_area),
            "over_10_sell": self._predict(image, area_param.over_10_sell_area),
            "over_11_sell": self._predict(image, area_param.over_11_sell_area),
            "over_12_sell": self._predict(image, area_param.over_12_sell_area),
            "over_13_sell": self._predict(image, area_param.over_13_sell_area),
            "over_14_sell": self._predict(image, area_param.over_14_sell_area),
            "over_15_sell": self._predict(image, area_param.over_15_sell_area),
            "over_16_sell": self._predict(image, area_param.over_16_sell_area),

            "under_buy": self._predict(image, area_param.under_buy_area),
            "under_1_buy": self._predict(image, area_param.under_1_buy_area),
            "under_2_buy": self._predict(image, area_param.under_2_buy_area),
            "under_3_buy": self._predict(image, area_param.under_3_buy_area),
            "under_4_buy": self._predict(image, area_param.under_4_buy_area),
            "under_5_buy": self._predict(image, area_param.under_5_buy_area),
            "under_6_buy": self._predict(image, area_param.under_6_buy_area),
            "under_7_buy": self._predict(image, area_param.under_7_buy_area),
            "under_8_buy": self._predict(image, area_param.under_8_buy_area),
            "under_9_buy": self._predict(image, area_param.under_9_buy_area),
            "under_10_buy": self._predict(image, area_param.under_10_buy_area),
            "under_11_buy": self._predict(image, area_param.under_11_buy_area),
            "under_12_buy": self._predict(image, area_param.under_12_buy_area),
            "under_13_buy": self._predict(image, area_param.under_13_buy_area),
            "under_14_buy": self._predict(image, area_param.under_14_buy_area),
            "under_15_buy": self._predict(image, area_param.under_15_buy_area),
            "under_16_buy": self._predict(image, area_param.under_16_buy_area),

            "under_player": self._predict(image, area_param.under_player_area),
            "under_1_player": self._predict(image, area_param.under_1_player_area),
            "under_2_player": self._predict(image, area_param.under_2_player_area),
            "under_3_player": self._predict(image, area_param.under_3_player_area),
            "under_4_player": self._predict(image, area_param.under_4_player_area),
            "under_5_player": self._predict(image, area_param.under_5_player_area),
            "under_6_player": self._predict(image, area_param.under_6_player_area),
            "under_7_player": self._predict(image, area_param.under_7_player_area),
            "under_8_player": self._predict(image, area_param.under_8_player_area),
            "under_9_player": self._predict(image, area_param.under_9_player_area),
            "under_10_player": self._predict(image, area_param.under_10_player_area),
            "under_11_player": self._predict(image, area_param.under_11_player_area),
            "under_12_player": self._predict(image, area_param.under_12_player_area),
            "under_13_player": self._predict(image, area_param.under_13_player_area),
            "under_14_player": self._predict(image, area_param.under_14_player_area),
            "under_15_player": self._predict(image, area_param.under_15_player_area),
            "under_16_player": self._predict(image, area_param.under_16_player_area),

            "volume_sum": self._predict(image, area_param.volume_area)
        }
        return data
        #return over_value, under_value, upper_price_value, downer_price_value