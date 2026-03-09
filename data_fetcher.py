import yfinance as yf
import pandas as pd
from datetime import datetime

class DataFetcher:
    """Fetch historical market data from Yahoo Finance"""
    
    def __init__(self, ticker, start_date, end_date):
        """
        Initialize DataFetcher
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'SPY', 'AAPL')
            start_date (str): Start date in format 'YYYY-MM-DD'
            end_date (str): End date in format 'YYYY-MM-DD'
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
    
    def fetch(self):
        """Fetch historical OHLCV data from Yahoo Finance"""
        print(f"Fetching data for {self.ticker} from {self.start_date} to {self.end_date}...")
        self.data = yf.download(
            self.ticker,
            start=self.start_date,
            end=self.end_date,
            progress=False
        )
        print(f"Successfully fetched {len(self.data)} rows of data")
        return self.data
    
    def validate(self):
        """Check for missing data and data quality issues"""
        if self.data is None:
            raise ValueError("No data fetched. Call fetch() first.")
        
        missing_data = self.data.isnull().sum().sum()
        if missing_data > 0:
            print(f"Warning: {missing_data} missing values detected")
        
        print("Data validation complete")
        return self.data
    
    def get_data(self):
        """Return the fetched and validated data"""
        return self.data