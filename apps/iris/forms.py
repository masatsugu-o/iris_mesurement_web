from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired

class CustomerForm(FlaskForm):
    customer_id = StringField("顧客番号", validators=[DataRequired()])
    name = StringField("氏名", validators=[DataRequired()])
    gender = RadioField("性別", choices=[("男", "男"), ("女", "女")], validators=[DataRequired()])
    memo = TextAreaField("メモ")
    submit = SubmitField("簡易測定")
