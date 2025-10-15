from flask import Blueprint, render_template, redirect, url_for, request, flash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: Implement login logic
        flash('Login functionality is not yet implemented.', 'info')
        return redirect(url_for('main.index'))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # TODO: Implement registration logic
        flash('Registration functionality is not yet implemented.', 'info')
        return redirect(url_for('main.index'))
    return render_template('register.html')