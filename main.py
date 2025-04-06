from core.data_loader import DataLoader
from core.backtester import Backtester
from strategies.sma_cross import SMACrossStrategy
from strategies.rsi_bb import RSIBBStrategy
from strategies.vwap_reversion import VWAPReversionStrategy

def main():
    # Основна функція: завантажує дані, створює стратегії та запускає бектест.
    loader = DataLoader()
    data = loader.load_data(symbol="BTCUSDT")
    strategies = [
        SMACrossStrategy(data),
        RSIBBStrategy(data),
        VWAPReversionStrategy(data)
    ]
    backtester = Backtester(strategies)
    results = backtester.run()
    print("Результаты бэктеста:")
    print(results)

if __name__ == "__main__":
    # Запускає main(), якщо файл виконаний напряму.
    main()