from binance.client import Client
from datetime import datetime
import dateutil.parser
from binance.exceptions import BinanceAPIException
import pandas as pd


class BinanceConnector:
    def __init__(self, api_key, api_secret, testnet = False):
        self.client = Client(api_key, api_secret, testnet = testnet)

    def get_market_data(self, symbol, interval, limit=500):
        """
        Get historical candlestick data for a symbol.

        :param symbol: Symbol for the market (e.g., 'BTCUSDT').
        :param interval: Chart interval (e.g., Client.KLINE_INTERVAL_1MINUTE).
        :param limit: Number of data points to fetch.
        """
        try:
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            return klines
        except BinanceAPIException as e:
            print(f"An exception occurred while fetching market data: {e}")
            return None

    def create_order(self, symbol, order_type, side, quantity, price=None):
        """
        Create an order.

        :param symbol: The symbol to trade (e.g., 'BTCUSDT').
        :param order_type: The type of the order ('LIMIT' or 'MARKET').
        :param side: The side of the order ('BUY' or 'SELL').
        :param quantity: The quantity to order.
        :param price: The price at which to place a limit order.
        """
        try:
            if order_type == 'MARKET':
                order = self.client.order_market_buy(symbol=symbol, quantity=quantity) if side == 'BUY' else self.client.order_market_sell(symbol=symbol, quantity=quantity)
            elif order_type == 'LIMIT' and price is not None:
                order = self.client.order_limit_buy(symbol=symbol, quantity=quantity, price=price) if side == 'BUY' else self.client.order_limit_sell(symbol=symbol, quantity=quantity, price=price)
            else:
                raise ValueError("Invalid order type or missing price for limit order.")
            return order
        except BinanceAPIException as e:
            print(f"An exception occurred while creating an order: {e}")
            return None

    def cancel_order(self, symbol, order_id):
        """
        Cancel an order.

        :param symbol: The symbol of the order to cancel.
        :param order_id: The ID of the order to cancel.
        """
        try:
            result = self.client.cancel_order(symbol=symbol, orderId=order_id)
            return result
        except BinanceAPIException as e:
            print(f"An exception occurred while canceling an order: {e}")
            return None

    def get_account_info(self):
        """
        Get account information.
        """
        try:
            account_info = self.client.get_account()
            return account_info
        except BinanceAPIException as e:
            print(f"An exception occurred while fetching account information: {e}")
            return None

    
    def get_historical_klines(self, symbol, interval, start_str, end_str=None):
        """
        Get historical klines from Binance.

        :param symbol: The symbol to fetch data for (e.g., 'BTCUSDT').
        :param interval: Binance Kline intervals (e.g., Client.KLINE_INTERVAL_1DAY).
        :param start_str: Start time string in UTC format.
        :param end_str: Optional - end time string in UTC format.
        """
        klines = self.client.get_historical_klines(symbol, interval, start_str, end_str=end_str)
        return klines    
