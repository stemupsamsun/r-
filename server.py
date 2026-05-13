# -------------------------------------------------
# server.py – eksik endpoint'lerin eklenmesi
# -------------------------------------------------
from flask import Flask, render_template, jsonify, send_file, request
from flask_cors import CORS
import json, os, io
import qrcode

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})   # CORS ayarı

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'web_veriler.json')

# ------------------- Mevcut route'lar -------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def data():
    """leaderboard için kullanılan orijinal endpoint (client‑side script.js)"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = []
    # En yüksek skora göre sıralayıp ilk 50'yi gönder
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

# ------------------- Yeni GET endpoint'ler -------------------
@app.route('/api/istatistikler')
def istatistikler():
    """
    İstatistikler: toplam oyuncu, toplam test, en iyi skor
    (frontend “checkServer()” fonksiyonu bu endpoint’i çağırıyor)
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = []

    total_players = len({d.get('ad') for d in data})          # benzersiz oyuncu sayısı
    total_tests   = len(data)                                 # toplam giriş (test)
    best_score    = min([d.get('score', 0) for d in data] or [None])
    result = {
        "success": True,
        "total_players": total_players,
        "total_tests": total_tests,
        "best_score": best_score
    }
    return jsonify(result)

@app.route('/api/skorlar')
def skorlar():
    """
    Front‑end “loadScores()” fonksiyonu bu endpoint’i GET eder
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = []
    # En yüksek skora göre sıralayıp 50 geri döndür
    data = sorted(data, key=lambda x: x.get('score', 0), reverse=True)[:50]
    return jsonify({"success": True, "data": data})

# ------------------- POST – yeni skor ekle -------------------
@app.route('/api/skor', methods=['POST'])
def add_score():
    try:
        incoming = request.get_json()
        if not incoming:
            return jsonify({'success': False, 'error': 'No JSON payload'}), 400

        # Mevcut veriyi oku
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    data_list = json.load(f)
                except Exception:
                    data_list = []
        else:
            data_list = []

        data_list.append(incoming)

        # Yaz back
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)

        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# -------------------------------------------------
if __name__ == '__main__':
    # Render, PORT ortam değişkenini otomatik verir
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
