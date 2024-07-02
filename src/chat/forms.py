from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm): 
    name = StringField('Benutzername', validators=[InputRequired(), Length(min=3)],
                        render_kw={"class": "form-control", "placeholder": "Benutzername"}) 
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=3)],
                            render_kw={"class": "form-control", "placeholder": "Passwort"}) 


class RegisterForm(FlaskForm):
    name = StringField('Benutzername', validators=[InputRequired(), Length(min=3)],
                        render_kw={"class": "form-control", "placeholder": "Benutzername"}) 
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=3)],
                            render_kw={"class": "form-control", "placeholder": "Passwort"}) 
    password2 = PasswordField('Passwort2', validators=[InputRequired(), Length(min=3), EqualTo("password")],
                            render_kw={"class": "form-control", "placeholder": "Passwort bestätigen"}) 
