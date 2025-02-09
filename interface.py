import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
import time
from datetime import datetime
import pytz
import data_handler
import utilities

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto OHLCV Downloader")
        self.root.geometry("1800x800")

        self.running = False
        self.exchange = data_handler.get_exchange()
        self.last_timestamp = None

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
            'Bande di Bollinger': tk.BooleanVar(),
            'EMA50 Volume': tk.BooleanVar()
        }

        self.checkbuttons = {}
        self.create_interface()

    def create_interface(self):
        # Frame per gli indicatori
        indicators_frame = tk.Frame(self.root)
        indicators_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        tk.Label(indicators_frame, text="INDICATORI:", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
        for indicator in self.indicators:
            self.checkbuttons[indicator] = tk.Checkbutton(indicators_frame, text=indicator, variable=self.indicators[indicator])
            self.checkbuttons[indicator].pack(anchor=tk.W)

        # Frame per i semafori di controllo
        traffic_lights_frame = tk.Frame(indicators_frame)
        traffic_lights_frame.pack(fill=tk.Y, pady=10)
        tk.Label(traffic_lights_frame, text="SEMAFORI DI CONTROLLO:", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
        self.traffic_lights = utilities.create_traffic_lights(traffic_lights_frame)

        # Frame per il resto dell'interfaccia
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pair_label = tk.Label(main_frame, text="BTC/USDC", font=("Helvetica", 16))
        self.pair_label.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        self.clock_label = tk.Label(main_frame, font=("Helvetica", 16))
        self.clock_label.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=40)
        self.update_clock()
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
        self.tree = ttk.Treeview(main_frame, columns=("DateTime", "Open", "High", "Low", "Close", "Volume"), show='headings')
        utilities.setup_treeview(self.tree)
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)
        self.scrollbar_x = ttk.Scrollbar(main_frame, orient='horizontal', command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.config(xscrollcommand=self.scrollbar_x.set)
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
            data_handler.download_ohlcv(self)  # Scarica subito i dati dell'ultima candela chiusa
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
            data_handler.save_to_csv(self)

    def update_columns(self):
        columns = data_handler.get_columns(self)
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=100)

    def reset_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def update_data_periodically(self):
        while self.running:
            current_second = datetime.now(pytz.timezone('Europe/Rome')).second
            if current_second == 2:
                data_handler.download_ohlcv(self)
                time.sleep(1)

    def update_clock(self):
        current_time = datetime.now(pytz.timezone('Europe/Rome')).strftime('%d/%m/%Y %H:%M:%S')
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def disable_controls(self):
        for indicator in self.checkbuttons:
            self.checkbuttons[indicator].config(state=tk.DISABLED)
        self.directory_entry.config(state=tk.DISABLED)
        self.directory_button.config(state=tk.DISABLED)

    def enable_controls(self):
        for indicator in self.checkbuttons:
            self.checkbuttons[indicator].config(state=tk.NORMAL)
        self.directory_entry.config(state=tk.NORMAL)
        self.directory_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()