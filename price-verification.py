from binance.client import Client
import requests
import pandas as pd
from datetime import datetime
import time
import ntplib
from typing import Tuple

def get_time_offset() -> int:
    """Get time offset between local and server time"""
    try:
        # Get Binance server time
        response = requests.get('https://fapi.binance.com/fapi/v1/time')
        server_time = int(response.json()['serverTime'])
        local_time = int(time.time() * 1000)
        return server_time - local_time
    except Exception as e:
        print(f"Error getting time offset: {e}")
        return 0

def sync_time():
    """Synchronize with Binance server time"""
    try:
        # Get the time offset
        offset = get_time_offset()
        print(f"Time offset: {offset}ms")
        
        if abs(offset) >= 1000:
            print("Local time is not synchronized with server time.")
            print("Adjusting requests to account for time difference...")
        else:
            print("Time is properly synchronized")
        
        return offset
    except Exception as e:
        print(f"Error in time sync: {e}")
        return 0

def get_prices() -> Tuple[float, float]:
    """Get prices from multiple sources"""
    try:
        # Get CoinGecko price
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        coingecko_price = float(response.json()['bitcoin']['usd'])
        
        # Get Coinbase price
        response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
        coinbase_price = float(response.json()['data']['amount'])
        
        return coingecko_price, coinbase_price
    except Exception as e:
        print(f"Error getting market prices: {e}")
        return None, None

def initialize_testnet_client(time_offset: int = 0):
    """Initialize Binance Testnet client with proper configuration"""
    try:
        client = Client(
            api_key="a8a877e475070f4daf24211ca07ddd9a95efc5aeeeae2b8bdeddb0da7740dd0b",
            api_secret="cbd5ab54a2a619d56aa890c8d062eabe40fe61566e570a8d96d3d9511c89b081",
            testnet=True
        )
        
        # Test the connection with time offset
        _ = client.futures_exchange_info()
        print("Successfully connected to Binance Testnet")
        return client
    except Exception as e:
        print(f"Error initializing client: {e}")
        return None

def compare_prices(client: Client, time_offset: int):
    """Compare prices between testnet and real market"""
    symbol = "BTCUSDT"
    
    while True:
        try:
            # Add time offset to requests
            timestamp = int(time.time() * 1000) + time_offset
            
            # Get market prices
            coingecko_price, coinbase_price = get_prices()
            
            # Get testnet prices
            try:
                mark_price_info = client.futures_mark_price(symbol=symbol, timestamp=timestamp)
                symbol_price_info = client.futures_symbol_ticker(symbol=symbol, timestamp=timestamp)
                
                mark_price = float(mark_price_info['markPrice'])
                symbol_price = float(symbol_price_info['price'])
                
                print("\n=== Price Comparison ===")
                print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                print("\nReal Market Prices:")
                if coingecko_price:
                    print(f"CoinGecko: ${coingecko_price:,.2f}")
                if coinbase_price:
                    print(f"Coinbase: ${coinbase_price:,.2f}")
                
                print("\nTestnet Prices:")
                print(f"Mark Price: ${mark_price:,.2f}")
                print(f"Symbol Price: ${symbol_price:,.2f}")
                
                # Calculate differences
                if coinbase_price:
                    diff = mark_price - coinbase_price
                    diff_pct = (diff / coinbase_price) * 100
                    print(f"\nDifference vs Coinbase:")
                    print(f"${diff:,.2f} ({diff_pct:.2f}%)")
                
                # Get account information
                account = client.futures_account(timestamp=timestamp)
                balance = float(account['availableBalance'])
                print(f"\nTestnet Balance: ${balance:,.2f} USDT")
                
                # Show positions
                positions = [p for p in account['positions'] if float(p['positionAmt']) != 0]
                if positions:
                    print("\nOpen Positions:")
                    for pos in positions:
                        print(f"Symbol: {pos['symbol']}")
                        print(f"Amount: {pos['positionAmt']}")
                        print(f"Entry Price: ${float(pos['entryPrice']):,.2f}")
                
                print("=====================")
                
            except Exception as e:
                print(f"Error getting testnet data: {e}")
                # Resync time if we get timestamp errors
                if "Timestamp" in str(e):
                    print("Resyncing time...")
                    time_offset = sync_time()
            
            time.sleep(5)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("Starting price comparison tool...")
    print("Synchronizing time with Binance servers...")
    
    # Initial time synchronization
    time_offset = sync_time()
    
    # Initialize client
    client = initialize_testnet_client(time_offset)
    
    if client:
        print("\nStarting price monitoring...")
        compare_prices(client, time_offset)
    else:
        print("Failed to initialize testnet client.")