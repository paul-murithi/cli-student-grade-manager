from webapp.utils.decorators import role_required
from webapp.utils.helpers import fetch_program_id, clean_form_data, check_errors
from webapp.models.models_file import Program, Course
from webapp import db 
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

course_bp = Blueprint('course', __name__, url_prefix='/course')


@course_bp.route('/enroll', methods=['GET', 'POST'])
@login_required
@role_required('student')
def enroll():
    if request.method == 'POST':
      ...
    return render_template('course/enroll.html')

@course_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('professor')
def create_course():
    programs = Program.query.all()
    form_data = {}
    if request.method == 'POST':
        form_ = request.form
        cleaned_data = clean_form_data(form_)
        missing_fields = check_errors(cleaned_data)

        if missing_fields:
            flash(f"Missing or invalid fields: {', '.join(missing_fields)}", "error")
            return render_template('course/create_course.html', programs=programs, form_data=cleaned_data), 400
        else:
            name = cleaned_data.get('name')
            code = cleaned_data.get('code')
            program_name = cleaned_data.get('program')
            semester = cleaned_data.get('semester')
            program_id = fetch_program_id(program_name)
            professor_id = current_user.id

            try:
                new_course = Course(name=name, code=code, program_id=program_id, professor_id=professor_id, semester=semester) # pyright: ignore[reportCallIssue]
                db.session.add(new_course)
                db.session.commit()
                flash('Course created successfully!', 'success')
                return redirect(url_for('course.view_course', course_id=new_course.id))
            except IntegrityError as e:
                flash('A course with this code already exists.', 'error')
                db.session.rollback()
                return render_template('/course/create_course.html', programs=programs, form_data=cleaned_data), 400
    return render_template('course/create_course.html', programs=programs, form_data=form_data)

@course_bp.route('/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
@role_required('professor')
def edit(course_id):
    if request.method == 'POST':
        ...
        # TODO: Add course editing logic
    return render_template('course/edit_course.html', course_id=course_id)

@course_bp.route('/delete/<int:course_id>', methods=['POST'])
@login_required
@role_required('professor')
def delete(course_id):
    ...
    # TODO: Add course deletion logic
    return '', 204

@course_bp.route('/view/<int:course_id>', methods=['GET'])
@login_required
def view(course_id):
    return render_template('course/view_course.html', course_id=course_id)