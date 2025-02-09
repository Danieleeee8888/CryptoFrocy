import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import ccxt
import threading
import time
import csv
from datetime import datetime, timezone
import pytz
import pandas as pd
from indicators import calculate_supertrend, calculate_ichimoku, calculate_vwap, calculate_macd, calculate_rsi, calculate_adx, calculate_atr, calculate_ema, calculate_obv, calculate_emas, calculate_bollinger_bands

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto OHLCV Downloader")
        self.root.geometry("1800x800")
        
        self.running = False
        self.exchange = ccxt.binance()  # Inizializza l'oggetto Binance
        self.last_timestamp = None  # Ultimo timestamp della candela chiusa

        self.indicators = {
            'Supertrend': tk.BooleanVar(),
            'VWAP': tk.BooleanVar(),
            'Kijun-sen': tk.BooleanVar(),
            'MACD': tk.BooleanVar(),
            'RSI': tk.BooleanVar(),
            'ADX': tk.BooleanVar(),
            'ATR': tk.BooleanVar(),
            'OBV': tk.BooleanVar(),
            'EMA Fibonacci': tk.BooleanVar(),
            'Bande di Bollinger': tk.BooleanVar()
        }

        self.checkbuttons = {}

        # Frame per gli indicatori
        indicators_frame = tk.Frame(root)
        indicators_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Etichetta per gli indicatori
        tk.Label(indicators_frame, text="INDICATORI:", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)

        # Aggiungi le spunte per gli indicatori
        for indicator in self.indicators:
            self.checkbuttons[indicator] = tk.Checkbutton(indicators_frame, text=indicator, variable=self.indicators[indicator])
            self.checkbuttons[indicator].pack(anchor=tk.W)

        # Frame per il resto dell'interfaccia
        main_frame = tk.Frame(root)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Aggiungi l'etichetta con il nome della coppia in alto a destra
        self.pair_label = tk.Label(main_frame, text="BTC/USDC", font=("Helvetica", 16))
        self.pair_label.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        
        # Aggiungi l'orologio digitale sotto l'etichetta della coppia
        self.clock_label = tk.Label(main_frame, font=("Helvetica", 16))
        self.clock_label.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=40)
        self.update_clock()

        # Frame per i pulsanti
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        self.start_button = tk.Button(buttons_frame, text="Avvio", command=self.start, bg="green", fg="white", font=("Helvetica", 12))
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(buttons_frame, text="Pausa", command=self.pause, bg="yellow", fg="black", font=("Helvetica", 12))
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(buttons_frame, text="Reset", command=self.reset, bg="red", fg="white", font=("Helvetica", 12))
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(main_frame, text="Status: In pausa", fg="red", font=("Helvetica", 12))
        self.status_label.pack(pady=10)
        
        # Crea la tabella
        self.tree = ttk.Treeview(main_frame, columns=("DateTime", "Open", "High", "Low", "Close", "Volume"), show='headings')
        self.tree.heading("DateTime", text="Data e Ora")
        self.tree.heading("Open", text="Apertura")
        self.tree.heading("High", text="Massimo")
        self.tree.heading("Low", text="Minimo")
        self.tree.heading("Close", text="Chiusura")
        self.tree.heading("Volume", text="Volume")
        
        self.tree.column("DateTime", anchor=tk.CENTER, width=150)
        self.tree.column("Open", anchor=tk.CENTER, width=100)
        self.tree.column("High", anchor=tk.CENTER, width=100)
        self.tree.column("Low", anchor=tk.CENTER, width=100)
        self.tree.column("Close", anchor=tk.CENTER, width=100)
        self.tree.column("Volume", anchor=tk.CENTER, width=100)
        
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        # Aggiungi la barra di testo per la directory di salvataggio
        self.directory_label = tk.Label(main_frame, text="Directory di salvataggio:", font=("Helvetica", 12))
        self.directory_entry = tk.Entry(main_frame, width=50, font=("Helvetica", 12))
        self.directory_entry.insert(0, "C:/Users/danie/OneDrive/Desktop/binaNCE/nuovo_bot/Report")
        self.directory_button = tk.Button(main_frame, text="Sfoglia", command=self.browse_directory, font=("Helvetica", 12))
        
        self.directory_label.pack(pady=5)
        self.directory_entry.pack(pady=5)
        self.directory_button.pack(pady=5)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, directory)

    def start(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: In attesa dei dati", fg="green")
            self.update_columns()
            self.download_ohlcv()  # Scarica subito i dati dell'ultima candela chiusa
            self.thread = threading.Thread(target=self.update_data_periodically)
            self.thread.start()
            self.disable_controls()
        else:
            messagebox.showinfo("Info", "Il download è già in corso.")
    
    def pause(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: In pausa", fg="yellow")
        else:
            messagebox.showinfo("Info", "Il download è già in pausa.")

    def reset(self):
        if self.running:
            self.running = False
        self.ask_save_to_csv()
        self.reset_table()
        self.enable_controls()
        self.status_label.config(text="Status: In pausa", fg="red")

    def ask_save_to_csv(self):
        save = messagebox.askyesno("Salva", "Vuoi salvare i dati in un file CSV?")
        if save:
            self.save_to_csv()

    def save_to_csv(self):
        directory = self.directory_entry.get()
        if directory:
            if self.tree.get_children():
                first_row_id = self.tree.get_children()[0]
                first_row = self.tree.item(first_row_id)['values']
                report_time = first_row[0].replace("/", ".").replace(":", ".")
                file_path = f"{directory}/Report del {report_time}.csv"
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    columns = self.get_columns()
                    writer.writerow(columns)
                    for row_id in self.tree.get_children():
                        row = self.tree.item(row_id)['values']
                        writer.writerow(row)
                messagebox.showinfo("Info", f"Dati salvati correttamente in {file_path}")
            else:
                messagebox.showwarning("Warning", "Nessun dato disponibile nella tabella per salvare.")
        else:
            messagebox.showwarning("Warning", "Per favore, inserisci una directory di salvataggio valida.")

    def get_columns(self):
        columns = ["DateTime", "Open", "High", "Low", "Close", "Volume"]
        if self.indicators['Supertrend'].get():
            columns.append('Supertrend')
        if self.indicators['VWAP'].get():
            columns.append('VWAP')
        if self.indicators['Kijun-sen'].get():
            columns.append('Kijun-sen')
        if self.indicators['MACD'].get():
            columns.extend(['MACD', 'MACD_Signal', 'MACD_Histogram'])
        if self.indicators['RSI'].get():
            columns.append('RSI')
        if self.indicators['ADX'].get():
            columns.append('ADX')
        if self.indicators['ATR'].get():
            columns.extend(['ATR', 'EMA50_ATR'])
        if self.indicators['OBV'].get():
            columns.extend(['OBV', 'EMA50_OBV'])
        if self.indicators['EMA Fibonacci'].get():
            columns.extend(['EMA8', 'EMA13', 'EMA21', 'EMA34', 'EMA55'])
        if self.indicators['Bande di Bollinger'].get():
            columns.extend(['Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower'])
        return columns

    def update_columns(self):
        columns = self.get_columns()
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=100)

    def download_ohlcv(self):
        try:
            # Scarica i dati dell'ultima candela chiusa
            ohlcv = self.exchange.fetch_ohlcv('BTC/USDC', timeframe='1m', limit=100)  # Aumenta il limite per ottenere più dati storici
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df.index = df.index.tz_localize('UTC')

            # Calcola gli indicatori selezionati
            if self.indicators['Supertrend'].get():
                df = calculate_supertrend(df)
            if self.indicators['VWAP'].get():
                df = calculate_vwap(df)
            if self.indicators['Kijun-sen'].get():
                df = calculate_ichimoku(df)
            if self.indicators['MACD'].get():
                df = calculate_macd(df)
            if self.indicators['RSI'].get():
                df = calculate_rsi(df)
            if self.indicators['ADX'].get():
                df = calculate_adx(df)
            if self.indicators['ATR'].get():
                df = calculate_atr(df)
                df = calculate_ema(df, 'ATR')
            if self.indicators['OBV'].get():
                df = calculate_obv(df)
                df = calculate_ema(df, 'OBV')
            if self.indicators['EMA Fibonacci'].get():
                df = calculate_emas(df)
            if self.indicators['Bande di Bollinger'].get():
                df = calculate_bollinger_bands(df)

            latest_candle = df.iloc[-2]
            values = [latest_candle.name.tz_convert('Europe/Rome').strftime('%d/%m/%Y %H:%M'), round(latest_candle['Open'], 2), round(latest_candle['High'], 2), round(latest_candle['Low'], 2), round(latest_candle['Close'], 2), round(latest_candle['Volume'], 2)]
            if self.indicators['Supertrend'].get():
                values.append(round(latest_candle['Supertrend'], 2))
            if self.indicators['VWAP'].get():
                values.append(round(latest_candle['VWAP'], 2))
            if self.indicators['Kijun-sen'].get():
                values.append(round(latest_candle['Kijun-sen'], 2))
            if self.indicators['MACD'].get():
                values.extend([round(latest_candle['MACD'], 2), round(latest_candle['MACD_Signal'], 2), round(latest_candle['MACD_Histogram'], 2)])
            if self.indicators['RSI'].get():
                values.append(round(latest_candle['RSI'], 2))
            if self.indicators['ADX'].get():
                values.append(round(latest_candle['ADX'], 2))
            if self.indicators['ATR'].get():
                values.extend([round(latest_candle['ATR'], 2), round(latest_candle['EMA50_ATR'], 2)])
            if self.indicators['OBV'].get():
                values.extend([round(latest_candle['OBV'], 2), round(latest_candle['EMA50_OBV'], 2)])
            if self.indicators['EMA Fibonacci'].get():
                values.extend([round(latest_candle['EMA8'], 2), round(latest_candle['EMA13'], 2), round(latest_candle['EMA21'], 2), round(latest_candle['EMA34'], 2), round(latest_candle['EMA55'], 2)])
            if self.indicators['Bande di Bollinger'].get():
                values.extend([round(latest_candle['Bollinger_Upper'], 2), round(latest_candle['Bollinger_Middle'], 2), round(latest_candle['Bollinger_Lower'], 2)])
            self.tree.insert("", "end", values=values)

        except Exception as e:
            self.tree.insert("", "end", values=("Errore", str(e), "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""))

    def reset_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def update_data_periodically(self):
        while self.running:
            current_second = datetime.now(pytz.timezone('Europe/Rome')).second
            if current_second == 2:
                self.download_ohlcv()
                time.sleep(1)  # Evita di eseguire più volte nello stesso secondo

    def update_clock(self):
        current_time = datetime.now(pytz.timezone('Europe/Rome')).strftime('%d/%m/%Y %H:%M:%S')
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def disable_controls(self):
        # Disabilita le spunte e la directory di salvataggio
        for indicator in self.checkbuttons:
            self.checkbuttons[indicator].config(state=tk.DISABLED)
        self.directory_entry.config(state=tk.DISABLED)
        self.directory_button.config(state=tk.DISABLED)

    def enable_controls(self):
        # Abilita le spunte e la directory di salvataggio
        for indicator in self.checkbuttons:
            self.checkbuttons[indicator].config(state=tk.NORMAL)
        self.directory_entry.config(state=tk.NORMAL)
        self.directory_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()