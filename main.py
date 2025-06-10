from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import uuid
import tempfile
import logging

app = Flask(__name__)

TEMP_DIR = tempfile.gettempdir()

def baixar_video(link, filename):
    opcoes = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([link])

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        link = request.form.get('ur')
        if not link:
            return "URL inválida", 400

        video_id = str(uuid.uuid4())
        temp_path = os.path.join(TEMP_DIR, f"{video_id}.mp3")

        try:
            baixar_video(link, temp_path)
        except Exception as e:
            app.logger.error(f"Erro ao baixar o vídeo: {e}")
            return f"Erro ao baixar o vídeo: {e}", 500

        if os.path.exists(temp_path):
            return send_file(temp_path, as_attachment=True, download_name="video.mp3")
        else:
            return "Falha ao localizar o arquivo baixado", 500

    return render_template('page.html')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
