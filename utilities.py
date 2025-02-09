import tkinter as tk
import pandas as pd
from indicators import (calculate_supertrend, calculate_ichimoku, calculate_vwap, calculate_macd,
                        calculate_rsi, calculate_adx, calculate_atr, calculate_ema, calculate_obv,
                        calculate_emas, calculate_bollinger_bands)
from conditions import check_conditions, update_traffic_lights

def create_traffic_lights(frame):
    traffic_lights = {}
    traffic_light_groups = {
        'Long/Short': ['Supertrend', 'Kijun-sen', 'VWAP'],
        'Volatilità': ['ADX', 'ATR'],
        'Volumi': ['OBV', 'Volume Ass.']
    }
    traffic_light_labels = {
        'Supertrend': 'Supertrend',
        'Kijun-sen': 'Kijun-sen',
        'VWAP': 'VWAP',
        'ADX': 'ADX',
        'ATR': 'ATR',
        'OBV': 'OBV',
        'Volume Ass.': 'Volume Ass.'
    }
    for group, indicators in traffic_light_groups.items():
        group_frame = tk.Frame(frame)
        group_frame.pack(anchor=tk.W, pady=5)
        tk.Label(group_frame, text=group + ":", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        for key in indicators:
            sub_frame = tk.Frame(group_frame)
            sub_frame.pack(anchor=tk.W, pady=2)
            tk.Label(sub_frame, text=traffic_light_labels[key], font=("Helvetica", 10)).pack(side=tk.LEFT)
            traffic_lights[key] = {
                'left': tk.Label(sub_frame, text="●", fg="black", font=("Helvetica", 20)),
                'right': tk.Label(sub_frame, text="●", fg="black", font=("Helvetica", 20))
            }
            traffic_lights[key]['left'].pack(side=tk.LEFT, padx=5)
            traffic_lights[key]['right'].pack(side=tk.LEFT, padx=5)
    return traffic_lights

def calculate_indicators(df, indicators):
    if indicators['Supertrend'].get():
        df = calculate_supertrend(df)
    if indicators['VWAP'].get():
        df = calculate_vwap(df)
    if indicators['Kijun-sen'].get():
        df = calculate_ichimoku(df)
    if indicators['MACD'].get():
        df = calculate_macd(df)
    if indicators['RSI'].get():
        df = calculate_rsi(df)
    if indicators['ADX'].get():
        df = calculate_adx(df)
    if indicators['ATR'].get():
        df = calculate_atr(df)
        df = calculate_ema(df, 'ATR')
    if indicators['OBV'].get():
        df = calculate_obv(df)
        df = calculate_ema(df, 'OBV')
    if indicators['EMA Fibonacci'].get():
        df = calculate_emas(df)
    if indicators['Bande di Bollinger'].get():
        df = calculate_bollinger_bands(df)
    if indicators['EMA50 Volume'].get():
        df = calculate_ema(df, 'Volume', 50)
    return df

def get_values(latest_candle, indicators):
    values = [latest_candle.name.tz_convert('Europe/Rome').strftime('%d/%m/%Y %H:%M'), 
              round(latest_candle['Open'], 2), 
              round(latest_candle['High'], 2), 
              round(latest_candle['Low'], 2), 
              round(latest_candle['Close'], 2), 
              round(latest_candle['Volume'], 2)]
    if indicators['Supertrend'].get():
        values.append(round(latest_candle['Supertrend'], 2))
    if indicators['VWAP'].get():
        values.append(round(latest_candle['VWAP'], 2))
    if indicators['Kijun-sen'].get():
        values.append(round(latest_candle['Kijun-sen'], 2))
    if indicators['MACD'].get():
        values.extend([round(latest_candle['MACD'], 2), round(latest_candle['MACD_Signal'], 2), round(latest_candle['MACD_Histogram'], 2)])
    if indicators['RSI'].get():
        values.append(round(latest_candle['RSI'], 2))
    if indicators['ADX'].get():
        values.append(round(latest_candle['ADX'], 2))
    if indicators['ATR'].get():
        values.extend([round(latest_candle['ATR'], 2), round(latest_candle['EMA50_ATR'], 2)])
    if indicators['OBV'].get():
        values.extend([round(latest_candle['OBV'], 2), round(latest_candle['EMA50_OBV'], 2)])
    if indicators['EMA Fibonacci'].get():
        values.extend([round(latest_candle['EMA8'], 2), round(latest_candle['EMA13'], 2), round(latest_candle['EMA21'], 2), 
                       round(latest_candle['EMA34'], 2), round(latest_candle['EMA55'], 2)])
    if indicators['Bande di Bollinger'].get():
        values.extend([round(latest_candle['Bollinger_Upper'], 2), round(latest_candle['Bollinger_Middle'], 2), round(latest_candle['Bollinger_Lower'], 2)])
    if indicators['EMA50 Volume'].get():
        values.append(round(latest_candle['EMA50_Volume'], 2))
    return values

def check_conditions(df):
    return check_conditions(df)

def update_traffic_lights(app, conditions):
    update_traffic_lights(app.traffic_lights, conditions)

def setup_treeview(tree):
    tree.heading("DateTime", text="Data e Ora")
    tree.heading("Open", text="Apertura")
    tree.heading("High", text="Massimo")
    tree.heading("Low", text="Minimo")
    tree.heading("Close", text="Chiusura")
    tree.heading("Volume", text="Volume")
    tree.column("DateTime", anchor=tk.CENTER, width=150)
    tree.column("Open", anchor=tk.CENTER, width=100)
    tree.column("High", anchor=tk.CENTER, width=100)
    tree.column("Low", anchor=tk.CENTER, width=100)
    tree.column("Close", anchor=tk.CENTER, width=100)
    tree.column("Volume", anchor=tk.CENTER, width=100)