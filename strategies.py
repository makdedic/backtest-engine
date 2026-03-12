import pandas as pd
import numpy as np

class TradingStrategy:
    """Base class for trading strategies"""
    
    def __init__(self, data):
        """
        Initialise strategy
        
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
        Initialise SMA Crossover strategy
        
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
        
        # Initialise signal column
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
        Initialise Momentum strategy
        
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
    
class RSIStrategy(TradingStrategy):
    """
    Relative Strength Index (RSI) Strategy
    
    Buy signal: RSI < 30 (oversold)
    Sell signal: RSI > 70 (overbought)
    """
    
    def __init__(self, data, period=14, oversold=30, overbought=70):
        """
        Initialise RSI strategy
        
        Args:
            data (pd.DataFrame): OHLCV data
            period (int): RSI calculation period (default: 14)
            oversold (float): Oversold threshold (default: 30)
            overbought (float): Overbought threshold (default: 70)
        """
        super().__init__(data)
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signals(self):
        """Generate buy/sell signals based on RSI"""
        # Calculate RSI
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        
        # Generate signals
        self.data['Signal'] = 0
        self.data.loc[self.data['RSI'] < self.oversold, 'Signal'] = 1
        self.data.loc[self.data['RSI'] > self.overbought, 'Signal'] = -1
        
        # Fill gaps
        self.data['Signal'] = self.data['Signal'].bfill().ffill()
        
        print(f"Generated signals using RSI({self.period}, oversold={self.oversold}, overbought={self.overbought})")
        return self.data


class MeanReversionStrategy(TradingStrategy):
    """
    Mean Reversion Strategy
    
    Buy signal: Price is 2 std devs below 20-day MA
    Sell signal: Price returns to 20-day MA
    """
    
    def __init__(self, data, ma_period=20, std_multiplier=2):
        """
        Initialise Mean Reversion strategy
        
        Args:
            data (pd.DataFrame): OHLCV data
            ma_period (int): Moving average period (default: 20)
            std_multiplier (float): Standard deviation multiplier (default: 2)
        """
        super().__init__(data)
        self.ma_period = ma_period
        self.std_multiplier = std_multiplier
    
    def generate_signals(self):
        """Generate buy/sell signals based on mean reversion"""
        # Calculate Bollinger Bands
        self.data['MA'] = self.data['Close'].rolling(window=self.ma_period).mean()
        self.data['STD'] = self.data['Close'].rolling(window=self.ma_period).std()
        self.data['Upper_Band'] = self.data['MA'] + (self.data['STD'] * self.std_multiplier)
        self.data['Lower_Band'] = self.data['MA'] - (self.data['STD'] * self.std_multiplier)
        
        # Generate signals - ensure Close is a Series first
        close = self.data['Close'].squeeze() if isinstance(self.data['Close'], pd.DataFrame) else self.data['Close']

        # Generate signals
        self.data['Signal'] = 0
        self.data.loc[close.values < self.data['Lower_Band'].values, 'Signal'] = 1
        self.data.loc[close.values > self.data['MA'].values, 'Signal'] = -1
        
        self.data['Signal'] = self.data['Signal'].bfill().ffill()
        
        print(f"Generated signals using Mean Reversion(MA={self.ma_period}, STD={self.std_multiplier})")
        return self.data