import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key-123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///vault.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Encryption Initialization
encryption_key = os.environ.get('ENCRYPTION_KEY')
if not encryption_key:
    # Fallback for development only
    cipher_suite = Fernet(Fernet.generate_key())
else:
    cipher_suite = Fernet(encryption_key.encode())

# --- DATABASE MODELS ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Encrypted username - length 255 to fit encrypted string
    encrypted_username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    entries = db.relationship('Entry', backref='owner', lazy=True)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    saved_login = db.Column(db.String(255), nullable=False)
    saved_password = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- HELPER FUNCTIONS ---

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data):
    return cipher_suite.decrypt(data.encode()).decode()

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('username').strip()
        pass_word = request.form.get('password')

        # Check for existing user (must decrypt all to check)
        all_users = User.query.all()
        for u in all_users:
            if decrypt_data(u.encrypted_username) == user_name:
                flash('Username already taken!', 'danger')
                return redirect(url_for('register'))

        new_user = User(
            encrypted_username=encrypt_data(user_name),
            password_hash=generate_password_hash(pass_word, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created with encrypted identity!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        
        all_users = User.query.all()
        target_user = None
        for u in all_users:
            try:
                if decrypt_data(u.encrypted_username) == user_name:
                    target_user = u
                    break
            except: continue

        if target_user and check_password_hash(target_user.password_hash, pass_word):
            login_user(target_user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Decrypt username for display
    display_name = decrypt_data(current_user.encrypted_username)

    if request.method == 'POST':
        new_entry = Entry(
            service_name=request.form.get('service'),
            saved_login=encrypt_data(request.form.get('login')),
            saved_password=encrypt_data(request.form.get('password')),
            user_id=current_user.id
        )
        db.session.add(new_entry)
        db.session.commit()
        flash('Securely saved!', 'success')
        return redirect(url_for('dashboard'))

    # Load and decrypt entries
    user_entries = Entry.query.filter_by(user_id=current_user.id).all()
    for entry in user_entries:
        try:
            entry.saved_login = decrypt_data(entry.saved_login)
            entry.saved_password = decrypt_data(entry.saved_password)
        except:
            entry.saved_login = "Error"
            entry.saved_password = "Error"

    return render_template('dashboard.html', entries=user_entries, name=display_name)

@app.route('/delete/<int:entry_id>')
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if entry.user_id == current_user.id:
        db.session.delete(entry)
        db.session.commit()
        flash('Entry deleted.', 'info')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)