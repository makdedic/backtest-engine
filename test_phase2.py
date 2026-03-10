from data_fetcher import DataFetcher
from strategies import MovingAverageCrossover, MomentumStrategy
from backtester import Backtester
from visualiser import Visualiser

# Fetch data
print("=== Fetching Data ===")
fetcher = DataFetcher('SPY', '2023-01-01', '2024-01-01')
data = fetcher.fetch()
data = fetcher.validate()
print(f"Data shape: {data.shape}\n")

# Test MovingAverageCrossover with Backtester
print("=== Testing SMA Crossover Strategy ===")
sma_strategy = MovingAverageCrossover(data, short_window=20, long_window=50)
backtester_sma = Backtester(data, sma_strategy, initial_capital=100000)
results_sma = backtester_sma.run()
metrics_sma = backtester_sma.calculate_metrics()
backtester_sma.print_metrics()

# Visualize SMA results
print("Generating visualizations for SMA strategy...")
visualizer_sma = Visualiser(results_sma, strategy_name="SMA Crossover (20, 50)")
visualizer_sma.plot_performance(save_path='sma_performance.png')
visualizer_sma.plot_signals(save_path='sma_signals.png')
visualizer_sma.plot_rolling_metrics(save_path='sma_rolling_metrics.png')

# Test MomentumStrategy with Backtester
print("\n=== Testing Momentum Strategy ===")
momentum_strategy = MomentumStrategy(data, lookback_window=20)
backtester_momentum = Backtester(data, momentum_strategy, initial_capital=100000)
results_momentum = backtester_momentum.run()
metrics_momentum = backtester_momentum.calculate_metrics()
backtester_momentum.print_metrics()

# Visualize Momentum results
print("Generating visualizations for Momentum strategy...")
visualiser_momentum = Visualiser(results_momentum, strategy_name="Momentum (20-day)")
visualiser_momentum.plot_performance(save_path='momentum_performance.png')
visualiser_momentum.plot_signals(save_path='momentum_signals.png')
visualiser_momentum.plot_rolling_metrics(save_path='momentum_rolling_metrics.png')

print("\n✅ Phase 3 tests and visualizations completed!")