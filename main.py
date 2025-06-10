from flask import Flask, request, url_for, render_template
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        link = request.form['ur']
        
        opcoes = {
            'outtmpl': '%(title)s.mp3'
        }
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([link])
    return render_template('page.html')
    
if __name__ == "__main__":
    app.run()
