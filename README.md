# Crypto OHLCV Downloader

Questo repository contiene un'applicazione Python per scaricare e analizzare i dati OHLCV (Open, High, Low, Close, Volume) delle criptovalute. L'applicazione è costruita con Tkinter per l'interfaccia grafica e utilizza la libreria `ccxt` per interagire con l'exchange Binance. Il codice è suddiviso in diversi moduli per una migliore organizzazione e manutenzione.

## Moduli

### 1. Modulo Interfaccia (`interface.py`)
Questo modulo gestisce gli elementi dell'interfaccia utente utilizzando Tkinter. Contiene la classe `CryptoApp`, che è responsabile della creazione della finestra principale, dell'aggiunta di widget e della gestione delle interazioni dell'utente.

#### Funzioni Principali:
- `create_interface()`: Configura i componenti principali dell'interfaccia, inclusi i pulsanti di selezione per gli indicatori, i semafori e i pulsanti per avviare, mettere in pausa e resettare.
- `browse_directory()`: Apre una finestra di dialogo per selezionare una directory per il salvataggio dei dati.
- `start()`, `pause()`, `reset()`: Controllano lo stato dell'applicazione (in esecuzione, in pausa, resettata).
- `update_columns()`: Aggiorna le colonne nella tabella dei dati in base agli indicatori selezionati.
- `reset_table()`: Cancella la tabella dei dati.
- `update_data_periodically()`: Scarica periodicamente nuovi dati OHLCV.
- `update_clock()`: Aggiorna l'orologio digitale nell'interfaccia.
- `disable_controls()`, `enable_controls()`: Abilitano o disabilitano i controlli dell'interfaccia utente.

### 2. Modulo Gestione Dati (`data_handler.py`)
Questo modulo gestisce il download, l'elaborazione e il salvataggio dei dati. Interagisce con l'exchange Binance per scaricare i dati OHLCV e li elabora per calcolare vari indicatori.

#### Funzioni Principali:
- `get_exchange()`: Inizializza e restituisce l'oggetto exchange.
- `download_ohlcv(app)`: Scarica i dati OHLCV, calcola gli indicatori e aggiorna la tabella dei dati.
- `save_to_csv(app)`: Salva i dati nella tabella in un file CSV.
- `get_columns(app)`: Restituisce i nomi delle colonne per la tabella dei dati in base agli indicatori selezionati.

### 3. Modulo Utilità (`utilities.py`)
Questo modulo contiene funzioni di utilità e calcoli per gli indicatori. Fornisce funzioni per creare e aggiornare i semafori, calcolare gli indicatori e configurare la tabella dei dati.

#### Funzioni Principali:
- `create_traffic_lights(frame)`: Crea i semafori per ciascun gruppo di indicatori.
- `calculate_indicators(df, indicators)`: Calcola gli indicatori selezionati e li aggiunge al DataFrame.
- `get_values(latest_candle, indicators)`: Estrae i valori dalla candela più recente in base agli indicatori selezionati.
- `check_conditions(df)`: Verifica le condizioni di trading in base ai valori degli indicatori.
- `update_traffic_lights(app, conditions)`: Aggiorna i semafori in base alle condizioni di trading.
- `setup_treeview(tree)`: Configura le colonne e le intestazioni della tabella dei dati.

### 4. Modulo Condizioni (`conditions.py`)
Questo modulo definisce le funzioni per verificare le condizioni di trading e aggiornare i semafori in base ai valori degli indicatori.

#### Funzioni Principali:
- `check_conditions(df)`: Verifica le condizioni di trading e restituisce un dizionario con i risultati per ciascun indicatore.
- `update_traffic_lights(traffic_lights, conditions)`: Aggiorna i semafori visivi in base alle condizioni fornite.

### 5. Modulo Indicatori (`indicators.py`)
Questo modulo fornisce varie funzioni per calcolare gli indicatori tecnici utilizzati nell'applicazione.

#### Funzioni Principali:
- `calculate_supertrend(df, atr_period=10, multiplier=3)`: Calcola l'indicatore Supertrend.
- `calculate_ichimoku(df, period=26)`: Calcola la Kijun-sen della Ichimoku Cloud.
- `calculate_vwap(df)`: Calcola il VWAP (Volume Weighted Average Price).
- `calculate_macd(df, fast_period=12, slow_period=26, signal_period=9)`: Calcola il MACD (Moving Average Convergence Divergence).
- `calculate_rsi(df, period=14)`: Calcola l'RSI (Relative Strength Index).
- `calculate_adx(df, period=14)`: Calcola l'ADX (Average Directional Index).
- `calculate_atr(df, period=14)`: Calcola l'ATR (Average True Range).
- `calculate_ema(df, column, period=50)`: Calcola l'EMA per una colonna specifica.
- `calculate_obv(df)`: Calcola l'OBV (On-Balance Volume).
- `calculate_emas(df, periods=[8, 13, 21, 34, 55])`: Calcola varie EMA (Exponential Moving Averages).
- `calculate_bollinger_bands(df, period=20, multiplier=2)`: Calcola le Bande di Bollinger.

## Gerarchia dei Moduli

1. **Applicazione Principale (interface.py)**
   - Gestisce l'interfaccia utente e il flusso complessivo dell'applicazione.
   - Chiama le funzioni di `data_handler.py` per recuperare e elaborare i dati OHLCV.
   - Utilizza `utilities.py` per impostare e gestire la tabella dei dati e i semafori.

2. **Gestione Dati (data_handler.py)**
   - Interagisce con l'exchange Binance per recuperare i dati OHLCV.
   - Elabora i dati e calcola gli indicatori utilizzando le funzioni di `utilities.py` e `indicators.py`.
   - Salva i dati elaborati in un file CSV.

3. **Utilità (utilities.py)**
   - Fornisce funzioni di utilità per creare semafori, calcolare indicatori e impostare la tabella dei dati.
   - Chiama le funzioni di `indicators.py` per calcolare gli indicatori tecnici.
   - Utilizza `conditions.py` per verificare le condizioni di trading e aggiornare i semafori.

4. **Condizioni (conditions.py)**
   - Definisce funzioni per verificare le condizioni di trading in base ai valori degli indicatori.
   - Aggiorna i semafori in base alle condizioni di trading.

5. **Indicatori (indicators.py)**
   - Fornisce funzioni per calcolare vari indicatori tecnici come Supertrend, VWAP, MACD, RSI, ADX, ATR, EMA, OBV e Bande di Bollinger.

## Come Eseguire

1. Clona il repository.
2. Installa i pacchetti richiesti:
   ```sh
   pip install -r requirements.txt
