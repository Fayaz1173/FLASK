from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- APP SETUP ----------------
app = Flask(__name__)

app.config['SECRET_KEY'] = 'my-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# 🔐 SESSION CONFIG (IMPORTANT)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config['SESSION_PERMANENT'] = False  # session ends when browser closes

# 🔐 reCAPTCHA CONFIG
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE_KEY')

# 📧 MAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# ---------------- DATABASE ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

# ---------------- FORMS ----------------
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

class OTPForm(FlaskForm):
    otp = StringField('OTP', validators=[InputRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')

# ---------------- UTILS ----------------
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    try:
        msg = Message(
            'Your OTP Code',
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = f"Your OTP is: {otp}"
        mail.send(msg)
    except Exception as e:
        print("Email error:", e)

# ---------------- CACHE CONTROL ----------------
@app.after_request
def prevent_caching(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            if existing_user.is_verified:
                flash('Already registered. Login.', 'info')
                return redirect(url_for('login'))
            else:
                otp = generate_otp()
                session['otp'] = otp
                session['email'] = email
                send_otp_email(email, otp)
                return redirect(url_for('verify_otp'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        otp = generate_otp()
        session['otp'] = otp
        session['email'] = email
        send_otp_email(email, otp)

        return redirect(url_for('verify_otp'))

    return render_template('register.html', form=form)

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    form = OTPForm()

    if 'email' not in session:
        return redirect(url_for('register'))

    if form.validate_on_submit():
        if form.otp.data == session.get('otp'):
            user = User.query.filter_by(email=session['email']).first()
            user.is_verified = True
            db.session.commit()

            session.pop('otp', None)
            session.pop('email', None)

            return redirect(url_for('login'))

        flash('Invalid OTP', 'danger')

    return render_template('verify_otp.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.is_verified:
                flash('Verify your account first', 'warning')
                return redirect(url_for('login'))

            session['user_id'] = user.id
            session.permanent = True   # 🔐 enable session lifetime

            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid credentials', 'danger')

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

# ---------------- RUN ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
