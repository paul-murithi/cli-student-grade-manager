from flask import Blueprint, redirect, url_for, request, flash, current_app, render_template
from webapp.utils.decorators import role_required
from webapp.utils.helpers import clean_form_data, get_letter_grade
from webapp import db
from webapp.models.models_file import Enrollment
from flask_login import login_required, current_user
from datetime import datetime, timezone

grades_bp = Blueprint('grades', __name__, url_prefix='/grades')


@grades_bp.route('/add', methods=['POST'])
@login_required
@role_required('professor')
def grade_student():
    form_data = request.form
    cleaned_data = clean_form_data(form_data)
    
    cleaned_score = cleaned_data.get('score')
    student_id = cleaned_data.get('student_id')
    course_id = cleaned_data.get('course_id')

    score = 0
    letter_grade = ''

    if cleaned_score:
        score = float(cleaned_score)
        letter_grade = get_letter_grade(score)

    enrollment = db.session.query(Enrollment).filter(
        Enrollment.user_id == student_id,
        Enrollment.course_id == course_id
    ).first()

    # enrollment does not exist
    if not enrollment:
        flash('Enrollment does not exist or student already graded', 'error')
        return redirect(url_for('dashboard.professor_dashboard'))
    
    # If the student has not been graded yet - score is None
    try:
        if enrollment.score is None:
            enrollment.score = score
            enrollment.letter_grade = letter_grade if cleaned_score else None
            enrollment.date_enrolled = datetime.now(timezone.utc)
            try:
                db.session.commit()
                flash('Grade added successfully', 'success')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f'An error occurred: {e}')
        else:
            flash('Student is already graded', 'warning')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'An error occured: {e}')

    return redirect(url_for('dashboard.professor_dashboard'))

@grades_bp.route('/view', methods=['GET'])
@login_required
@role_required('student')
def view_grades():
    enrollments = db.session.query(Enrollment).filter_by(user_id=current_user.id).all()
    enrollments_list = list(enrollments) if enrollments else []
    if not enrollments_list:
        flash('No enrollments were found for this user', 'error')
        current_app.logger.error(f'No enrollments were found for this user. UserId: {current_user.id}')
        return render_template('enrollments/enrollment.html', enrollments=[])
    return render_template('enrollments/enrollment.html', enrollments=enrollments_list)