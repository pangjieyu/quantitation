import sys
from binance.client import Client
import pandas as pd
from utils.binance_connector import BinanceConnector
from trading_strategy.strategy_moving_average import StrategyMovingAverage
from backtest.backtest_engine import BacktestEngine

def get_historical_data(binance_connector, symbol, interval, start_str, end_str=None):
    """
    Fetch historical klines data from Binance and prepare it for backtesting.
    """
    klines = binance_connector.get_historical_klines(symbol, interval, start_str, end_str)
    # Convert to DataFrame and prepare data
    columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df.set_index('open_time', inplace=True)
    df['close'] = df['close'].astype(float)
    return df[['close']]

def prepare_historical_data(historical_klines):
    """
    Convert historical kline data fetched from Binance into a pandas DataFrame.
    
    :param historical_klines: The list of klines (candlesticks) returned from the Binance API.
    :return: pandas DataFrame with formatted historical data.
    """
    # Define column names for the DataFrame
    columns = [
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ]
    
    # Convert the list of klines to a DataFrame
    df = pd.DataFrame(historical_klines, columns=columns)
    
    # Convert timestamp to datetime and set as index
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df.set_index('open_time', inplace=True)
    
    # Convert columns to the appropriate data types
    numeric_columns = ['open', 'high', 'low', 'close', 'volume',
                       'quote_asset_volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, axis=1)
    
    # Here we return only the 'close' column for simplicity, but you can adjust this to your needs
    return df[['close']]

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py backtest")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "backtest":
        # Setup your Binance API key and secret
        api_key = "T5W5jrmwDqEiHHeMH7LgQDFjm4xPLekKzDuj8jrAHvRyvYu4iBaZNODsIvLzZF3c"
        api_secret = "EeNeRCBCiacM4UQ865uwUBOs6zYrFVz3UKg8oEIR8KxrKgNm10kOdSWaIENDXAJz"

        # 初始化BinanceConnector
        connector = BinanceConnector(api_key, api_secret)
        
        # 获取历史数据
        historical_data = connector.get_historical_klines("BTCUSDT", "1 Jan, 2020", "1 Jan, 2021")
        
        # 转换数据为DataFrame
        data = prepare_historical_data(historical_data)
        
        # 初始化策略
        strategy = StrategyMovingAverage(data)
        
        # 初始化并运行回测引擎
        backtest_engine = BacktestEngine(strategy, data)
        backtest_engine.run()
        
        # 输出回测结果
        print(backtest_engine.calculate_performance_metrics())
        backtest_engine.plot_equity_curve()
    else:
        print("Invalid mode. Please choose 'backtest'.")

if __name__ == "__main__":
    main()
