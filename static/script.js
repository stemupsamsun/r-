// script.js – veri çek ve animasyonlu tablo satırları

async function loadBoard(){
  try {
    const res = await fetch('/data');
    const API_URL = 'https://r-3kyi.onrender.com/api';
    
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();

    const tbody = document.querySelector('#board tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    data.forEach((row,i)=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${i+1}</td><td>${row.name}</td><td>${row.score}</td>`;
      tr.style.animationDelay = `${i * 0.1}s`;
      tbody.appendChild(tr);
    });

  } catch (err) {
    console.error('loadBoard error:', err);
  }
}

async function loadQR(){
  try {
    const qrContainer = document.getElementById('qr');
    if (!qrContainer) return;

    qrContainer.innerHTML = '';

    const img = document.createElement('img');
    img.src = '/qr';

    img.onerror = () => {
      console.error('QR yüklenemedi');
    };

    qrContainer.appendChild(img);

  } catch (err) {
    console.error('loadQR error:', err);
  }
}

window.addEventListener('load', ()=>{

  loadBoard();
  loadQR();

  // New: send score data to server
  async function sendScore(scoreData) {
    try {
      const response = await fetch(`${API_URL}/skor`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(scoreData)
      });
      const result = await response.json();
      if (result.success) {
        console.log('Score sent successfully');
        // Refresh leaderboard after successful post
        await loadBoard();
      } else {
        console.error('Failed to send score:', result.error || response.status);
      }
    } catch (err) {
      console.error('sendScore error:', err);
    }
  }

  const btn = document.getElementById('copyLink');

  if (btn) {
    btn.addEventListener('click', ()=>{
      navigator.clipboard.writeText(window.location.origin)
        .then(()=>{ alert('Site linki kopyalandı!'); })
        .catch(err => console.error('Clipboard error:', err));
    });
  }

});
