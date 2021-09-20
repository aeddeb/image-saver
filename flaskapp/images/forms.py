from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms import SubmitField

class UploadImageForm(FlaskForm):
    image = FileField("Allowed file types: .jpg, .jpeg, .png or .gif", 
                            validators = [FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif']), 
                                FileSize(1024*1024, message="File must be less than 1 MB.")])
                            
                            
    submit = SubmitField('Upload')