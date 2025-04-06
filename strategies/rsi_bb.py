import pandas as pd
import vectorbt as vbt
from .base import StrategyBase

class RSIBBStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, rsi_period=14, bb_period=20):
        # Ініціалізує стратегію RSI (14) із підтвердженням Bollinger Bands (20).
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_period = bb_period
        self.signals = None
        self.backtest_results = None

    def generate_signals(self) -> pd.DataFrame:
        # Генерує сигнали: купівля при RSI < 30 і ціні нижче нижньої BB, вихід при поверненні до середньої BB.
        rsi = vbt.RSI.run(self.price_data["close"], window=self.rsi_period)
        bb = vbt.BBANDS.run(self.price_data["close"], window=self.bb_period)
        entries = (rsi.rsi < 30) & (self.price_data["close"] < bb.lower)
        exits = self.price_data["close"] > bb.middle
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
            "total_return self.backtest_results.total_return(),
            "sharpe_ratio": self.backtest_results.sharpe_ratio(),
            "max_drawdown": self.backtest_results.max_drawdown()
        }