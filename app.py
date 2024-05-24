from flask import Flask, render_template , request, redirect, url_for
import random
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Uploaded Files Folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # Maximum file size
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        video_file = request.files['video_file']
        if video_file and allowed_file(video_file.filename):
            filename = secure_filename(video_file.filename)
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/')
def home():
    # data
    popular_videos = [
        {'title': 'Video 1', 'url': '#'},
        {'title': 'Video 2', 'url': '#'},
        {'title': 'Video 3', 'url': '#'}
    ]
    random_videos = random.sample(popular_videos, len(popular_videos))  # Basit bir rastgele örnekleme

    # get uploaded videos list
    video_files = os.listdir(app.config['UPLOAD_FOLDER'])

    # Şablonu, video listeleri ile birlikte döndür
    return render_template('home.html', popular_videos=popular_videos, random_videos=random_videos, video_files=video_files)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="80")
