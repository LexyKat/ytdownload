function descargar() {
    const url = document.getElementById('url').value;
    const estado = document.getElementById('estado');
    const progressBar = document.getElementById('progress-bar');
    const loadingBar = document.getElementById('loading-bar');
  
    if (!url) {
      estado.textContent = "Por favor, introduce una URL.";
      return;
    }

    // --- LÓGICA ACTUALIZADA ---
    // Decide a qué URL del servidor llamar
    let postUrl = '/descargar'; // Ruta por defecto (MP4)
    
    // Si estamos en la página de MP3, cambia la URL
    if (window.location.pathname.endsWith('/descargar-mp3')) {
      postUrl = '/descargar-audio'; 
    }
    // -------------------------
  
    loadingBar.style.display = 'block';
    estado.textContent = "Descargando...";
    progressBar.style.width = "0%";
    
    let fakeProgress = 0;
    const interval = setInterval(() => {
      if (fakeProgress < 95) {
        fakeProgress += Math.random() * 5;
        progressBar.style.width = `${Math.min(fakeProgress, 95)}%`;
      }
    }, 500);
  
    // Usa la variable postUrl que definimos arriba
    fetch(postUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'url=' + encodeURIComponent(url),
    })
      .then(response => response.text())
      .then(data => {
        clearInterval(interval);
        progressBar.style.width = '100%';
        estado.textContent = data;
      })
      .catch(err => {
        clearInterval(interval);
        estado.textContent = "❌ Error durante la descarga.";
      });
  }