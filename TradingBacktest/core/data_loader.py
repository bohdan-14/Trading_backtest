import pandas as pd
import pyarrow.parquet as pq
import os
import ccxt
from datetime import datetime

class DataLoader:
    def __init__(self, data_dir="data"):
        # Ініціалізує об'єкт для завантаження даних, створює папку для кешу та підключається до Binance.
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.exchange = ccxt.binance()

    def load_data(self, symbol="BTCUSDT", start_date="2024-02-01", end_date="2024-02-28"):
        # Завантажує 1-хвилинні OHLCV дані з Binance або кешу, зберігає у форматі Parquet і повертає DataFrame.
        file_path = os.path.join(self.data_dir, f"{symbol}_1m_feb24.parquet")
        if os.path.exists(file_path):
            print(f"Завантажуємо дані з кешу для {symbol}...")
            return pq.read_table(file_path).to_pandas()
        print(f"Завантажуємо дані для {symbol} з Binance...")
        start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
        end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe="1m", since=start_ts, limit=None)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["symbol"] = symbol
        df.to_parquet(file_path, compression="snappy")
        return df

if __name__ == "__main__":
    # Тестовий блок: створює об'єкт DataLoader і виводить перші рядки завантажених даних.
    loader = DataLoader()
    df = loader.load_data()
    print(df.head())