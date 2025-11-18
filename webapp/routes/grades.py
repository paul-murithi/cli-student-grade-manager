from flask import Blueprint, redirect, url_for, request, flash, current_app
from webapp.utils.decorators import role_required
from webapp.utils.helpers import clean_form_data, get_letter_grade
from webapp import db
from webapp.models.models_file import Enrollment
from flask_login import login_required
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

    enrollment = Enrollment.query.filter(
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