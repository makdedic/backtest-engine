import pandas as pd
import numpy as np

class Backtester:
    """Core backtesting engine that executes strategies and calculates metrics"""
    
    def __init__(self, data, strategy, initial_capital=100000):
        """
        Initialize Backtester
        
        Args:
            data (pd.DataFrame): OHLCV data with 'Close' column
            strategy (TradingStrategy): Strategy object with generate_signals() method
            initial_capital (float): Starting capital in dollars (default: $100,000)
        """
        self.data = data.copy()
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.portfolio = None
        self.metrics = None
    
    def run(self):
        """
        Execute the backtest
        
        Returns:
            pd.DataFrame: Data with returns, signals, and portfolio value columns
        """
        print("Running backtest...")
        
        # Generate trading signals
        self.data = self.strategy.generate_signals()
        
        # Calculate daily returns
        self.data['Returns'] = self.data['Close'].pct_change()
        
        # Calculate strategy returns (shift signal by 1 to avoid lookahead bias)
        self.data['Strategy_Returns'] = self.data['Signal'].shift(1) * self.data['Returns']
        
        # Calculate cumulative returns
        self.data['Cumulative_Returns'] = (1 + self.data['Strategy_Returns']).cumprod()
        
        # Calculate portfolio value over time
        self.data['Portfolio_Value'] = self.initial_capital * self.data['Cumulative_Returns']
        
        # Calculate benchmark (buy and hold)
        self.data['Buy_Hold_Returns'] = self.data['Close'].pct_change()
        self.data['Buy_Hold_Cumulative'] = (1 + self.data['Buy_Hold_Returns']).cumprod()
        self.data['Buy_Hold_Value'] = self.initial_capital * self.data['Buy_Hold_Cumulative']
        
        print("Backtest completed successfully")
        return self.data
    
    def calculate_metrics(self):
        """
        Calculate risk and return metrics
        
        Returns:
            dict: Dictionary of performance metrics
        """
        if self.data is None:
            raise ValueError("Run backtest first with run() method")
        
        # Filter out NaN values
        returns = self.data['Strategy_Returns'].dropna()
        
        if len(returns) == 0:
            raise ValueError("No valid returns to calculate metrics")
        
        # Total return
        final_portfolio_value = self.data['Portfolio_Value'].iloc[-1]
        total_return = (final_portfolio_value / self.initial_capital) - 1
        
        # Annualized return (252 trading days per year)
        num_years = len(self.data) / 252
        annualized_return = (final_portfolio_value / self.initial_capital) ** (1 / num_years) - 1
        
        # Annualized volatility
        annual_volatility = returns.std() * np.sqrt(252)
        
        # Sharpe Ratio (assuming 0% risk-free rate)
        sharpe_ratio = (annualized_return / annual_volatility) if annual_volatility > 0 else 0
        
        # Maximum Drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Win Rate
        winning_days = (returns > 0).sum()
        total_trading_days = len(returns)
        win_rate = winning_days / total_trading_days if total_trading_days > 0 else 0
        
        # Comparison to buy and hold
        buy_hold_returns = self.data['Buy_Hold_Returns'].dropna()
        buy_hold_final = self.data['Buy_Hold_Value'].iloc[-1]
        buy_hold_return = (buy_hold_final / self.initial_capital) - 1
        
        self.metrics = {
            'Total Return': total_return,
            'Annualized Return': annualized_return,
            'Annual Volatility': annual_volatility,
            'Sharpe Ratio': sharpe_ratio,
            'Max Drawdown': max_drawdown,
            'Win Rate': win_rate,
            'Buy & Hold Return': buy_hold_return,
            'Outperformance': total_return - buy_hold_return
        }
        
        return self.metrics
    
    def print_metrics(self):
        """Print metrics in a readable format"""
        if self.metrics is None:
            raise ValueError("Calculate metrics first with calculate_metrics() method")
        
        print("\n" + "="*50)
        print("BACKTEST RESULTS")
        print("="*50)
        for key, value in self.metrics.items():
            if isinstance(value, float):
                print(f"{key:<25} {value:>10.2%}")
            else:
                print(f"{key:<25} {value:>10}")
        print("="*50 + "\n")
    
    def get_data(self):
        """Return the backtest data"""
        return self.data
    
    def get_metrics(self):
        """Return the metrics dictionary"""
        return self.metrics