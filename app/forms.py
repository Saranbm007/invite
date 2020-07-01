from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class InvitationForm(FlaskForm):
    invitation_header = TextAreaField('Invitation Header', validators=[DataRequired()])
    invitation_body = TextAreaField('Invitation Body', validators=[DataRequired()])
    invitation_footer = TextAreaField('Invitation Footer', validators=[DataRequired()])
    recipients = StringField('Recipient', validators=[DataRequired()])
    submit = SubmitField('Create Invitation')

    def validate_recipients(self, recipients):
        recipients_ = recipients.data.split(',')
        for recipient in recipients_:
            user = User.query.filter_by(username=recipient).first()
            if user is None:
                raise ValidationError(f'{recipient} Not Found')

