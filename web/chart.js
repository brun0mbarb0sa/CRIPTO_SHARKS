window.addEventListener('DOMContentLoaded', async () => {
  const chartContainer = document.getElementById('chart');
  const chart = LightweightCharts.createChart(chartContainer, {
    layout: { background: { color: '#1e1e1e' }, textColor: '#DDD' },
    grid: { vertLines: { color: '#333' }, horzLines: { color: '#333' } },
    width: chartContainer.clientWidth,
    height: chartContainer.clientHeight
  });
  const candleSeries = chart.addCandlestickSeries();

  try {
    const csvResp = await fetch('binance_btcusdt_normalized.csv');
    const csvText = await csvResp.text();
    const lines = csvText.trim().split('\n').slice(1);
    const candles = lines.map(line => {
      const [timestamp, open, high, low, close] = line.split(',');
      return {
        time: Math.floor(new Date(timestamp).getTime() / 1000),
        open: parseFloat(open),
        high: parseFloat(high),
        low: parseFloat(low),
        close: parseFloat(close)
      };
    });
    candleSeries.setData(candles);

    const res = await fetch('indicadores.json');
    const indicadores = await res.json();

    for (const [nome, dados] of Object.entries(indicadores)) {
      if (nome.includes('volume_delta')) continue;
      const color = nome.includes('EMA') ? 'orange' : nome.includes('SMA') ? 'cyan' : 'yellow';
      chart.addLineSeries({ color, lineWidth: 2 }).setData(dados);
    }

    const delta = chart.addHistogramSeries({
      color: 'rgba(0,255,0,0.6)',
      scaleMargins: { top: 0.7, bottom: 0 },
      priceFormat: { type: 'volume' }
    });
    delta.setData(indicadores['volume_delta']);

    const deltaSma = chart.addLineSeries({
      color: 'blue',
      lineWidth: 2
    });
    deltaSma.setData(indicadores['volume_delta_sma']);

  } catch (err) {
    console.error("❌ Erro ao carregar dados:", err);
  }
});
