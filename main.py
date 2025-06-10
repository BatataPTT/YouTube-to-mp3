from flask import Flask, request, render_template, send_file, after_this_request
import yt_dlp
import os
import uuid
from threading import Thread

app = Flask(__name__)

TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

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

            if os.path.exists(temp_path):
                @after_this_request
                def cleanup(response):
                    try:
                        os.remove(temp_path)
                    except Exception as e:
                        print(f"Erro ao remover: {e}")
                    return response

                return send_file(temp_path, as_attachment=True, download_name="video.mp3")
            else:
                return "Falha ao baixar o vídeo", 500

        except Exception as e:
            print("Erro:", e)
            return "Erro durante o download", 500

    return render_template('page.html')

if __name__ == "__main__":
    app.run(debug=True)
