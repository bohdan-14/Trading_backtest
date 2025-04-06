import pandas as pd
import vectorbt as vbt
from .base import StrategyBase

class SMACrossStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, fast_period=10, slow_period=30):
        # Ініціалізує стратегію перетину SMA з швидким (10) і повільним (30) періодами.
        super().__init__(price_data)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signals = None
        self.backtest_results = None

    def generate_signals(self) -> pd.DataFrame:
        # Генерує сигнали купівлі (швидка SMA перетинає повільну вгору) і продажу (навпаки).
        fast_sma = vbt.MA.run(self.price_data["close"], window=self.fast_period)
        slow_sma = vbt.MA.run(self.price_data["close"], window=self.slow_period)
        entries = fast_sma.ma_crossed_above(slow_sma)
        exits = fast_sma.ma_crossed_below(slow_sma)
        self.signals = pd.DataFrame({"entries": entries, "exits": exits})
        return self.signals

    def run_backtest(self) -> pd.DataFrame:
        # Запускає бектест на основі сигналів із урахуванням комісій і прослизання.
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
        # Повертає основні метрики: загальну дохідність, коефіцієнт Шарпа та максимальну просадку.
        if self.backtest_results is None:
            self.run_backtest()
        return {
            "total_return": self.backtest_results.total_return(),
            "sharpe_ratio": self.backtest_results.sharpe_ratio(),
            "max_drawdown": self.backtest_results.max_drawdown()
        }