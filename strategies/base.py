from abc import ABC, abstractmethod
import pandas as pd

class StrategyBase(ABC):
    def __init__(self, price_data: pd.DataFrame):
        # Ініціалізує базовий клас стратегії з даними цін.
        self.price_data = price_data

    @abstractmethod
    def generate_signals(self) -> pd.DataFrame:
        # Абстрактний метод для генерації сигналів купівлі/продажу (повинен бути реалізований у дочірніх класах).
        pass

    @abstractmethod
    def run_backtest(self) -> pd.DataFrame:
        # Абстрактний метод для запуску бектесту (повинен бути реалізований у дочірніх класах).
        pass

    @abstractmethod
    def get_metrics(self) -> dict:
        # Абстрактний метод для отримання метрик продуктивності (повинен бути реалізований у дочірніх класах).
        pass