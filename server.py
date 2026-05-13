from flask import Flask, render_template, jsonify, send_file, request
from flask_cors import CORS
import json, os, io
import qrcode

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'web_veriler.json')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = []
    # en yüksek 50 öğeyi sıralı olarak döndür
    data = sorted(data, key=lambda x: x.get('score', 0), reverse=True)[:50]
    return jsonify(data)

@app.route('/qr')
def qr():
    url = request.host_url.rstrip('/')
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
