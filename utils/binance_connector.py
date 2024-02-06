from binance.client import Client
from datetime import datetime
import dateutil.parser

class BinanceConnector:
    def __init__(self, api_key, api_secret, testnet = False):
        self.client = Client(api_key, api_secret, testnet = testnet)

    def get_histotical_klines(self, symbol, interval, start_str, end_str = None):
        """
        获取历史数据
        :param symbol: 交易对，如 'BTCUSDT'
        :param interval: 时间间隔，如 '1h'，'1d'
        :param start_str: 开始时间
        :param end_str: 结束时间，可选
        :return: 历史数据列表
        """
        klines = self.client.get_historical_klines(symbol, interval, start_str, end_str)
        #解析数据
        parsed_data = []
        for kline in klines:
            parsed_data.append({
                "timestamp": kline[0],
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5]),
                "close_time": kline[6]
            })
        return parsed_data

    def get_recent_market_data(self, symbol):
        # 获取最近的市场数据，这里以获取最近一分钟的数据为例
        candles = self.client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=1)
        if candles:
            latest_candle = candles[-1]  # 获取最新的K线数据
            market_data = {
                'open_time': dateutil.parser.parse(datetime.utcfromtimestamp(latest_candle[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')),
                'open': latest_candle[1],
                'high': latest_candle[2],
                'low': latest_candle[3],
                'close': latest_candle[4],
                'volume': latest_candle[5],
                'close_time': dateutil.parser.parse(datetime.utcfromtimestamp(latest_candle[6] / 1000).strftime('%Y-%m-%d %H:%M:%S')),
            }
            return market_data
        return None

    def get_last_hour_average_price(self, symbol):
        # 获取过去一小时的平均价格
        candles = self.client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=60)
        average_price = sum(float(candle[4]) for candle in candles) / len(candles)
        return average_price