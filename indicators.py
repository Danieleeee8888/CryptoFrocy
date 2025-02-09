import pandas as pd

# Funzione per calcolare il Supertrend
def calculate_supertrend(df, atr_period=10, multiplier=3):
    df['TR'] = df[['High', 'Close']].max(axis=1) - df[['Low', 'Close']].min(axis=1)
    df['ATR'] = df['TR'].rolling(atr_period).mean()
    df['Upper_Band'] = ((df['High'] + df['Low']) / 2) + (multiplier * df['ATR'])
    df['Lower_Band'] = ((df['High'] + df['Low']) / 2) - (multiplier * df['ATR'])
    df['Supertrend'] = df['Upper_Band']
    for i in range(1, len(df)):
        if df.iloc[i]['Close'] > df.iloc[i-1]['Supertrend']:
            df.loc[df.index[i], 'Supertrend'] = df.loc[df.index[i], 'Lower_Band']
        elif df.iloc[i]['Close'] < df.iloc[i-1]['Supertrend']:
            df.loc[df.index[i], 'Supertrend'] = df.loc[df.index[i], 'Upper_Band']
    return df

# Funzione per calcolare la Kijun-sen della Ichimoku Cloud
def calculate_ichimoku(df, period=26):
    df['Kijun-sen'] = (df['High'].rolling(window=period).max() + df['Low'].rolling(window=period).min()) / 2
    return df

# Funzione per calcolare il VWAP
def calculate_vwap(df):
    df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
    return df

# Funzione per calcolare il MACD
def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    df['MACD'] = df['Close'].ewm(span=fast_period, adjust=False).mean() - df['Close'].ewm(span=slow_period, adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    return df

# Funzione per calcolare l'RSI
def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# Funzione per calcolare le varie EMA
def calculate_emas(df, periods=[8, 13, 21, 34, 55]):
    for period in periods:
        df[f'EMA{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
    return df

# Funzione per calcolare le bande di Bollinger
def calculate_bollinger_bands(df, period=20, multiplier=2):
    df['Bollinger_Middle'] = df['Close'].rolling(window=period).mean()
    df['Bollinger_Upper'] = df['Bollinger_Middle'] + (df['Close'].rolling(window=period).std() * multiplier)
    df['Bollinger_Lower'] = df['Bollinger_Middle'] - (df['Close'].rolling(window=period).std() * multiplier)
    return df

# Funzioni per calcolare ADX, ATR, EMA, OBV
def calculate_adx(df, period=14):
    df['TR'] = df[['High', 'Low']].max(axis=1) - df[['Low', 'Close']].min(axis=1)
    df['+DM'] = df['High'].diff()
    df['-DM'] = df['Low'].diff()
    df['+DM'] = df.apply(lambda row: row['+DM'] if row['+DM'] > row['-DM'] and row['+DM'] > 0 else 0, axis=1)
    df['-DM'] = df.apply(lambda row: row['-DM'] if row['-DM'] > row['+DM'] and row['-DM'] > 0 else 0, axis=1)
    df['TR14'] = df['TR'].rolling(window=period).sum()
    df['+DM14'] = df['+DM'].rolling(window=period).sum()
    df['-DM14'] = df['-DM'].rolling(window=period).sum()
    df['+DI14'] = 100 * (df['+DM14'] / df['TR14'])
    df['-DI14'] = 100 * (df['-DM14'] / df['TR14'])
    df['DX'] = 100 * abs(df['+DI14'] - df['-DI14']) / (df['+DI14'] + df['-DI14'])
    df['ADX'] = df['DX'].rolling(window=period).mean()
    return df

def calculate_atr(df, period=14):
    df['TR'] = df[['High', 'Low']].max(axis=1) - df[['Low', 'Close']].min(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()
    return df

def calculate_ema(df, column, period=50):
    df[f'EMA{period}_{column}'] = df[column].ewm(span=period, adjust=False).mean()
    return df

def calculate_obv(df):
    obv = [0]
    for i in range(1, len(df)):
        if df.iloc[i]['Close'] > df.iloc[i-1]['Close']:
            obv.append(obv[-1] + df.iloc[i]['Volume'])
        elif df.iloc[i]['Close'] < df.iloc[i-1]['Close']:
            obv.append(obv[-1] - df.iloc[i]['Volume'])
        else:
            obv.append(obv[-1])
    df['OBV'] = obv
    return df