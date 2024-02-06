
class StrategyBase:
    def __init__(self):
        pass

    def initialize(self, context):
        """
        初始化策略，在策略启动时调用一次
        :param context: 传递市场数据、交易函数等
        """
        raise NotImplementedError("Should implement initialize method")

    def handle_data(self, context, data):
        """
        核心交易逻辑，每个交易周期调用一次
        :param context: 传递市场数据、交易函数等
        :param data: 当前交易周期的数据
        """
        raise NotImplementedError("Should implement handle_data method")

    def before_trading_start(self, context):
        """
        每日交易开始前调用一次
        :param context: 传递市场数据、交易函数等
        """
        pass

    def analyze(self, context, perf):
        """
        策略结束后的分析函数
        :param context: 传递市场数据、交易函数等
        :param perf: 策略的性能数据
        """
        pass
