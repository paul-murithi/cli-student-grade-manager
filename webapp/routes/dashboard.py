from flask import Blueprint, render_template, abort, current_app, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from webapp.utils.decorators import roles_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/student')
@login_required
@roles_required('student')
def student_dashboard():
    return render_template('dashboard/student.html')

@dashboard_bp.route('/professor')
@login_required
@roles_required('professor')
def professor_dashboard():
    return render_template('dashboard/professor.html')
