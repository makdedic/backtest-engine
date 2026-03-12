"""
Unit tests for backtesting engine
"""

import unittest
import pandas as pd
import numpy as np
from data_fetcher import DataFetcher
from strategies import MovingAverageCrossover, MomentumStrategy, RSIStrategy, MeanReversionStrategy
from backtester import Backtester

class TestDataFetcher(unittest.TestCase):
    """Test data fetching functionality"""
    
    def setUp(self):
        self.fetcher = DataFetcher('SPY', '2023-01-01', '2023-06-30')
        self.data = self.fetcher.fetch()
    
    def test_fetch_returns_dataframe(self):
        """Test that fetch returns a DataFrame"""
        self.assertIsInstance(self.data, pd.DataFrame)
    
    def test_data_has_required_columns(self):
        """Test that data has OHLCV columns"""
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            self.assertIn(col, self.data.columns)
    
    def test_data_is_sorted_by_date(self):
        """Test that data is sorted chronologically"""
        dates = self.data.index
        self.assertTrue((dates == dates.sort_values()).all())
    
    def test_validate_fills_missing_data(self):
        """Test that validate handles missing values"""
        validated = self.fetcher.validate()
        self.assertEqual(validated.isnull().sum().sum(), 0)


class TestStrategies(unittest.TestCase):
    """Test strategy signal generation"""
    
    def setUp(self):
        fetcher = DataFetcher('SPY', '2023-01-01', '2023-12-31')
        self.data = fetcher.fetch()
    
    def test_sma_generates_signals(self):
        """Test SMA strategy generates signals"""
        strategy = MovingAverageCrossover(self.data)
        result = strategy.generate_signals()
        self.assertIn('Signal', result.columns)
        self.assertIn('SMA_short', result.columns)
        self.assertIn('SMA_long', result.columns)
    
    def test_momentum_generates_signals(self):
        """Test Momentum strategy generates signals"""
        strategy = MomentumStrategy(self.data)
        result = strategy.generate_signals()
        self.assertIn('Signal', result.columns)
        self.assertIn('Momentum', result.columns)
    
    def test_rsi_generates_signals(self):
        """Test RSI strategy generates signals"""
        strategy = RSIStrategy(self.data)
        result = strategy.generate_signals()
        self.assertIn('Signal', result.columns)
        self.assertIn('RSI', result.columns)
    
    def test_signals_are_valid(self):
        """Test that signals are -1, 0, or 1"""
        strategy = MovingAverageCrossover(self.data)
        result = strategy.generate_signals()
        valid_signals = {-1, 0, 1}
        self.assertTrue(set(result['Signal'].unique()).issubset(valid_signals))


class TestBacktester(unittest.TestCase):
    """Test backtesting engine"""
    
    def setUp(self):
        fetcher = DataFetcher('SPY', '2023-01-01', '2023-12-31')
        self.data = fetcher.fetch()
        self.strategy = MovingAverageCrossover(self.data)
        self.backtester = Backtester(self.data, self.strategy)
    
    def test_backtest_runs_successfully(self):
        """Test that backtest runs without errors"""
        result = self.backtester.run()
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_backtest_calculates_portfolio_value(self):
        """Test that portfolio value is calculated"""
        self.backtester.run()
        self.assertIn('Portfolio_Value', self.backtester.data.columns)
    
    def test_metrics_calculated_correctly(self):
        """Test that metrics are calculated"""
        self.backtester.run()
        metrics = self.backtester.calculate_metrics()
        
        # Check all expected metrics exist
        expected_metrics = ['Total Return', 'Annualized Return', 'Sharpe Ratio', 
                          'Max Drawdown', 'Win Rate', 'Buy & Hold Return']
        for metric in expected_metrics:
            self.assertIn(metric, metrics)
    
    def test_sharpe_ratio_is_numeric(self):
        """Test that Sharpe ratio is a number"""
        self.backtester.run()
        metrics = self.backtester.calculate_metrics()
        self.assertIsInstance(metrics['Sharpe Ratio'], (int, float))


if __name__ == '__main__':
    unittest.main()