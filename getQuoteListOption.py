import time
import os
import requests
import pandas as pd
from datetime import datetime, timedelta


def func():
    arg1 = "TXFE5-M"
    res = requests.post("https://mis.taifex.com.tw/futures/api/getQuoteDetail",
                        json={"SymbolID": ["TXF-S", arg1, "TXO-R"]}).json()["RtData"]['QuoteList'][1]
    # qr_time = datetime.strptime(res["CTime"], '%H%M%S').strftime('%H:%M:%S')
    last_close = float(res['CLastPrice'])

    close_to_strike = int(last_close / 50) * 50
    strike_range = [str(close_to_strike + i * 50) for i in range(-2, 3)]
    arg2 = "202505W1"
    quote_table = requests.post("https://mis.taifex.com.tw/futures/api/getQuoteListOption",
                                json={"MarketType": "1", "SymbolType": "O", "KindID": "1", "CID": "TXO",
                                      "ExpireMonth": arg2, "RowSize": "全部", "PageNo": "", "SortColumn": "", "AscDesc": "A"},
                                ).json()["RtData"]['QuoteList']
    data = [
        {item['DispEName'][9:15]: (float(item['CBestAskPrice']) + float(item['CBestBidPrice'])) / 2} for item in quote_table
        if item['DispEName'][9:14] in strike_range
        and ((float(item['CBestAskPrice']) + float(item['CBestBidPrice'])) / 2 > 76)
    ]

    StrikeCall = [item for item in data if list(item.keys())[0].endswith('C')]
    StrikeCall_ = sorted(
        StrikeCall, key=lambda x: list(x.keys())[0], reverse=True)
    StrikePut = [item for item in data if list(item.keys())[0].endswith('P')]
    StrikePut_ = sorted(StrikePut, key=lambda x: list(
        x.keys())[0], reverse=True)
    return StrikeCall_, StrikePut_


def main():
    result = func()
    print(result)


if __name__ == "__main__":
    main()
