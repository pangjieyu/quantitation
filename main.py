from cgi import test
import socket
from utils.binance_connector import BinanceConnector
import socket
from utils.ip_utils import get_public_ip

if __name__ == '__main__':
    print("Welcome to the Quantitative Trading System!")
    print("This is the main file of the system.")
    api_key = 'T5W5jrmwDqEiHHeMH7LgQDFjm4xPLekKzDuj8jrAHvRyvYu4iBaZNODsIvLzZF3c'
    api_secret = 'EeNeRCBCiacM4UQ865uwUBOs6zYrFVz3UKg8oEIR8KxrKgNm10kOdSWaIENDXAJz'

    # Call the function to get the public IP address
    public_ip = get_public_ip()
    print("Public IP Address:", public_ip)

    # 创建BinanceConnector对象
    connector = BinanceConnector(api_key, api_secret, testnet=True)

    # 测试获取最近的市场数据
    recent_data = connector.get_recent_market_data('BTCUSDT')
    print("Recent Market Data:", recent_data)

    # 测试计算过去一小时的平均价格
    average_price = connector.get_last_hour_average_price('BTCUSDT')
    print("Last Hour Average Price:", average_price)

    