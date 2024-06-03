import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Define the stock ticker and period
ticker = 'MYNA'  # MYNA ticker symbol
period = '6mo'

# Download historical data for the past 6 months
data = yf.download(ticker, period=period)

# Calculate Moving Averages
data['20_SMA'] = data['Close'].rolling(window=20).mean()
data['50_SMA'] = data['Close'].rolling(window=50).mean()

# Plot the data
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['20_SMA'], label='20-Day SMA', color='orange')
plt.plot(data['50_SMA'], label='50-Day SMA', color='green')
plt.axhline(y=5, color='red', linestyle='--', label='Buy Price ($5)')
plt.axhline(y=5.25, color='purple', linestyle='--', label='Sell Price ($5.25)')
plt.title(f'{ticker} Price and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

# Print recent data to understand current price trend
print(data.tail())