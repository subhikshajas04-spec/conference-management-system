from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# ====================== REGISTER ======================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('auth.register'))

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

# ====================== LOGIN ======================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            session['name'] = user.name
            session['role'] = user.role
            
            flash(f'Login successful! Welcome, {user.name}! 👋', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('login.html')

# ====================== LOGOUT ======================
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))