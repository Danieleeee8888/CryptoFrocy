import ccxt
import pandas as pd
import csv
from datetime import datetime
import utilities
from tkinter import messagebox

def get_exchange():
    return ccxt.binance()

def download_ohlcv(app):
    try:
        ohlcv = app.exchange.fetch_ohlcv('BTC/USDC', timeframe='1m', limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df.index = df.index.tz_localize('UTC')
        df = utilities.calculate_indicators(df, app.indicators)
        latest_candle = df.iloc[-2]
        values = utilities.get_values(latest_candle, app.indicators)
        row_id = app.tree.insert("", "end", values=values)
        app.tree.tag_configure('bold_font', font=('Helvetica', 10, 'bold'))
        app.tree.item(row_id, tags=('bold_font',))
        conditions = utilities.check_conditions(df)
        utilities.update_traffic_lights(app, conditions)
    except Exception as e:
        app.tree.insert("", "end", values=("Errore", str(e), "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""))

def save_to_csv(app):
    directory = app.directory_entry.get()
    if directory:
        if app.tree.get_children():
            first_row_id = app.tree.get_children()[0]
            first_row = app.tree.item(first_row_id)['values']
            report_time = first_row[0].replace("/", ".").replace(":", ".")
            file_path = f"{directory}/Report del {report_time}.csv"
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                columns = get_columns(app)
                writer.writerow(columns)
                for row_id in app.tree.get_children():
                    row = app.tree.item(row_id)['values']
                    writer.writerow(row)
            messagebox.showinfo("Info", f"Dati salvati correttamente in {file_path}")
        else:
            messagebox.showwarning("Warning", "Nessun dato disponibile nella tabella per salvare.")
    else:
        messagebox.showwarning("Warning", "Per favore, inserisci una directory di salvataggio valida.")

def get_columns(app):
    columns = ["DateTime", "Open", "High", "Low", "Close", "Volume"]
    if app.indicators['Supertrend'].get():
        columns.append('Supertrend')
    if app.indicators['VWAP'].get():
        columns.append('VWAP')
    if app.indicators['Kijun-sen'].get():
        columns.append('Kijun-sen')
    if app.indicators['MACD'].get():
        columns.extend(['MACD', 'MACD_Signal', 'MACD_Histogram'])
    if app.indicators['RSI'].get():
        columns.append('RSI')
    if app.indicators['ADX'].get():
        columns.append('ADX')
    if app.indicators['ATR'].get():
        columns.extend(['ATR', 'EMA50_ATR'])
    if app.indicators['OBV'].get():
        columns.extend(['OBV', 'EMA50_OBV'])
    if app.indicators['EMA Fibonacci'].get():
        columns.extend(['EMA8', 'EMA13', 'EMA21', 'EMA34', 'EMA55'])
    if app.indicators['Bande di Bollinger'].get():
        columns.extend(['Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower'])
    if app.indicators['EMA50 Volume'].get():
        columns.append('EMA50_Volume')
    return columns