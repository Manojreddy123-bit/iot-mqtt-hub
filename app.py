import sqlite3
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
DB = "data.db"

def query(sql, args=()):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute(sql, args).fetchall()
    con.close()
    return [dict(r) for r in rows]

@app.route("/api/latest")
def latest():
    rows = query("SELECT ts, topic, temp, hum FROM readings ORDER BY rowid DESC LIMIT 1")
    return jsonify(rows[0] if rows else {})

@app.route("/api/history")
def history():
    rows = query("SELECT ts, temp, hum FROM readings ORDER BY rowid DESC LIMIT 60")
    return jsonify(rows[::-1])

PAGE = """
<!doctype html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IoT Hub</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  body{font-family:system-ui,sans-serif;margin:0;padding:16px;background:#f4f6f8;color:#222}
  h1{font-size:1.3rem}
  .cards{display:flex;gap:12px;flex-wrap:wrap}
  .card{flex:1;min-width:140px;background:#fff;border-radius:10px;padding:16px;box-shadow:0 1px 3px #0002}
  .val{font-size:2rem;font-weight:600}
  .small{color:#777;font-size:.8rem}
  .chart{background:#fff;border-radius:10px;padding:12px;margin-top:12px;box-shadow:0 1px 3px #0002}
</style></head>
<body>
<h1>IoT Sensor Hub</h1>
<div class="cards">
  <div class="card"><div class="small">Temperature</div><div class="val" id="t">--</div></div>
  <div class="card"><div class="small">Humidity</div><div class="val" id="h">--</div></div>
  <div class="card"><div class="small">Last update (UTC)</div><div id="ts">--</div></div>
</div>
<div class="chart"><canvas id="chart"></canvas></div>
<script>
const chart = new Chart(document.getElementById('chart'), {
  type:'line',
  data:{labels:[],datasets:[
    {label:'Temp (C)',data:[],borderColor:'#e4572e',tension:.3},
    {label:'Humidity (%)',data:[],borderColor:'#2e86e4',tension:.3}]},
  options:{animation:false,responsive:true}
});
async function refresh(){
  const l = await (await fetch('/api/latest')).json();
  if(l.temp!==undefined){
    document.getElementById('t').textContent = l.temp + ' C';
    document.getElementById('h').textContent = l.hum + ' %';
    document.getElementById('ts').textContent = l.ts;
  }
  const hist = await (await fetch('/api/history')).json();
  chart.data.labels = hist.map(r=>r.ts.slice(11));
  chart.data.datasets[0].data = hist.map(r=>r.temp);
  chart.data.datasets[1].data = hist.map(r=>r.hum);
  chart.update();
}
refresh(); setInterval(refresh, 5000);
</script></body></html>
"""

@app.route("/")
def index():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
