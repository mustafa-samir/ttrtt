from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models.models import User

class LoginForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    remember_me = BooleanField('تذكرني')
    submit = SubmitField('تسجيل الدخول')

class RegistrationForm(FlaskForm):
    first_name = StringField('الاسم الأول', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('الاسم الأخير', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    role = SelectField('الدور', coerce=int, validators=[DataRequired()])
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('تسجيل')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('اسم المستخدم مستخدم بالفعل. الرجاء اختيار اسم آخر.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('البريد الإلكتروني مستخدم بالفعل. الرجاء استخدام بريد آخر.')