from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, DateField, IntegerRangeField, FieldList, FormField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class LoginForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Iniciar sesion')

class ExperienceForm(FlaskForm):
    Company = StringField('Nombre de la Empresa', validators=[DataRequired(), Length(max=120)]) 
    Position = StringField('Position', validators=[DataRequired()])
    start_date = DateField('Fecha de inicio', validators= [DataRequired()])
    end_date = DateField('Fecha final')
    description = TextAreaField('Descripcion', validators= [DataRequired(), Length(max=500)])

class EducationForm(FlaskForm):
    institution = StringField('Institucion', validators=[DataRequired(), Length(max=120)]) 
    degree = StringField('Titulo', validators=[DataRequired()])
    start_date = DateField('Fecha de inicio', validators= [DataRequired()])
    end_date = DateField('Fecha final')
    description = TextAreaField('Descripcion', validators= [DataRequired(), Length(max=500)])

class SkillForm (FlaskForm):
    name = StringField('Nombre de la Habilidad', validators=[DataRequired(), Length(max=60)])
    level = IntegerRangeField('Nivel de Rango', default=0, validators=[DataRequired()])


class CVForm(FlaskForm):
    full_name = StringField('Nombre Completo', validators=[DataRequired(), Length(max=64)]) 
    title = StringField('Titulo', validators=[DataRequired(), Length(64)])
    about_me = TextAreaField('Acerca de ti', validators= [DataRequired(), Length(max=250)])
    experience = FieldList(FormField(ExperienceForm))
    education = FieldList(FormField(EducationForm))
    skills = FieldList(FormField(SkillForm))
    submit = SubmitField('Registrar')
