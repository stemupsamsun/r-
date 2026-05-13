from flask import Flask, render_template, jsonify, send_file, request
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

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

@app.route('/api/skor', methods=['POST'])
def add_score():
    try:
        incoming = request.get_json()
        if not incoming:
            return jsonify({'success': False, 'error': 'No JSON payload'}), 400
        # Load existing data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    data_list = json.load(f)
                except Exception:
                    data_list = []
        else:
            data_list = []
        data_list.append(incoming)
        # Write back
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
