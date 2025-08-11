from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    # WTForms는 기본적인 입력 길이 검증 등을 제공합니다.
    author = StringField('이름', validators=[DataRequired(), Length(min=2, max=80)])
    content = TextAreaField('내용', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('남기기')