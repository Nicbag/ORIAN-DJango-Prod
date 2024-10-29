from abc import ABC, abstractmethod

import pandas as pd

from orian_online_simulation.trading.prediction import PredictionEnum


class TradingAlgorithm(ABC):
    def __init__(self):
        self.name = "TradingAlgorithm"

    @abstractmethod
    def make_prediction(self, stock_market_data: pd.DataFrame) -> PredictionEnum:
        pass


class TrendAlgorithm(TradingAlgorithm):
    """
    A trading algorithm that predicts the trend of a stock based on the recent closing prices.
    Args:
        n (int): The number of recent closing prices to consider for prediction.
    Methods:
        make_prediction(stock_market_data: pd.DataFrame) -> PredictionEnum:
            Makes a prediction on the trend of a stock based on the given stock market data.
    """

    def __init__(self, n: int):
        self.n = n
        self.name = f"TrendAlgorithm({n})"

    def make_prediction(self, stock_market_data: pd.DataFrame) -> PredictionEnum:
        """
        Makes a prediction on the trend of a stock based on the given stock market data.
        Args:
            stock_market_data (pd.DataFrame): The stock market data containing the closing prices.
        Returns:
            PredictionEnum: The predicted trend of the stock (INCREASE, DECREASE, or STABLE).
        """
        if len(stock_market_data) < self.n:
            return PredictionEnum.UNKNOWN

        prices = stock_market_data["Close"].iloc[-self.n :]

        if all(prices.iloc[i] < prices.iloc[i + 1] for i in range(self.n - 1)):
            return PredictionEnum.INCREASE
        elif all(prices.iloc[i] > prices.iloc[i + 1] for i in range(self.n - 1)):
            return PredictionEnum.DECREASE
        else:
            return PredictionEnum.STABLE
