from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, EmailField, URLField
from flask_ckeditor import CKEditorField
from wtforms.widgets import TextArea
from wtforms.validators import Length, Email, DataRequired, URL, InputRequired


class LoginForm(FlaskForm):
    email = StringField('Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])
    submit = SubmitField("LOGIN")


class CreateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()])
    submit = SubmitField("SIGN-UP")


class CreateBlogPostForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=3, max=50)])
    subtitle = StringField('Subtitle', [DataRequired(), Length(min=3, max=120)])
    img_url = URLField("Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Write Your Post Here")
    submit = SubmitField("Create Post")


class PostEditForm(CreateBlogPostForm):
    new_body = CKEditorField("Edit Your Post Here", [InputRequired(), Length(min=50, max=5000)])
    submit = SubmitField("Update Post")


class CommentForm(FlaskForm):
    comment = StringField('Comment Here', widget=TextArea(), validators=[InputRequired()])
    submit = SubmitField("Submit Comment")


class ContactUsForm(FlaskForm):
    name = StringField('Name', [DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', [DataRequired(), Email()])
    message = StringField(label='Message', widget=TextArea(), validators=[DataRequired(), Length(min=10)])
    send = SubmitField("SEND MESSAGE")


class EditProfileForm(FlaskForm):
    profile_img = FileField('Image File', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg'])])
    profession = StringField('Your Profession')
    bio = StringField(label='Write Your Bio', widget=TextArea())
    submit = SubmitField("Save")
