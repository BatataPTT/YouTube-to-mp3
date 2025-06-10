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
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': filename,
        'quiet': True,
        'merge_output_format': 'mp4'
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
        temp_path = os.path.join(TEMP_DIR, f"{video_id}.mp4")

        thread = Thread(target=baixar_video, args=(link, temp_path))
        thread.start()
        thread.join()

        if os.path.exists(temp_path):
            @after_this_request
            def cleanup(response):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
                return response

            return send_file(temp_path, as_attachment=True, download_name="video.mp4")

    return render_template('page.html')

if __name__ == "__main__":
    app.run(debug=True)
