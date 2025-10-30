from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from webapp.models.models_file import User
from webapp import db
from webapp.utils.helpers import validate_email, validate_password, validate_username
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        errors = []

        if not validate_username(name):
            errors.append('Invalid username')
        if not validate_email(email):
            errors.append('Invalid email format')
        if not validate_password(password):
            errors.append('Password is too weak or invalid')

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('auth.register'))

        new_user = User(name=name, email=email) # pyright: ignore[reportCallIssue]
        new_user.set_password(password)
        new_user.set_role('student')

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if 'UNIQUE constraint failed' in str(e.orig):
                error_msg = str(e.orig)
                if 'user.name' in error_msg:
                    flash('Username already exists. Please choose another.', 'error')
                elif 'user.email' in error_msg:
                    flash('Email already exists. Please choose another.', 'error')
                else:
                    flash('Username or email already exists. Please choose another.', 'error')
                return render_template('auth.html', action='register', name=name, email=email)
            else:
                flash('An error occurred, try again later!', 'error')
                return redirect(url_for('auth.register'))        
        flash('Registration successful, you can now log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth.html', action='register')