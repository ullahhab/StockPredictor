import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Download stock data
ticker = "AUST"  # Replace with your desired ticker
data = yf.download(ticker, period="5y")  # Adjust period as needed

# Calculate MACD
short_ema = data["Close"].ewm(span=12, min_periods=12).mean()
long_ema = data["Close"].ewm(span=26, min_periods=26).mean()
macd = short_ema - long_ema
signal = macd.ewm(span=9, min_periods=9).mean()  # Signal line

# Add MACD and signal line to DataFrame
data["MACD"] = macd
data["Signal"] = signal

# Visualize MACD and signal line
plt.figure(figsize=(12, 6))
plt.plot(data["Close"], label="Close Price")
plt.plot(data["MACD"], label="MACD", linestyle="--")
plt.plot(data["Signal"], label="Signal", linestyle="-.")
plt.legend()
plt.show()
