# 🦈 CRIPTO SHARKS

Visualizador de indicadores técnicos com dados reais do BTC via Binance.

## 🔎 O que este projeto faz

- Coleta candles da Binance (1m)
- Calcula indicadores (SMA, EMA, RSI)
- Exporta para CSV e JSON
- Exibe os dados com `LightweightCharts` via GitHub Pages

## 🌐 Acesse o gráfico online

Quando publicado via GitHub Pages:

```
https://seu_usuario.github.io/CRIPTO_SHARKS/
```

## 🚀 Como publicar no GitHub Pages

1. Faça push da pasta `/web` com:
   ```bash
   git add web/
   git commit -m "Add frontend"
   git push origin main
   ```

2. Vá em Settings → Pages → Configure para `/web`

## 📦 Requisitos Python

```bash
pip install -r requirements.txt
python main.py
```

> Os indicadores são exportados para `web/indicadores.json` e `data/processed/*.csv`.
