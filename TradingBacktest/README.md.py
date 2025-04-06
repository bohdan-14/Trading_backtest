# Trading Backtest Project

## Опис
Проєкт реалізує систему бектестингу торгових стратегій на 1-хвилинних OHLCV даних з використанням VectorBT.

## Встановлення
1. Клонуйте репозиторій: `https://github.com/bohdan-14/trading-backtest`
2. Встановіть залежності: `pip install -r requirements.txt`
3. Запустіть: `python main.py`

## Стратегії
1. **SMA Crossover**: Перетин швидкої (10 хв) і повільної (30 хв) ковзних середніх.
2. **RSI with Bollinger Bands**: Вхід при RSI < 30 і підтвердженні від нижньої смуги BB.
3. **VWAP Reversion**: Купівля при відхиленні від VWAP на 1% з виходом при поверненні.

## Результати
- Дані: `data/BTCUSDT_1m_feb25.parquet`
- Метрики: `results/metrics.csv`
- Графіки: `results/screenshots/`

## Висновки
- SMA Crossover показала стабільні результати з помірною дохідністю.
- RSI BB більш консервативна, але з меншим ризиком.
- VWAP Reversion чутлива до волатильності.

## Тестування
Запустіть тести: `python -m unittest discover tests`