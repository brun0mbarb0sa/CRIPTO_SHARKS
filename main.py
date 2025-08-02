import os
import json
import pandas as pd
import requests
from datetime import datetime
from indicators.classic import calcular_indicadores

RAW_DIR = 'data/raw'
PROCESSED_DIR = 'data/processed'
WEB_DIR = 'web'
CONFIG_PATH = 'indicators/config.json'

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(WEB_DIR, exist_ok=True)

def fetch_binance_futures_klines():
    url = "https://fapi.binance.com/fapi/v1/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "limit": 1000
    }
    print("📥 Coletando dados de velas da Binance...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df.to_csv(f"{RAW_DIR}/binance_btcusdt_klines.csv", index=False)
    print(f"✅ Dados brutos salvos em {RAW_DIR}/binance_btcusdt_klines.csv")
    return df

def normalize_volume(df):
    print("🔄 Normalizando volume em USD...")
    df = df.copy()
    df['volume_usd'] = df['close'] * df['volume']
    output_path = f"{PROCESSED_DIR}/binance_btcusdt_normalized.csv"
    df[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'volume_usd']].to_csv(output_path, index=False)
    print(f"✅ Volume normalizado salvo em {output_path}")
    return df

def calcular_e_salvar_indicadores(df):
    print("📊 Calculando indicadores técnicos...")
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    df_ind = calcular_indicadores(df, config)
    df_ind.to_csv(f"{PROCESSED_DIR}/binance_indicadores.csv", index=False)
    print(f"✅ Indicadores salvos em {PROCESSED_DIR}/binance_indicadores.csv")
    return df_ind

def exportar_para_json(df_ind):
    print("🧾 Exportando indicadores para JSON (chart.js)...")
    df_ind['time'] = pd.to_datetime(df_ind['timestamp']).astype(int) // 10**9
    colunas = [c for c in df_ind.columns if c not in ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'volume_usd', 'time']]
    result = {}
    for col in colunas:
        result[col] = [{"time": int(t), "value": float(v)} for t, v in zip(df_ind['time'], df_ind[col]) if pd.notna(v)]
    with open(f"{WEB_DIR}/indicadores.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"✅ JSON exportado para {WEB_DIR}/indicadores.json")

if __name__ == "__main__":
    df_raw = fetch_binance_futures_klines()
    df_norm = normalize_volume(df_raw)
    df_ind = calcular_e_salvar_indicadores(df_norm)
    exportar_para_json(df_ind)
    print("🏁 Processo finalizado com sucesso.")
