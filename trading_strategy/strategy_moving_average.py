from strategy_base import StrategyBase
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class StrategyMovingAverage(StrategyBase):
    def __init__(self, binance_connector, symbol, quantity):
        super().__init__()
        self.binance_connector = binance_connector
        self.symbol = symbol
        self.quantity = quantity
    
    def analyze_market_data(self):
        """
        分析市场数据
        """
        # 获取最近一小时的平均价格
        average_price_last_hour = self.binance_connector.get_last_hour_average_price(self.symbol)
        # 获取最近一分钟的市场数据
        recent_market_data = self.binance_connector.get_recent_market_data(self.symbol)
        if not recent_market_data:
            print("Failed to fetch recent market data.")
            return None
        current_price = float(recent_market_data['close'])

        print(f"Current Price: {current_price}, Last Hour Average Price: {average_price_last_hour}")
        
        if current_price > average_price_last_hour:
            return 'buy'
        elif current_price < average_price_last_hour:
            return 'sell'
        else:
            return 'hold'

    def execute_trade(self, decision):
        if decision == 'buy':
            print("Executing buy order")
            # 这里演示代码，实际应用中需要处理order_market_buy的返回值和可能的异常
            self.binance_connector.client.order_market_buy(symbol=self.symbol, quantity=self.quantity)
        elif decision == 'sell':
            print("Executing sell order")
            # 这里演示代码，实际应用中需要处理order_market_sell的返回值和可能的异常
            self.binance_connector.client.order_market_sell(symbol=self.symbol, quantity=self.quantity)
        else:
            print("Holding position")

    def run(self):
        decision = self.analyze_market_data()
        if decision:
            self.execute_trade(decision)
    