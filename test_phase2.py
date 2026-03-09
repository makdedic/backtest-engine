from data_fetcher import DataFetcher
from strategies import MovingAverageCrossover, MomentumStrategy

# Test DataFetcher
print("=== Testing DataFetcher ===")
fetcher = DataFetcher('SPY', '2023-01-01', '2024-01-01')
data = fetcher.fetch()
data = fetcher.validate()
print(f"Data shape: {data.shape}")
print(f"\nFirst few rows:\n{data.head()}")

# Test MovingAverageCrossover
print("\n=== Testing MovingAverageCrossover ===")
sma_strategy = MovingAverageCrossover(data, short_window=20, long_window=50)
sma_data = sma_strategy.generate_signals()
print(f"\nSignal column sample:\n{sma_data[['Close', 'SMA_short', 'SMA_long', 'Signal']].tail(10)}")

# Test MomentumStrategy
print("\n=== Testing MomentumStrategy ===")
momentum_strategy = MomentumStrategy(data, lookback_window=20)
momentum_data = momentum_strategy.generate_signals()
print(f"\nSignal column sample:\n{momentum_data[['Close', 'Momentum', 'Signal']].tail(10)}")

print("\n✅ Phase 2 tests passed!")