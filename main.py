"""
Backtesting Engine - Main Entry Point

This script runs a complete backtest of trading strategies on historical market data,
calculates performance metrics, and generates visualisations.
"""

from data_fetcher import DataFetcher
from strategies import (MovingAverageCrossover, MomentumStrategy, 
                        RSIStrategy, MeanReversionStrategy)
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
    
    results = {}
    
    # Strategy 1: SMA Crossover
    print("\n" + "="*60)
    print("STRATEGY 1: Simple Moving Average Crossover (20, 50)")
    print("="*60)
    
    sma_strategy = MovingAverageCrossover(data, short_window=20, long_window=50)
    backtester_sma = Backtester(data, sma_strategy, initial_capital=initial_capital)
    results_sma = backtester_sma.run()
    metrics_sma = backtester_sma.calculate_metrics()
    backtester_sma.print_metrics()
    results['SMA'] = metrics_sma
    
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
    results['Momentum'] = metrics_momentum
    
    visualiser_momentum = Visualiser(results_momentum, strategy_name="Momentum (20-day)")
    visualiser_momentum.plot_performance(save_path='momentum_performance.png')
    visualiser_momentum.plot_signals(save_path='momentum_signals.png')
    visualiser_momentum.plot_rolling_metrics(save_path='momentum_rolling_metrics.png')
    
    # Strategy 3: RSI
    print("\n" + "="*60)
    print("STRATEGY 3: RSI Strategy (14, oversold=30, overbought=70)")
    print("="*60)
    
    rsi_strategy = RSIStrategy(data, period=14, oversold=30, overbought=70)
    backtester_rsi = Backtester(data, rsi_strategy, initial_capital=initial_capital)
    results_rsi = backtester_rsi.run()
    metrics_rsi = backtester_rsi.calculate_metrics()
    backtester_rsi.print_metrics()
    results['RSI'] = metrics_rsi
    
    visualiser_rsi = Visualiser(results_rsi, strategy_name="RSI (14)")
    visualiser_rsi.plot_performance(save_path='rsi_performance.png')
    visualiser_rsi.plot_signals(save_path='rsi_signals.png')
    visualiser_rsi.plot_rolling_metrics(save_path='rsi_rolling_metrics.png')
    
    # Strategy 4: Mean Reversion
    print("\n" + "="*60)
    print("STRATEGY 4: Mean Reversion Strategy (20, 2 STD)")
    print("="*60)
    
    mr_strategy = MeanReversionStrategy(data, ma_period=20, std_multiplier=2)
    backtester_mr = Backtester(data, mr_strategy, initial_capital=initial_capital)
    results_mr = backtester_mr.run()
    metrics_mr = backtester_mr.calculate_metrics()
    backtester_mr.print_metrics()
    results['Mean Reversion'] = metrics_mr
    
    visualiser_mr = Visualiser(results_mr, strategy_name="Mean Reversion (20, 2σ)")
    visualiser_mr.plot_performance(save_path='mr_performance.png')
    visualiser_mr.plot_signals(save_path='mr_signals.png')
    visualiser_mr.plot_rolling_metrics(save_path='mr_rolling_metrics.png')
    
    # Summary comparison
    print("\n" + "="*60)
    print("STRATEGY COMPARISON SUMMARY")
    print("="*60)
    
    # Get all metrics keys from first strategy
    metric_keys = list(results['SMA'].keys())
    
    # Print header
    header = f"{'Metric':<25}"
    for strategy_name in results.keys():
        header += f"{strategy_name:<20}"
    print(header)
    print("-" * (25 + 20 * len(results)))
    
    # Print each metric row
    for metric_key in metric_keys:
        row = f"{metric_key:<25}"
        for strategy_name in results.keys():
            val = results[strategy_name][metric_key]
            if isinstance(val, float):
                row += f"{val:>18.2%} "
            else:
                row += f"{str(val):>18} "
        print(row)
    
    print("="*60 + "\n")
    
    print("✅ Backtest completed successfully!")
    print("📊 Charts saved for all strategies")
    print("   - sma_performance.png, sma_signals.png, sma_rolling_metrics.png")
    print("   - momentum_performance.png, momentum_signals.png, momentum_rolling_metrics.png")
    print("   - rsi_performance.png, rsi_signals.png, rsi_rolling_metrics.png")
    print("   - mr_performance.png, mr_signals.png, mr_rolling_metrics.png\n")

if __name__ == "__main__":
    # Run backtest with default parameters
    run_backtest()
    
    # Optional: Test with different parameters
    # run_backtest(ticker='AAPL', start_date='2022-01-01', end_date='2024-01-01')