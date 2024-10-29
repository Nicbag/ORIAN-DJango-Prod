import os
import sys
import unittest
from typing import Any

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from orian_online_simulation.simulation import OnlineSimulation
from orian_online_simulation.market import Asset, Currency, StockMarketHandler
from orian_online_simulation.trading.algorithm import TrendAlgorithm
from orian_online_simulation.transaction import (
    Wallet,
    TransactionQuantityManagerByWalletPercentage,
    TransactionTriggerByRepeatedPredictions,
)
from orian_online_simulation.strategy import AutomatedStrategy


def _all_equal(iterator):
    """Check if all elements in an iterator are equal."""
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)


def _get_dummy_data(prices: list[float], start_date: str, periods: int) -> pd.DataFrame:
    """Generate a dummy dataframe with the given prices.

    Parameters
    ----------
    prices : list[float]
        A list of prices.
    start_date : str
        The start date of the dataframe.
    periods : int
        The number of periods in the dataframe.

    Returns
    -------
    pd.DataFrame
        A dataframe with the given prices
    """
    return pd.DataFrame(
        {
            "Open": prices,
            "High": prices,
            "Low": prices,
            "Close": prices,
            "Adj Close": prices,
            "Volume": prices,
        },
        index=pd.date_range(start=start_date, periods=periods),
    )


def _get_dummy_simulation_with_two_dummy_assets(
    dummy_df_1: pd.DataFrame, dummy_df_2: pd.DataFrame
) -> OnlineSimulation:
    # Create dummy assets and currency
    dummy_asset_1 = Asset("dummy_1")
    dummy_asset_2 = Asset("dummy_2")
    dummy_currency = Currency("dummy_currency")

    # Create dummy stock market handler
    dummy_stock_market_handler = StockMarketHandler(
        stock_market_dict={
            dummy_asset_1: dummy_df_1,
            dummy_asset_2: dummy_df_2,
        }
    )

    # Create dummy wallet
    dummy_wallet = Wallet(
        amounts={
            dummy_asset_1: 100,
            dummy_asset_2: 100,
            dummy_currency: 100,
        },
        base_currency=dummy_currency,
    )

    # Create dummy strategies for each asset
    dummy_strategy_1 = AutomatedStrategy(
        trading_algorithm=TrendAlgorithm(n=1),
        trading_asset=dummy_asset_1,
        priority=1,
        transaction_quantity_manager=TransactionQuantityManagerByWalletPercentage(
            wallet=dummy_wallet,
            percentage=0.05,
        ),
        transaction_trigger=TransactionTriggerByRepeatedPredictions(
            repetitions=2,
        ),
    )

    dummy_strategy_2 = AutomatedStrategy(
        trading_algorithm=TrendAlgorithm(n=1),
        trading_asset=dummy_asset_2,
        priority=1,
        transaction_quantity_manager=TransactionQuantityManagerByWalletPercentage(
            wallet=dummy_wallet,
            percentage=0.05,
        ),
        transaction_trigger=TransactionTriggerByRepeatedPredictions(
            repetitions=2,
        ),
    )

    # Create dummy simulation
    dummy_simulation = OnlineSimulation(
        strategies=[dummy_strategy_1, dummy_strategy_2],
        stock_market_handler=dummy_stock_market_handler,
        wallet=dummy_wallet,
    )
    return dummy_simulation


class TestSimulation(unittest.TestCase):
    def test_simulation_history_dates(self):
        """Test that the transaction dates in the simulation history are sorted \
            and in the stock market handler dates"""
        # Create dummy data
        dummy_df_1 = _get_dummy_data(
            prices=[i for i in range(10)],
            start_date="2020-01-01",
            periods=10,
        )
        dummy_df_2 = _get_dummy_data(
            prices=[i for i in range(10)],
            start_date="2020-01-06",
            periods=10,
        )

        # Create and run dummy simulation
        dummy_simulation = _get_dummy_simulation_with_two_dummy_assets(
            dummy_df_1, dummy_df_2
        )
        dummy_simulation.run_simulation()

        # Get the history dataframe and the dates
        history_df = dummy_simulation.simulation_history_dataframe
        dates = history_df.index.to_list()

        # Check that the dates are sorted
        self.assertEqual(dates, sorted(dates), "Transaction dates are not sorted")

        # Check that all dates are in the stock market handler dates
        self.assertTrue(
            all(date in dummy_simulation.stock_market_handler._dates for date in dates)
        )

    def test_simulation_history_total_net_value(self):
        """Test that the total net value in the simulation history is always the same"""
        # Create dummy data
        dummy_df_1 = _get_dummy_data(
            prices=[1 for i in range(10)],
            start_date="2020-01-01",
            periods=10,
        )
        dummy_df_2 = _get_dummy_data(
            prices=[1 for i in range(5)],
            start_date="2020-01-01",
            periods=5,
        )

        # Create and run dummy simulation
        dummy_simulation = _get_dummy_simulation_with_two_dummy_assets(
            dummy_df_1, dummy_df_2
        )
        dummy_simulation.run_simulation()

        # Get the history dataframe and total net value list
        history_df = dummy_simulation.simulation_history_dataframe
        total_net_value = history_df["total_net_value"].to_list()

        # Check that all total net values are non-negative
        self.assertTrue(
            all(net_value >= 0 for net_value in total_net_value),
            msg="Total net value is negative",
        )

        # Check that all total net values are equal
        self.assertTrue(_all_equal(total_net_value), msg="Total net value is not equal")


if __name__ == "__main__":
    unittest.main()
