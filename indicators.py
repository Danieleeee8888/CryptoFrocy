import pandas as pd
import numpy as np

def calculate_supertrend(df, atr_period=10, multiplier=3):
    hl2 = (df['High'] + df['Low']) / 2
    df['ATR'] = df['High'].rolling(window=atr_period).max() - df['Low'].rolling(window=atr_period).min()
    df['UpperBand'] = hl2 + (multiplier * df['ATR'])
    df['LowerBand'] = hl2 - (multiplier * df['ATR'])
    df['Supertrend'] = np.nan
    for current in range(1, len(df.index)):
        previous = current - 1
        if df.loc[current, 'Close'] > df.loc[previous, 'UpperBand']:
            df.loc[current, 'Supertrend'] = df.loc[current, 'UpperBand']
        elif df.loc[current, 'Close'] < df.loc[previous, 'LowerBand']:
            df.loc[current, 'Supertrend'] = df.loc[current, 'LowerBand']
        else:
            df.loc[current, 'Supertrend'] = df.loc[previous, 'Supertrend']
    df.drop(['UpperBand', 'LowerBand', 'ATR'], axis=1, inplace=True)
    return df

def calculate_ichimoku(df, period=26):
    df['Kijun-sen'] = (df['High'].rolling(window=period).max() + df['Low'].rolling(window=period).min()) / 2
    return df

def calculate_vwap(df):
    df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
    return df

def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    df['EMA12'] = df['Close'].ewm(span=fast_period, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=slow_period, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['MACD_Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    df.drop(['EMA12', 'EMA26'], axis=1, inplace=True)
    return df

def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def calculate_adx(df, period=14):
    df['TR'] = np.maximum(df['High'] - df['Low'], np.maximum(abs(df['High'] - df['Close'].shift()), abs(df['Low'] - df['Close'].shift())))
    df['+DM'] = np.where((df['High'] - df['High'].shift()) > (df['Low'].shift() - df['Low']), df['High'] - df['High'].shift(), 0)
    df['+DM'] = np.where(df['+DM'] < 0, 0, df['+DM'])
    df['-DM'] = np.where((df['Low'].shift() - df['Low']) > (df['High'] - df['High'].shift()), df['Low'].shift() - df['Low'], 0)
    df['-DM'] = np.where(df['-DM'] < 0, 0, df['-DM'])
    df['TR'] = df['TR'].rolling(window=period).sum()
    df['+DM'] = df['+DM'].rolling(window=period).sum()
    df['-DM'] = df['-DM'].rolling(window=period).sum()
    df['+DI'] = 100 * (df['+DM'] / df['TR'])
    df['-DI'] = 100 * (df['-DM'] / df['TR'])
    df['DX'] = 100 * (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI']))
    df['ADX'] = df['DX'].rolling(window=period).mean()
    df.drop(['TR', '+DM', '-DM', '+DI', '-DI', 'DX'], axis=1, inplace=True)
    return df

def calculate_atr(df, period=14):
    df['TR'] = np.maximum(df['High'] - df['Low'], np.maximum(abs(df['High'] - df['Close'].shift()), abs(df['Low'] - df['Close'].shift())))
    df['ATR'] = df['TR'].rolling(window=period).mean()
    df.drop('TR', axis=1, inplace=True)
    return df

def calculate_ema(df, column, period=50):
    df[f'EMA{period}_{column}'] = df[column].ewm(span=period, adjust=False).mean()
    return df

def calculate_obv(df):
    df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).cumsum()
    return df

def calculate_emas(df, periods=[8, 13, 21, 34, 55]):
    for period in periods:
        df[f'EMA{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
    return df

def calculate_bollinger_bands(df, period=20, multiplier=2):
    df['Bollinger_Middle'] = df['Close'].rolling(window=period).mean()
    df['Bollinger_Upper'] = df['Bollinger_Middle'] + (df['Close'].rolling(window=period).std() * multiplier)
    df['Bollinger_Lower'] = df['Bollinger_Middle'] - (df['Close'].rolling(window=period).std() * multiplier)
    return df