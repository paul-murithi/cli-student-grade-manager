from flask import Blueprint, render_template, redirect, url_for, request, flash

grades_bp = Blueprint('grades', __name__, url_prefix='/grades')

@grades_bp.route('/')
def dashboard():
    return render_template('grades/dashboard.html')