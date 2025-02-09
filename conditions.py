import numpy as np

def check_conditions(df):
    conditions = {
        'Supertrend': check_supertrend_condition(df),
        'Kijun-sen': check_kijun_sen_condition(df),
        'VWAP': check_vwap_condition(df),
        'ADX': check_adx_condition(df),
        'ATR': check_atr_condition(df),
        'OBV': check_obv_condition(df),
        'Volume Ass.': check_volume_condition(df)
    }
    return conditions

def check_supertrend_condition(df):
    if df['Close'].iloc[-1] > df['Supertrend'].iloc[-1]:
        return "green"
    else:
        return "red"

def check_kijun_sen_condition(df):
    if df['Close'].iloc[-1] > df['Kijun-sen'].iloc[-1]:
        return "green"
    else:
        return "red"

def check_vwap_condition(df):
    if df['Close'].iloc[-1] > df['VWAP'].iloc[-1]:
        return "green"
    else:
        return "red"

def check_adx_condition(df):
    if df['ADX'].iloc[-1] > 25:
        return "green"
    else:
        return "red"

def check_atr_condition(df):
    atr_change = df['ATR'].pct_change().iloc[-1]
    if atr_change > 0:
        return "green"
    else:
        return "red"

def check_obv_condition(df):
    if df['OBV'].iloc[-1] > df['OBV'].mean():
        return "green"
    else:
        return "red"

def check_volume_condition(df):
    if df['Volume'].iloc[-1] > df['Volume'].rolling(window=20).mean().iloc[-1]:
        return "green"
    else:
        return "red"

def update_traffic_lights(traffic_lights, conditions):
    for key, value in conditions.items():
        if key in traffic_lights:
            if value == "green":
                traffic_lights[key]['left'].config(fg="green")
                traffic_lights[key]['right'].config(fg="green")
            else:
                traffic_lights[key]['left'].config(fg="red")
                traffic_lights[key]['right'].config(fg="red")