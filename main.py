from flask import Flask, request, url_for, render_template
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def homepage():
    msg = ""
    if request.method == 'POST':
        link = request.form['ur']
        if link:
            msg = "Baixando..."
            opcoes = {
                'outtmpl': 'Download/yt-to-mp3/%(title)s.mp3'
            }
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                ydl.download([link])
            msg = "Download concluído!"
        else:
            msg = "Insira um link!"
    return render_template('page.html', msg=msg)

if __name__ == "__main__":
    app.run()
