from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import Length

class PostsForm(FlaskForm):
    content = TextAreaField('',render_kw={'placeholder':'这一刻的想法...'},validators=[Length(5,128,message='说话要注意分寸（5~128）')])
    submit = SubmitField('提交')