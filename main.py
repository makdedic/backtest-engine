"""
Backtesting Engine - Main Entry Point

This script runs a complete backtest of trading strategies on historical market data,
calculates performance metrics, and generates visualizations.
"""

from data_fetcher import DataFetcher
from strategies import MovingAverageCrossover, MomentumStrategy
from backtester import Backtester
from visualiser import Visualiser

def run_backtest(ticker='SPY', start_date='2023-01-01', end_date='2024-01-01', initial_capital=100000):
    """
    Run a complete backtest for multiple strategies
    
    Args:
        ticker (str): Stock ticker to backtest
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        initial_capital (float): Starting capital in dollars
    """
    
    # Fetch historical data
    print(f"\n{'='*60}")
    print(f"Backtesting {ticker} from {start_date} to {end_date}")
    print(f"{'='*60}\n")
    
    fetcher = DataFetcher(ticker, start_date, end_date)
    data = fetcher.fetch()
    data = fetcher.validate()
    
    # Strategy 1: SMA Crossover
    print("\n" + "="*60)
    print("STRATEGY 1: Simple Moving Average Crossover (20, 50)")
    print("="*60)
    
    sma_strategy = MovingAverageCrossover(data, short_window=20, long_window=50)
    backtester_sma = Backtester(data, sma_strategy, initial_capital=initial_capital)
    results_sma = backtester_sma.run()
    metrics_sma = backtester_sma.calculate_metrics()
    backtester_sma.print_metrics()
    
    visualiser_sma = Visualiser(results_sma, strategy_name="SMA Crossover (20, 50)")
    visualiser_sma.plot_performance(save_path='sma_performance.png')
    visualiser_sma.plot_signals(save_path='sma_signals.png')
    visualiser_sma.plot_rolling_metrics(save_path='sma_rolling_metrics.png')
    
    # Strategy 2: Momentum
    print("\n" + "="*60)
    print("STRATEGY 2: Momentum Strategy (20-day)")
    print("="*60)
    
    momentum_strategy = MomentumStrategy(data, lookback_window=20)
    backtester_momentum = Backtester(data, momentum_strategy, initial_capital=initial_capital)
    results_momentum = backtester_momentum.run()
    metrics_momentum = backtester_momentum.calculate_metrics()
    backtester_momentum.print_metrics()
    
    visualiser_momentum = Visualiser(results_momentum, strategy_name="Momentum (20-day)")
    visualiser_momentum.plot_performance(save_path='momentum_performance.png')
    visualiser_momentum.plot_signals(save_path='momentum_signals.png')
    visualiser_momentum.plot_rolling_metrics(save_path='momentum_rolling_metrics.png')
    
    # Summary comparison
    print("\n" + "="*60)
    print("STRATEGY COMPARISON")
    print("="*60)
    print(f"\n{'Metric':<25} {'SMA':<15} {'Momentum':<15}")
    print("-"*55)
    for metric_key in metrics_sma.keys():
        sma_val = metrics_sma[metric_key]
        mom_val = metrics_momentum[metric_key]
        if isinstance(sma_val, float):
            print(f"{metric_key:<25} {sma_val:>14.2%} {mom_val:>14.2%}")
        else:
            print(f"{metric_key:<25} {sma_val:>14} {mom_val:>14}")
    print("="*60 + "\n")
    
    print("✅ Backtest completed successfully!")
    print("📊 Charts saved:")
    print("   - sma_performance.png")
    print("   - sma_signals.png")
    print("   - sma_rolling_metrics.png")
    print("   - momentum_performance.png")
    print("   - momentum_signals.png")
    print("   - momentum_rolling_metrics.png\n")

if __name__ == "__main__":
    # Run backtest with default parameters
    run_backtest()
    
    # Optional: Test with different parameters
    # run_backtest(ticker='AAPL', start_date='2022-01-01', end_date='2024-01-01')