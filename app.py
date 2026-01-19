#Simple Flask application
from flask import Flask, jsonify, render_template_string
from datetime import datetime, timezone
import threading

app = Flask(__name__)

# Metrics storage
metrics = {
    "start_time": datetime.now(timezone.utc),
    "total_requests": 0,
    "endpoints": {
        "/": 0,
        "/health": 0,
        "/api/info": 0,
        "/dashboard": 0
    }
}
metrics_lock = threading.Lock()

@app.before_request
def track_request():
    from flask import request
    with metrics_lock:
        metrics["total_requests"] += 1
        if request.path in metrics["endpoints"]:
            metrics["endpoints"][request.path] += 1

@app.route('/')
def home():
    return jsonify({
        "message": "This is a secret webpage made possible with the powerful Harness tool!",
        "status": "success"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy"
    }), 200

@app.route('/api/info')
def info():
    return jsonify({
        "app": "Python Flask Demo",
        "version": "1.0.0",
        "description": "Sample app for Harness Enterprise SE Lab"
    })

@app.route('/api/metrics')
def get_metrics():
    with metrics_lock:
        uptime = (datetime.now(timezone.utc) - metrics["start_time"]).total_seconds()
        return jsonify({
            "uptime_seconds": round(uptime, 2),
            "total_requests": metrics["total_requests"],
            "endpoints": metrics["endpoints"]
        })

@app.route('/dashboard')
def dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>App Metrics Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #00d4ff;
            margin-bottom: 30px;
        }
        .metric-card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            backdrop-filter: blur(10px);
        }
        .metric-title {
            font-size: 14px;
            color: #aaa;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 36px;
            font-weight: bold;
            color: #00d4ff;
        }
        .endpoints {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        .endpoint {
            background: rgba(0,212,255,0.1);
            padding: 10px;
            border-radius: 5px;
        }
        .endpoint-path {
            font-family: monospace;
            color: #00d4ff;
        }
        .endpoint-count {
            font-size: 24px;
            font-weight: bold;
        }
        .status {
            text-align: center;
            font-size: 12px;
            color: #666;
            margin-top: 20px;
        }
        .live-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #00ff88;
            border-radius: 50%;
            margin-right: 5px;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Live Metrics Dashboard</h1>

        <div class="metric-card">
            <div class="metric-title">Uptime</div>
            <div class="metric-value" id="uptime">--</div>
        </div>

        <div class="metric-card">
            <div class="metric-title">Total Requests</div>
            <div class="metric-value" id="total-requests">--</div>
        </div>

        <div class="metric-card">
            <div class="metric-title">Requests by Endpoint</div>
            <div class="endpoints" id="endpoints"></div>
        </div>

        <div class="status">
            <span class="live-dot"></span> Auto-refreshing every 2 seconds
        </div>
    </div>

    <script>
        function formatUptime(seconds) {
            const hrs = Math.floor(seconds / 3600);
            const mins = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            return `${hrs}h ${mins}m ${secs}s`;
        }

        async function updateMetrics() {
            try {
                const response = await fetch('/api/metrics');
                const data = await response.json();

                document.getElementById('uptime').textContent = formatUptime(data.uptime_seconds);
                document.getElementById('total-requests').textContent = data.total_requests;

                const endpointsDiv = document.getElementById('endpoints');
                endpointsDiv.innerHTML = '';
                for (const [path, count] of Object.entries(data.endpoints)) {
                    endpointsDiv.innerHTML += `
                        <div class="endpoint">
                            <div class="endpoint-path">${path}</div>
                            <div class="endpoint-count">${count}</div>
                        </div>
                    `;
                }
            } catch (e) {
                console.error('Failed to fetch metrics:', e);
            }
        }

        updateMetrics();
        setInterval(updateMetrics, 2000);
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)