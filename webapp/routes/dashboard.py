from flask import Blueprint, render_template, current_app, flash
from flask_login import login_required, current_user
from webapp.utils.decorators import role_required
from webapp.models.models_file import Course, Enrollment
from webapp import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/student', methods=['GET'])
@login_required
@role_required('student')
def student_dashboard():
    """
    Displays a student's dashboard showing their enrolled courses
    and other available courses they can join
    """
    try:
        # All enrolled courses
        enrolled_courses = (
            Course.query
            .join(Enrollment, Enrollment.course_id == Course.id)
            .filter(Enrollment.user_id == current_user.id)
            .all()
        )

        enrolled_ids = {course.id for course in enrolled_courses}

        # Get not enrolled courses
        courses_to_show = Course.query.filter(~Course.id.in_(enrolled_ids)).all()

        return render_template(
            'dashboard/student.html',
            enrolled_courses=enrolled_courses,
            courses=courses_to_show
        )

    except Exception as e:
        current_app.logger.error(f"Error loading dashboard for user {current_user.id}: {e}")
        flash('Unable to load your dashboard at the moment.', 'error')
        return render_template(
            'dashboard/student.html',
            enrolled_courses=[],
            courses=[]
        )


@dashboard_bp.route('/professor')
@login_required
@role_required('professor')
def professor_dashboard():
    """
    Handles professor view on the dashboard
        1. Allows view to all students enrolled in user's courses
        2. 
    Return: enrollments page
    """
    user_id = current_user.id
    courses = Course.query.filter_by(professor_id=user_id).all()
    enrollments = Enrollment.query.filter(Enrollment.course_id.in_([c.id for c in courses])).all()

    return render_template('dashboard/professor.html', enrollments=enrollments)
