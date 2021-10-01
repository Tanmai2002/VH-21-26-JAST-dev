from flask_wtf import FlaskForm
# from routes import app
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class VideoForm(FlaskForm):
    video_1 = FileField('Upload video 1', validators=[DataRequired(),FileAllowed(['mp4'])])
    video_2 = FileField('Upload video 2', validators=[DataRequired(),FileAllowed(['mp4'])])
    video_3 = FileField('Upload video 3', validators=[FileAllowed(['mp4'])])
    video_4 = FileField('Upload video 4', validators=[FileAllowed(['mp4'])])
    submit = SubmitField('Upload')
