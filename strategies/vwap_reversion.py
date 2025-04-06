import pandas as pd
import vectorbt as vbt
from .base import StrategyBase

class VWAPReversionStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame):
        # Ініціалізує стратегію повернення до VWAP без додаткових параметрів.
        super().__init__(price_data)
        self.signals = None
        self.backtest_results = None

    def generate_signals(self) -> pd.DataFrame:
        # Генерує сигнали: купівля при відхиленні вниз на 1% від VWAP, вихід при поверненні до VWAP.
        vwap = vbt.VWAP.run(self.price_data["high"], self.price_data["low"],
                           self.price_data["close"], self.price_data["volume"])
        entries = self.price_data["close"] < (vwap.vwap * 0.99)
        exits = self.price_data["close"] >= vwap.vwap
        self.signals = pd.DataFrame({"entries": entries, "exits": exits})
        return self.signals

    def run_backtest(self) -> pd.DataFrame:
        # Запускає бектест із сигналами, враховуючи комісії та прослизання.
        if self.signals is None:
            self.generate_signals()
        pf = vbt.Portfolio.from_signals(
            close=self.price_data["close"],
            entries=self.signals["entries"],
            exits=self.signals["exits"],
            fees=0.001,
            slippage=0.001
        )
        self.backtest_results = pf
        return pf.stats()

    def get_metrics(self) -> dict:
        # Повертає метрики: дохідність, Шарп, максимальна просадка.
        if self.backtest_results is None:
            self.run_backtest()
        return {
            "total_return": self.backtest_results.total_return(),
            "sharpe_ratio": self.backtest_results.sharpe_ratio(),
            "max_drawdown": self.backtest_results.max_drawdown()
        }