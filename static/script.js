// script.js – veri çek ve animasyonlu tablo satırları

async function loadBoard(){
  const res = await fetch('/data');
  const data = await res.json();
  const tbody = document.querySelector('#board tbody');
  tbody.innerHTML = '';
  data.forEach((row,i)=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${i+1}</td><td>${row.name}</td><td>${row.score}</td>`;
    // Staggered animation: delay based on index
    tr.style.animationDelay = `${i * 0.1}s`;
    tbody.appendChild(tr);
  });
}

async function loadQR(){
  const img = document.createElement('img');
  img.src = '/qr';
  document.getElementById('qr').appendChild(img);
}

window.addEventListener('load',()=>{ loadBoard(); loadQR();
  const btn = document.getElementById('copyLink');
  if (btn) {
    btn.addEventListener('click',()=>{
      navigator.clipboard.writeText(window.location.origin).then(()=>{ alert('Site linki kopyalandı!'); });
    });
  }
});
