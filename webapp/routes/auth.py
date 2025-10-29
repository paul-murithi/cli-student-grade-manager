from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from webapp.models.models_file import User
from webapp import db
from webapp.utils.helpers import validate_email, validate_password, validate_username
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not validate_username(username):
            flash('Invalid username', 'error')
            return redirect(url_for('auth.register'))
        if not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('auth.register'))
        if not validate_password(password):
            flash('Password is too weak or invalid', 'error')
            return redirect(url_for('auth.register'))
        
        new_user = User(name=username, email=email) # pyright: ignore[reportCallIssue]
        new_user.set_password(password)
        new_user.set_role('student')

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if 'UNIQUE constraint failed' in str(e.orig):
                flash('Username or email already exists. Please choose another.', 'error')
            else:
                flash('An error occurred, try again later!', 'error')
            return redirect(url_for('auth.register'))
        
        flash('Registration successful, you can now log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth.html', action='register')