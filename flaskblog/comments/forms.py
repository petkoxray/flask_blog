from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, URL


class CommentForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    author = StringField('Username',
                         validators=[DataRequired(), Length(min=2, max=20)])
    site_url = StringField('Your site url', validators=[URL()])
    content = TextAreaField('Content', validators=[DataRequired()])
    recaptcha = RecaptchaField()

    submit = SubmitField('Post')
