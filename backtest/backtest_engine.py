from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

class BacktestEngine:
    def __init__(self, strategy, data, initial_capital=10000, transaction_cost=0.001, slippage=0.0002):
        """
        Backtest Engine for running trading strategies.

        :param strategy: An instance of a trading strategy.
        :param data: Historical market data (Pandas DataFrame).
        """
        self.strategy = strategy
        self.data = data
        self.results = None
        self.transaction_cost = transaction_cost  # 交易成本（手续费比例）
        self.slippage = slippage  # 滑点（价格变动比例）


    def run(self):
        """
        Executes the backtest of the provided trading strategy.
        """
        self.strategy.data = self.data
        self.strategy.generate_signals()
        
        # Assume we start with $10,000 and invest the entire amount in every trade
        initial_capital = 10000
        positions = self.strategy.data['signal'].diff()
        
        # Create a portfolio DataFrame
        portfolio = pd.DataFrame(index=self.strategy.data.index)
        portfolio['positions'] = positions
        portfolio['prices'] = self.data['close']
        portfolio['cash'] = initial_capital - (positions * portfolio['prices']).cumsum()
        portfolio['total'] = portfolio['cash'] + positions.cumsum() * portfolio['prices']
        portfolio['returns'] = portfolio['total'].pct_change()

        self.results = portfolio

    def get_results(self):
        """
        Returns the backtest results.
        """
        return self.results

    def get_performance_metrics(self):
        """
        Calculate and return key performance metrics.
        """
        if self.results is None:
            return None

        total_return = self.results['total'][-1] / self.results['total'][0] - 1
        daily_returns = self.results['returns']
        annualized_return = daily_returns.mean() * 252
        annualized_volatility = daily_returns.std() * np.sqrt(252)
        sharpe_ratio = annualized_return / annualized_volatility

        return {
            'Total Return': total_return,
            'Annualized Return': annualized_return,
            'Annualized Volatility': annualized_volatility,
            'Sharpe Ratio': sharpe_ratio
        }


    def adjust_for_slippage_and_transaction_cost(price, quantity, is_buy, transaction_cost, slippage):
        """
        Adjust the price for slippage and add transaction cost.

        :param price: Original price of the asset.
        :param quantity: Quantity of the asset being traded.
        :param is_buy: True if buy order, False if sell order.
        :param transaction_cost: The cost of making a trade (as a percentage).
        :param slippage: The slippage in price (as a percentage).
        :return: The adjusted price and the total cost of the trade.
        """
        slippage_adjustment = price * slippage
        adjusted_price = price + slippage_adjustment if is_buy else price - slippage_adjustment
        cost = adjusted_price * quantity * transaction_cost
        return adjusted_price, cost


    def calculate_trade_size(account_value, risk_factor):
        """
        Calculate the size of the trade based on the current account value and risk factor.

        :param account_value: Current value of the account.
        :param risk_factor: The risk factor to determine trade size (e.g., 0.02 for 2% of account value).
        :return: The size of the trade.
        """
        return account_value * risk_factor

    def apply_stop_loss_and_take_profit(signals, stop_loss_percentage, take_profit_percentage):
        """
        Adjust trading signals to include stop loss and take profit logic.

        :param signals: DataFrame of trading signals.
        :param stop_loss_percentage: The stop loss percentage.
        :param take_profit_percentage: The take profit percentage.
        """
        # Add columns for stop loss and take profit levels
        signals['stop_loss'] = signals['entry_price'] * (1 - stop_loss_percentage)
        signals['take_profit'] = signals['entry_price'] * (1 + take_profit_percentage)

    def calculate_performance_metrics(portfolio):
        """
        Calculate key performance metrics for the portfolio.

        :param portfolio: DataFrame of the portfolio's performance.
        :return: A dictionary of performance metrics.
        """
        total_return = (portfolio['total'][-1] - portfolio['total'][0]) / portfolio['total'][0]
        sharpe_ratio = portfolio['returns'].mean() / portfolio['returns'].std() * np.sqrt(252)
        # Calculate more metrics as needed
        return {'total_return': total_return, 'sharpe_ratio': sharpe_ratio}

    def plot_equity_curve(portfolio):
        """
        Plot the equity curve of the portfolio.
        
        :param portfolio: DataFrame of the portfolio's performance.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(portfolio.index, portfolio['total'], label='Equity Curve')
        plt.title('Equity Curve')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.legend()
        plt.show()