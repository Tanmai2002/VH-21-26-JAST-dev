from genericpath import exists
from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage
import os
import secrets
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from forms import VideoForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '15de991f5f224a1d524d408efc1753ac'

# path = os.getcwd()
# UPLOAD_FOLDER = os.path.join(path, 'uploads')
# if not os.path.isdir(UPLOAD_FOLDER):
#     os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/videos')

ALLOWED_EXTENSIONS = {'mp4', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

# def save_video(form_video):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.split(form_video.filename)
#     video_fn = random_hex + f_ext
#     video_path = os.path.join(app.root_path, 'static/videos', video_fn)
#     form_video.save(video_path)
#     return video_fn

@app.route('/')
@app.route('/upload', methods=['GET','POST'])
def upload():
    form = VideoForm()
    if request.method == 'POST':
        for f in request.files.getlist('file_name'):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            return render_template('upload.html', msg="File(s) have been uploaded successfully")
    return render_template('upload.html', title='upload',form=form, msg="Please Choose files")
