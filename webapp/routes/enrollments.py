from flask import render_template, Blueprint, redirect, url_for, request, flash, current_app
from webapp.utils.decorators import role_required
from webapp import db
from webapp.models.models_file import Course, Enrollment
from flask_login import current_user, login_required

enrollment_bp = Blueprint('enrollment', __name__, url_prefix='/enrollment')

@enrollment_bp.route('/view')
@login_required
@role_required('professor')
def view_all_enrollments():
    return render_template('enrollments/enrollment.html')

@enrollment_bp.route('/new', methods=['POST'])
@login_required
@role_required('student')
def enroll_to_course():
    """
    Handles student enrollment in a course.
    Validates input, prevents duplicates, and commits enrollment to the database.
    """
    course_id = request.form.get('course_id', type=int)
    if not course_id:
        flash('Invalid course ID provided.', 'error')
        return redirect(url_for('dashboard.student_dashboard'))

    selected_course = Course.query.filter_by(id=course_id).first()
    if not selected_course:
        flash('Course not found.', 'error')
        return redirect(url_for('dashboard.student_dashboard'))

    # check duplicate enrollment
    existing_enrollment = Enrollment.query.filter_by(
        user_id=current_user.id, course_id=course_id
    ).first()
    if existing_enrollment:
        flash('You are already enrolled in this course.', 'info')
        return redirect(url_for('dashboard.student_dashboard'))

    try:
        enrollment = Enrollment(course_id=course_id, user_id=current_user.id) # type: ignore
        db.session.add(enrollment)
        db.session.commit()
        flash('Successfully enrolled in the course!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error enrolling user {current_user.id} in course {course_id}: {e}")
        flash('An unexpected error occurred during enrollment.', 'error')

    return redirect(url_for('dashboard.student_dashboard'))