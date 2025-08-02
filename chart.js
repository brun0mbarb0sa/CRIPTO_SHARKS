
window.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('chart');
  if (!container) return console.error("❌ Elemento #chart não encontrado");

  const chart = LightweightCharts.createChart(container, {
    width: container.clientWidth,
    height: container.clientHeight,
    layout: {
      background: { color: '#1e1e1e' },
      textColor: '#DDD'
    },
    grid: {
      vertLines: { color: '#333' },
      horzLines: { color: '#333' }
    }
  });

  const candleSeries = chart.addCandlestickSeries();
  candleSeries.setData([
    { time: 1690000000, open: 29000, high: 29300, low: 28800, close: 29100 },
    { time: 1690000600, open: 29100, high: 29400, low: 29050, close: 29300 },
    { time: 1690001200, open: 29300, high: 29500, low: 29200, close: 29400 }
  ]);
});
