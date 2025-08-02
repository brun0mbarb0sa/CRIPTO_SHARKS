import pandas as pd

def calcular_indicadores(df, config):
    df = df.copy()
    for ind in config.get("indicadores", []):
        nome = ind["nome"]
        periodo = ind.get("periodo", 14)
        fonte = ind.get("fonte", "close")

        if nome == "sma":
            df[f"SMA_{periodo}"] = df[fonte].rolling(window=periodo).mean()
        elif nome == "ema":
            df[f"EMA_{periodo}"] = df[fonte].ewm(span=periodo, adjust=False).mean()
        elif nome == "rsi":
            delta = df[fonte].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=periodo).mean()
            avg_loss = loss.rolling(window=periodo).mean()
            rs = avg_gain / avg_loss
            df[f"RSI_{periodo}"] = 100 - (100 / (1 + rs))
    return df
