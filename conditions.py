import pandas as pd

def check_conditions(df):
    """
    Questa funzione verifica le condizioni specificate e restituisce un dizionario con i risultati.
    Ogni chiave del dizionario rappresenta un indicatore e il valore è True (verde) o False (rosso).
    """
    conditions = {
        'Supertrend': False,
        'Kijun-sen': False,
        'VWAP': False,
        'ADX': False,
        'ATR': False,
        'OBV': False,
        'Volume Ass.': False
    }

    if not df.empty:
        latest_candle = df.iloc[-2]

        # Condizioni Long/Short
        if 'Supertrend' in df.columns:
            conditions['Supertrend'] = latest_candle['Close'] > latest_candle['Supertrend']
        
        if 'Kijun-sen' in df.columns:
            conditions['Kijun-sen'] = latest_candle['Close'] > latest_candle['Kijun-sen']
        
        if 'VWAP' in df.columns:
            conditions['VWAP'] = latest_candle['Close'] > latest_candle['VWAP']

        # Condizioni Volatilità
        if 'ADX' in df.columns:
            conditions['ADX'] = latest_candle['ADX'] >= 25

        if 'ATR' in df.columns and 'EMA50_ATR' in df.columns:
            conditions['ATR'] = latest_candle['ATR'] >= latest_candle['EMA50_ATR']

        # Condizioni Volumi
        if 'OBV' in df.columns and 'EMA50_OBV' in df.columns:
            conditions['OBV'] = latest_candle['OBV'] >= latest_candle['EMA50_OBV']

        if 'Volume' in df.columns and 'EMA50_Volume' in df.columns:
            conditions['Volume Ass.'] = latest_candle['Volume'] >= latest_candle['EMA50_Volume']

    return conditions

# Funzione di aggiornamento dei semafori
def update_traffic_lights(traffic_lights, conditions):
    """
    Aggiorna i semafori visivi basati sulle condizioni fornite.
    """
    for key, value in conditions.items():
        if value:
            traffic_lights[key].config(bg='green')
        else:
            traffic_lights[key].config(bg='red')