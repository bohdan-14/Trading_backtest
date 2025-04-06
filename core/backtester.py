import pandas as pd
import vectorbt as vbt
import plotly.graph_objects as go
import os

class Backtester:
    def __init__(self, strategies, output_dir="results"):
        # Ініціалізує бектестер зі списком стратегій і створює папку для результатів.
        self.strategies = strategies
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if not os.path.exists(os.path.join(output_dir, "screenshots")):
            os.makedirs(os.path.join(output_dir, "screenshots"))

    def run(self):
        # Запускає бектест для кожної стратегії, зберігає метрики в CSV і графіки equity curve у PNG.
        all_metrics = []
        for strategy in self.strategies:
            print(f"Запускаем бэктест для {strategy.__class__.__name__}...")
            results = strategy.run_backtest()
            metrics = strategy.get_metrics()
            metrics["strategy"] = strategy.__class__.__name__
            all_metrics.append(metrics)
            equity = strategy.backtest_results.total_profit()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=equity.index, y=equity, mode="lines",
                                   name=f"{strategy.__class__.__name__} Equity"))
            fig.update_layout(title=f"{strategy.__class__.__name__} Equity Curve",
                            xaxis_title="Время", yaxis_title="Значение")
            fig.write_image(os.path.join(self.output_dir, "screenshots",
                                        f"{strategy.__class__.__name__}_equity.png"))
        metrics_df = pd.DataFrame(all_metrics)
        metrics_df.to_csv(os.path.join(self.output_dir, "metrics.csv"), index=False)
        return metrics_df

if __name__ == "__main__":
    # Тестовий блок: завантажує дані, створює стратегії та запускає бектест.
    from core.data_loader import DataLoader
    from strategies.sma_cross import SMACrossStrategy
    from strategies.rsi_bb import RSIBBStrategy
    from strategies.vwap_reversion import VWAPReversionStrategy
    loader = DataLoader()
    data = loader.load_data()
    strategies = [SMACrossStrategy(data), RSIBBStrategy(data), VWAPReversionStrategy(data)]
    backtester = Backtester(strategies)
    results = backtester.run()
    print(results)