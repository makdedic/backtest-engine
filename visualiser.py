import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Visualiser:
    """Create visualizations for backtest results"""
    
    def __init__(self, backtest_data, strategy_name="Strategy"):
        """
        Initialize Visualiser
        
        Args:
            backtest_data (pd.DataFrame): Data from Backtester.run()
            strategy_name (str): Name of the strategy for plot titles
        """
        self.data = backtest_data
        self.strategy_name = strategy_name
    
    def plot_performance(self, save_path='backtest_performance.png'):
        """
        Plot strategy performance vs buy and hold
        
        Args:
            save_path (str): Path to save the figure
        """
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        fig.suptitle(f'{self.strategy_name} Backtest Results', fontsize=16, fontweight='bold')
        
        # Plot 1: Portfolio Value
        ax1 = axes[0]
        ax1.plot(self.data.index, self.data['Portfolio_Value'], label='Strategy', linewidth=2.5, color='#2E86AB')
        ax1.plot(self.data.index, self.data['Buy_Hold_Value'], label='Buy & Hold (SPY)', linewidth=2, alpha=0.7, color='#A23B72')
        ax1.set_ylabel('Portfolio Value ($)', fontsize=11, fontweight='bold')
        ax1.set_title('Portfolio Value Over Time', fontsize=12, fontweight='bold')
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        # Plot 2: Drawdown
        ax2 = axes[1]
        returns = self.data['Strategy_Returns'].dropna()
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        
        ax2.fill_between(self.data.index[1:], drawdown.values, 0, alpha=0.4, color='#F18F01', label='Drawdown')
        ax2.plot(self.data.index[1:], drawdown.values, color='#C1121F', linewidth=1.5)
        ax2.set_ylabel('Drawdown', fontsize=11, fontweight='bold')
        ax2.set_title('Maximum Drawdown Over Time', fontsize=12, fontweight='bold')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc='best', fontsize=10)
        
        # Plot 3: Cumulative Returns Comparison
        ax3 = axes[2]
        strategy_cumulative = self.data['Cumulative_Returns']
        buy_hold_cumulative = self.data['Buy_Hold_Cumulative']
        
        ax3.plot(self.data.index, (strategy_cumulative - 1) * 100, label='Strategy', linewidth=2.5, color='#2E86AB')
        ax3.plot(self.data.index, (buy_hold_cumulative - 1) * 100, label='Buy & Hold', linewidth=2, alpha=0.7, color='#A23B72')
        ax3.set_ylabel('Cumulative Return (%)', fontsize=11, fontweight='bold')
        ax3.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax3.set_title('Cumulative Returns Comparison', fontsize=12, fontweight='bold')
        ax3.legend(loc='best', fontsize=10)
        ax3.grid(True, alpha=0.3)
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}%'))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Performance chart saved to {save_path}")
        plt.show()
    
    def plot_signals(self, save_path='trading_signals.png'):
        """
        Plot price with buy/sell signals
        
        Args:
            save_path (str): Path to save the figure
        """
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Plot price
        ax.plot(self.data.index, self.data['Close'], label='Close Price', linewidth=2, color='#2E86AB')
        
        # Plot buy signals (where Signal changes from -1 to 1)
        buy_signals = self.data[(self.data['Signal'] == 1) & (self.data['Signal'].shift(1) != 1)]
        ax.scatter(buy_signals.index, buy_signals['Close'], color='green', marker='^', s=100, label='Buy Signal', zorder=5)
        
        # Plot sell signals (where Signal changes from 1 to -1)
        sell_signals = self.data[(self.data['Signal'] == -1) & (self.data['Signal'].shift(1) != -1)]
        ax.scatter(sell_signals.index, sell_signals['Close'], color='red', marker='v', s=100, label='Sell Signal', zorder=5)
        
        ax.set_ylabel('Price ($)', fontsize=11, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax.set_title(f'{self.strategy_name} - Trading Signals', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Signals chart saved to {save_path}")
        plt.show()
    
    def plot_rolling_metrics(self, window=30, save_path='rolling_metrics.png'):
        """
        Plot rolling Sharpe ratio and volatility
        
        Args:
            window (int): Rolling window in days
            save_path (str): Path to save the figure
        """
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        fig.suptitle(f'{self.strategy_name} - Rolling Metrics (30-day window)', fontsize=16, fontweight='bold')
        
        # Calculate rolling metrics
        returns = self.data['Strategy_Returns'].dropna()
        rolling_volatility = returns.rolling(window=window).std() * np.sqrt(252)
        rolling_sharpe = (returns.rolling(window=window).mean() * 252) / rolling_volatility
        
        # Plot rolling volatility
        ax1 = axes[0]
        ax1.plot(self.data.index[window:], rolling_volatility.iloc[window:], linewidth=2, color='#F18F01')
        ax1.fill_between(self.data.index[window:], rolling_volatility.iloc[window:], alpha=0.3, color='#F18F01')
        ax1.set_ylabel('Annual Volatility', fontsize=11, fontweight='bold')
        ax1.set_title('Rolling Annual Volatility', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
        
        # Plot rolling Sharpe ratio
        ax2 = axes[1]
        ax2.plot(self.data.index[window:], rolling_sharpe.iloc[window:], linewidth=2, color='#2E86AB')
        ax2.fill_between(self.data.index[window:], rolling_sharpe.iloc[window:], alpha=0.3, color='#2E86AB')
        ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax2.set_ylabel('Sharpe Ratio', fontsize=11, fontweight='bold')
        ax2.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax2.set_title('Rolling Sharpe Ratio', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Rolling metrics chart saved to {save_path}")
        plt.show()