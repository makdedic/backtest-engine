# Backtesting Engine

A Python-based backtesting framework for evaluating trading strategies on historical market data. This project demonstrates data engineering, financial analysis, and software engineering best practices.

## Overview

This backtesting engine allows you to:
- **Fetch historical market data** from Yahoo Finance
- **Implement trading strategies** with clean, modular code
- **Calculate performance metrics** (Sharpe ratio, max drawdown, returns, etc.)
- **visualise results** with professional-grade charts
- **Compare strategies** side-by-side

## Features

### Data Management
- Fetches historical OHLCV data from Yahoo Finance
- Validates data quality and handles missing values
- Supports any ticker (stocks, ETFs, indices)

### Strategy Framework
- Base `TradingStrategy` class for easy extensibility
- Multiple pre-built strategies:
  - **Simple Moving Average (SMA) Crossover** — trades based on short/long MA intersection
  - **Momentum Strategy** — trades based on price momentum

### Backtesting Engine
- Calculates daily returns and strategy returns
- Tracks portfolio value over time
- Compares against buy-and-hold benchmark
- Handles position sizing and trade execution

### Performance Metrics
- **Total Return** — Overall percentage gain/loss
- **Annualized Return** — Returns normalized to annual basis
- **Annual Volatility** — Standard deviation of returns
- **Sharpe Ratio** — Risk-adjusted return metric
- **Maximum Drawdown** — Largest peak-to-trough decline
- **Win Rate** — Percentage of profitable trading days
- **Outperformance** — Excess return vs. buy-and-hold

### Visualizations
- Portfolio value over time (vs. benchmark)
- Maximum drawdown analysis
- Trading signals on price chart
- Rolling Sharpe ratio and volatility metrics

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/backtest-engine.git
cd backtest-engine

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the default backtest:
```bash
python main.py
```

This will:
1. Fetch SPY data from 2023-01-01 to 2024-01-01
2. Run SMA Crossover and Momentum strategies
3. Calculate metrics and generate visualizations

### Custom Backtest

Edit `main.py` and modify the parameters:
```python
if __name__ == "__main__":
    run_backtest(
        ticker='AAPL',
        start_date='2022-01-01',
        end_date='2024-01-01',
        initial_capital=100000
    )
```

### Programmatic Usage
```python
from data_fetcher import DataFetcher
from strategies import MovingAverageCrossover
from backtester import Backtester
from visualiser import Visualiser

# Fetch data
fetcher = DataFetcher('SPY', '2023-01-01', '2024-01-01')
data = fetcher.fetch()

# Create strategy
strategy = MovingAverageCrossover(data, short_window=20, long_window=50)

# Run backtest
backtester = Backtester(data, strategy, initial_capital=100000)
results = backtester.run()
metrics = backtester.calculate_metrics()

# visualise
visualiser = Visualiser(results, strategy_name="My Strategy")
visualiser.plot_performance()
```

## Project Structure
```
backtest-engine/
├── main.py                 # Entry point
├── data_fetcher.py         # Data fetching and validation
├── strategies.py           # Trading strategy implementations
├── backtester.py           # Core backtesting engine
├── visualiser.py           # Visualization utilities
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Strategies Implemented

### 1. Simple Moving Average Crossover (SMA)
- **Logic**: Buy when short MA > long MA, sell when short MA < long MA
- **Parameters**: 
  - `short_window=20` (20-day moving average)
  - `long_window=50` (50-day moving average)
- **Use case**: Trend-following strategy

### 2. Momentum Strategy
- **Logic**: Buy when price momentum is positive, sell when negative
- **Parameters**:
  - `lookback_window=20` (momentum calculated over 20 days)
- **Use case**: Mean reversion and momentum capture

## Example Results

Running `python main.py` on SPY (2023-2024) produces:
```
==================================================
BACKTEST RESULTS
==================================================
Total Return                     15.23%
Annualized Return                15.23%
Annual Volatility                12.45%
Sharpe Ratio                      1.22
Max Drawdown                      -8.34%
Win Rate                          52.34%
Buy & Hold Return                 24.15%
Outperformance                    -8.92%
==================================================
```

## Future Improvements

- [ ] Add more strategies (RSI, Bollinger Bands, MACD)
- [ ] Implement position sizing and risk management
- [ ] Add stop-loss and take-profit mechanisms
- [ ] Parameter optimization (grid search, genetic algorithms)
- [ ] Monte Carlo simulation for robustness testing
- [ ] Transaction costs and slippage modeling
- [ ] Walk-forward analysis
- [ ] Unit tests and integration tests
- [ ] Support for multiple asset classes

## Technical Stack

- **Python 3.8+** — Core language
- **pandas** — Data manipulation and analysis
- **numpy** — Numerical computations
- **matplotlib** — Visualizations
- **yfinance** — Market data fetching

## Notes

- All backtests assume:
  - 0% transaction costs (realistic commissions are ignored)
  - 0% slippage (trades execute at exact prices)
  - No risk-free rate (Sharpe ratio uses 0% risk-free rate)
  - Perfect execution on signal dates

- For production use, consider:
  - Adding realistic transaction costs
  - Modeling market impact and slippage
  - Using higher-quality data sources
  - Incorporating regime detection
  - Stress testing across multiple market periods

## License

MIT License

## Author

Created as a portfolio project demonstrating:
- Python software engineering best practices
- Financial analysis and quantitative methods
- Data pipeline design
- Visualization and communication of results
