# In trading_strategy/strategy_moving_average.py
import numpy as np
import pandas as pd
from trading_strategy.strategy_base import StrategyBase
from utils.binance_connector import BinanceConnector

class StrategyMovingAverage(StrategyBase):
    def __init__(self, data, short_window=5, long_window=20):
        """
        Moving Average Strategy.

        :param data: Initial market data as a DataFrame.
        :param short_window: Window size for the short moving average.
        :param long_window: Window size for the long moving average.
        """
        super().__init__(data, {})
        self.binance_connector = BinanceConnector
        self.short_window = short_window
        self.long_window = long_window
        self.data['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1).mean()
        self.data['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1).mean()
        self.data['signal'] = 0  # Default to no position
        self.generate_signals()

    def generate_signals(self):
        """
        Generate signals based on moving average crossovers.
        """
        self.data['signal'][self.short_window:] = np.where(self.data['short_mavg'][self.short_window:] > self.data['long_mavg'][self.short_window:], 1.0, 0.0)

        # Taking the diff to identify changes in the signal
        self.data['positions'] = self.data['signal'].diff()

    def calculate_signals(self):
        return self.data[self.data['positions'] != 0]

    def execute_trade(self, signal):
        """
        Execute a trade based on the signal.

        :param signal: The trading signal to act upon.
        """
        if signal["positions"] == 1.0:
            # This indicates a buy signal
            self.binance_connector.create_order(symbol='YOUR_SYMBOL', order_type='MARKET', side='BUY', quantity='YOUR_QUANTITY')
        elif signal['positions'] == -1.0:
            # This indicates a sell signal
            self.binance_connector.create_order(symbol='YOUR_SYMBOL', order_type='MARKET', side='SELL', quantity='YOUR_QUANTITY')

        print(f"Executing trade for signal: {signal}")
