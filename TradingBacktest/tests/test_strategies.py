import unittest
import pandas as pd
import numpy as np
from TradingBacktest.strategies.sma_cross import SMACrossStrategy
from TradingBacktest.strategies.rsi_bb import RSIBBStrategy
from TradingBacktest.strategies.vwap_reversion import VWAPReversionStrategy

class TestStrategies(unittest.TestCase):
    def setUp(self):
        # Створює тестові дані: 100 хвилин із випадковими цінами та обсягами.
        dates = pd.date_range("2024-02-01", periods=100, freq="1min")
        self.data = pd.DataFrame({
            "open": np.random.uniform(50000, 60000, 100),
            "high": np.random.uniform(50000, 60000, 100),
            "low": np.random.uniform(50000, 60000, 100),
            "close": np.random.uniform(50000, 60000, 100),
            "volume": np.random.uniform(0, 100, 100)
        }, index=dates)

    def test_sma_cross(self):
        # Перевіряє, чи стратегія SMA генерує коректні сигнали (наявність колонки "entries").
        strategy = SMACrossStrategy(self.data)
        signals = strategy.generate_signals()
        self.assertIsInstance(signals, pd.DataFrame)
        self.assertTrue("entries" in signals.columns)

    def test_rsi_bb(self):
        # Перевіряє, чи стратегія RSI BB генерує коректні сигнали (наявність колонки "exits").
        strategy = RSIBBStrategy(self.data)
        signals = strategy.generate_signals()
        self.assertIsInstance(signals, pd.DataFrame)
        self.assertTrue("exits" in signals.columns)

    def test_vwap_reversion(self):
        # Перевіряє, чи стратегія VWAP генерує коректні сигнали (наявність колонки "entries").
        strategy = VWAPReversionStrategy(self.data)
        signals = strategy.generate_signals()
        self.assertIsInstance(signals, pd.DataFrame)
        self.assertTrue("entries" in signals.columns)

if __name__ == "__main__":
    # Запускає тести, якщо файл виконаний напряму.
    unittest.main()