from flask import Flask, render_template, request
import yt_dlp
import os

app = Flask(__name__)

# Ruta de descargas
carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads", "VideosYouTube")
os.makedirs(carpeta_descargas, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/descargar-mp4")
def descargar_mp4():
    return render_template("descarga-mp4.html")

# --- NUEVA RUTA (GET) ---
@app.route("/descargar-mp3")
def descargar_mp3():
    return render_template("descarga-mp3.html")

@app.route("/descargar", methods=["POST"])
def descargar():
    url = request.form.get("url")
    if not url:
        return "No se proporcionó ninguna URL.", 400

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(carpeta_descargas, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'ffmpeg_location': 'C:\\ffmpeg\\bin',  

        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "✅ ¡Descarga completada!"
    except Exception as e:
        return f"❌ Error al descargar: {str(e)}", 500

# --- NUEVA RUTA (POST) ---
@app.route("/descargar-audio", methods=["POST"])
def descargar_audio():
    url = request.form.get("url")
    if not url:
        return "No se proporcionó ninguna URL.", 400

    # Opciones de YDL para MP3
    ydl_opts = {
        'format': 'bestaudio/best', # Solo descarga el mejor audio
        'outtmpl': os.path.join(carpeta_descargas, '%(title)s.mp3'), # Guarda como mp3
        'noplaylist': True,
        'ffmpeg_location': 'C:\\ffmpeg\\bin', # ¡Esencial para convertir a MP3!
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',      # El formato de salida
            'preferredquality': '192',    # Calidad del MP3
        }],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "✅ ¡Descarga de MP3 completada!"
    except Exception as e:
        return f"❌ Error al descargar audio: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)