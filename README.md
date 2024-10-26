
### Method 1: Using Mermaid Bar Chart
```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#8884d8', 'secondaryColor': '#82ca9d', 'tertiaryColor': '#ffc658'}}}%%
barchart
    title Performance Metrics by Mode
    "No Detection" 30 "FPS" 33 "Latency (ms)" 15 "CPU Usage (%)"
    "Face Detection" 25 "FPS" 40 "Latency (ms)" 35 "CPU Usage (%)"
    "Detection + Recording" 22 "FPS" 45 "Latency (ms)" 45 "CPU Usage (%)"
```

# Binance Testnet Real-Time Price Comparison Tool

## Overview
This Python script is designed to compare cryptocurrency prices between real market sources (CoinGecko and Coinbase) and Binance Testnet prices. It monitors prices in real time and displays the differences between them. Additionally, it synchronizes the local machine's time with Binance's server time to ensure accurate timestamped requests and fetches account balances and open positions from the Binance Testnet.

## Features
- Synchronizes local time with Binance server time
- Fetches Bitcoin (BTC) prices from CoinGecko and Coinbase
- Retrieves mark and symbol prices from Binance Testnet
- Compares real market prices with Binance Testnet prices
- Calculates and displays differences between prices
- Fetches Binance Testnet account balance and open positions
- Periodically updates every 5 seconds

## Prerequisites
- Python 3.x
- Required libraries:
  - `binance` (install via `pip install python-binance`)
  - `requests` (install via `pip install requests`)
  - `pandas` (install via `pip install pandas`)
  - `ntplib` (install via `pip install ntplib`)

## Installation
1. Install the required libraries using the following command:
```bash
pip install python-binance requests pandas ntplib
```

2. Ensure you have the correct API keys from Binance. You can sign up for a testnet account at Binance Testnet and generate API keys for development.

## How to Run
1. Clone the repository or copy the script into your Python environment
2. Modify the `api_key` and `api_secret` in the `initialize_testnet_client()` function with your Binance Testnet credentials
3. Run the script using:
```bash
python price_comparison.py
```

## Script Breakdown

### 1. Time Synchronization
The script synchronizes local machine time with Binance server time using the `get_time_offset()` and `sync_time()` functions. This ensures that the requests to Binance Testnet include accurate timestamps.

### 2. Price Fetching
- `get_prices()`: Fetches Bitcoin (BTC) prices from CoinGecko and Coinbase APIs
- `compare_prices()`: Retrieves prices from Binance Testnet and compares them with the real market prices from CoinGecko and Coinbase

### 3. Binance Client Initialization
- `initialize_testnet_client()`: Initializes the Binance Testnet client using the provided API keys

### 4. Price Comparison
The `compare_prices()` function continuously fetches prices from both the real market and Binance Testnet. It calculates the percentage difference between real market prices (Coinbase) and Binance's mark price, and displays the results.

### 5. Account and Positions
The script fetches the available balance and open positions from the Binance Testnet and displays them during each update cycle.

## Example Output
```
Starting price comparison tool...
Synchronizing time with Binance servers...
Time offset: 20ms
Successfully connected to Binance Testnet

=== Price Comparison ===
Timestamp: 2024-10-22 12:00:00

Real Market Prices:
CoinGecko: $33,000.00
Coinbase: $33,050.00

Testnet Prices:
Mark Price: $33,100.00
Symbol Price: $33,110.00

Difference vs Coinbase: $50.00 (0.15%)

Testnet Balance: $10,000.00 USDT

Open Positions:
Symbol: BTCUSDT
Amount: 0.05
Entry Price: $33,000.00
=====================
```

## Notes
- The script assumes you are using Binance's Testnet for testing purposes
- Adjust the sleep intervals in the main loop if you want to modify the frequency of price updates
- Ensure your API keys are securely stored and not shared publicly

## Future Improvements
- Add more error handling and logging
- Support multiple cryptocurrency pairs for comparison
- Implement a GUI for real-time monitoring

## License
This project is licensed under the MIT License.
