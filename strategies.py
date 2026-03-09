import pandas as pd
import numpy as np

class TradingStrategy:
    """Base class for trading strategies"""
    
    def __init__(self, data):
        """
        Initialize strategy
        
        Args:
            data (pd.DataFrame): OHLCV data with 'Close' column
        """
        self.data = data.copy()
        self.signals = None
    
    def generate_signals(self):
        """Generate trading signals. Must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement generate_signals()")


class MovingAverageCrossover(TradingStrategy):
    """
    Simple Moving Average Crossover Strategy
    
    Buy signal: Short MA > Long MA
    Sell signal: Short MA < Long MA
    """
    
    def __init__(self, data, short_window=20, long_window=50):
        """
        Initialize SMA Crossover strategy
        
        Args:
            data (pd.DataFrame): OHLCV data
            short_window (int): Short moving average window (default: 20 days)
            long_window (int): Long moving average window (default: 50 days)
        """
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self):
        """
        Generate buy/sell signals based on SMA crossover
        
        Returns:
            pd.DataFrame: Data with 'SMA_short', 'SMA_long', and 'Signal' columns
                         Signal: 1 = long, -1 = short/flat, 0 = no position
        """
        # Calculate simple moving averages
        self.data['SMA_short'] = self.data['Close'].rolling(window=self.short_window).mean()
        self.data['SMA_long'] = self.data['Close'].rolling(window=self.long_window).mean()
        
        # Initialize signal column
        self.data['Signal'] = 0
        
        # Generate signals
        # 1 = in position (long), -1 = out of position
        self.data.loc[self.data['SMA_short'] > self.data['SMA_long'], 'Signal'] = 1
        self.data.loc[self.data['SMA_short'] <= self.data['SMA_long'], 'Signal'] = -1
        
        # Remove NaN values from signal (warm-up period)
        self.data['Signal'] = self.data['Signal'].bfill().ffill()
        
        print(f"Generated signals using SMA({self.short_window}, {self.long_window})")
        return self.data


class MomentumStrategy(TradingStrategy):
    """
    Momentum-based strategy
    
    Buy signal: Price momentum is positive
    Sell signal: Price momentum is negative
    """
    
    def __init__(self, data, lookback_window=20):
        """
        Initialize Momentum strategy
        
        Args:
            data (pd.DataFrame): OHLCV data
            lookback_window (int): Window for momentum calculation (default: 20 days)
        """
        super().__init__(data)
        self.lookback_window = lookback_window
    
    def generate_signals(self):
        """
        Generate buy/sell signals based on momentum
        
        Returns:
            pd.DataFrame: Data with 'Momentum' and 'Signal' columns
        """
        # Calculate momentum (price change over lookback period)
        self.data['Momentum'] = self.data['Close'].pct_change(self.lookback_window)
        
        # Generate signals based on momentum sign
        self.data['Signal'] = 0
        self.data.loc[self.data['Momentum'] > 0, 'Signal'] = 1
        self.data.loc[self.data['Momentum'] <= 0, 'Signal'] = -1
        
        self.data['Signal'] = self.data['Signal'].bfill().ffill()
        
        print(f"Generated signals using Momentum({self.lookback_window})")
        return self.data