from webapp.utils.decorators import role_required
from flask import Blueprint, request, render_template
from flask_login import login_required

course_bp = Blueprint('course', __name__, url_prefix='/course')


@course_bp.route('/enroll', methods=['GET', 'POST'])
@login_required
@role_required('student')
def enroll():
    if request.method == 'POST':
        ...
        # TODO:: Add course enrollment logic
    return render_template('/course/enroll.html')


@course_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('professor')
def create():
    if request.method == 'POST':
        ...
        # TODO: Add course creation logic
    return render_template('/course/create_course.html')
