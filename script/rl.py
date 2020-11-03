import json
import os
import numpy
import pandas
from PIL import Image
import datetime
import os

DIR_PATH = os.path.dirname(__file__)

import sys
sys.path.append("{}/daytra/script".format(DIR_PATH))
from trader import rl_trader

sys.path.append("{}/daytra/script/rlapi".format(DIR_PATH))
import rl_api_interface


class RLBotter(object):

    def __init__(self):
        # 1日前, 2日前のextractedのデータを読み込む
        filepath_list = sorted([f for f in os.listdir("daily_output") if "log_extracted" in f])
        last2 = filepath_list[-2:]
        y1 = pandas.read_csv("daily_output/{}".format(last2[0]))
        y2 = pandas.read_csv("daily_output/{}".format(last2[1]))
        self.y1 = y1
        self.y2 = y2
        
        self.status = "sell"
        self.buy_count = 0
        self.position = [0]

    def origin_to_processed(self, df):
        df2 = df.query(
            "over >= 50000 and over <= 2000000"
        ).query(
            "under >= 50000 and under <= 2000000"
        ).query(
            "upper_price >= 2500 and upper_price <= 10000"
        ).assign(
            over_under=lambda df: df["over"] / df["under"],
            hms=lambda df: df["time"].apply(lambda x: x[11:])
        ).query("'09-00-00' <= hms <= '11-30-00' or '12-30-00' <= hms").reset_index(drop=True)
        return df2

    def processed_to_extracted(self, df2, ymd):
        df3 = rl_api_interface.log_extract(df2, ymd)
        return df3
        
    def extracted_to_feature(self, df_extracted):
        df = pandas.concat([self.y2, self.y1, df_extracted], axis=0).reset_index(drop=True)
        df_feature = rl_api_interface.log_to_feature(df)
        return df_feature
            
    def feature_to_action(self, feature):
        # response_data: {'action': 'buy', 'q_value': 0, 'buy_tau': 0, 'sell_tau': -0.005}
        r = rl_api_interface.rl_predict(feature, self.position)
        if (self.status == "sell" and r["action"] == "buy" and r["q_value"] >= r["buy_tau"])\
        or (self.status == "buy" and r["q_value"] >= r["sell_tau"])\
        or 1 <= self.buy_count <= 5:
            self.status = "buy"
            self.position = [1]
            self.buy_count += 1
        else:
            self.status = "sell"
            self.position = [0]
            self.buy_count = 0
        return self.status
        

def get_trade_timing():
    hms = "09-00-00"
    timing = [hms]
    for i in range(72):
        next_hms = plus_second(hms, 300)
        if not "11-30-00" <= next_hms <= "12-30-00":
            timing.append(next_hms)
        hms = next_hms
    return timing
    
def plus_second(hms, n):
    # hms + n秒
    dt = datetime.datetime.strptime(hms, "%H-%M-%S")
    plus_dt = dt + datetime.timedelta(seconds=n)
    plus_hms = plus_dt.strftime("%H-%M-%S")
    return plus_hms
    
if __name__ == "__main__":
    timing = get_trade_timing()
    print(timing)
    rlbotter = RLBotter()