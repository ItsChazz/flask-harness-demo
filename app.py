#Simple Flask application
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from Harness CI/CD Lab!",
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)