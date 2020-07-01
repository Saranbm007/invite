from datetime import datetime
from flask import render_template, url_for, redirect, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, InvitationForm
from app.models import User, Invitation

@app.route('/')
@app.route('/home')
@login_required
def home():
    return redirect('invitations')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/newInvitation', methods=['GET', 'POST'])
@login_required
def new_invitation():
    form = InvitationForm()
    if form.validate_on_submit():
        recipients = form.recipients.data.split(',')
        for recipient in recipients:
            receiver = User.query.filter_by(username=recipient).first()
            invitation = Invitation(
                sender=current_user, recipient=receiver,
                invitation_header=form.invitation_header.data, 
                invitation_body=form.invitation_body.data,
                invitation_footer=form.invitation_footer.data,
                accepted = True
                )
            db.session.add(invitation)
            db.session.commit()
        flash('Invitation Created')
        return redirect(url_for('home'))
    return render_template('new_invitation.html', title='New Invitation',
            form=form)
        
@app.route('/invitations')
@login_required
def invitations():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    invitations = current_user.invitations_received.filter_by(accepted=True).order_by(
        Invitation.timestamp.desc()).all()
    return render_template('home.html', title=' Invitations', invitations=invitations)

@app.route('/created_invitations')
@login_required
def created_invitations():
    invitations = current_user.invitations_sent.order_by(
        Invitation.timestamp.desc()).all()
    return render_template('home.html',title='Created Invitations', invitations=invitations, flag=1)

@app.route('/view_invitation/<invitation>')
@login_required
def view_invitation(invitation):
    invitation = Invitation.query.get(invitation)
    return render_template('view_invitation.html', title='View Invitation', invitation=invitation)

@app.route('/accept_invitation/<invitation>')
@login_required
def accept_invitation(invitation):
    invitation = Invitation.query.get(invitation)
    invitation.accepted = True
    db.session.commit()
    return redirect(url_for('invitations'))

@app.route('/reject_invitation/<invitation>')
@login_required
def reject_invitation(invitation):
    invitation = Invitation.query.get(invitation)
    invitation.accepted = False
    db.session.commit()
    return redirect(url_for('invitations'))

