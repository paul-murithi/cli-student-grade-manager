from webapp.utils.decorators import role_required
from webapp.utils.helpers import fetch_program_id, clean_form_data, check_errors
from webapp.models.models_file import Program, Course
from webapp import db 
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

course_bp = Blueprint('course', __name__, url_prefix='/course')

@course_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required('professor')
def create_course():
    """ Module to be used by user (role='professor') to create a new course
    Keyword arguments:
    argument -- description
    Return: GET request returns the template page to add a new course
            POST request returns the template page to view the created course
    """
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
    """
    Edit a specific course by its ID (professors can only edit name and semester).
    """
    course = Course.query.get(course_id)
    if not course:
        return render_template('404.html'), 404

    # only the professor who created the course can edit it
    if course.professor_id != current_user.id:
        flash('You do not have permission to edit this course.', 'error')
        return redirect(url_for('course.view_course', course_id=course_id))

    if request.method == 'POST':
        cleaned_data = clean_form_data(request.form)
        missing_fields = []

        if not cleaned_data.get('name'):
            missing_fields.append('Name')
        if not cleaned_data.get('semester'):
            missing_fields.append('Semester')

        if missing_fields:
            flash(f"Missing or invalid fields: {', '.join(missing_fields)}", "error")
            return render_template('course/edit_course.html', course=course, form_data=cleaned_data), 400

        course.name = cleaned_data.get('name')
        course.semester = cleaned_data.get('semester')

        try:
            db.session.commit()
            flash('Course updated successfully!', 'success')
            return redirect(url_for('course.view_course', course_id=course_id))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while updating the course. Please try again.', 'error')
            return render_template('course/edit_course.html', course=course, form_data=cleaned_data), 400

    return render_template('course/edit_course.html', course=course)

@course_bp.route('/delete/<int:course_id>', methods=['POST'])
@login_required
@role_required('professor')
def delete(course_id):
    """
    Delete a specific course by its ID.

    Parameters:
        course_id (int): The ID of the course to delete.

    Returns:
        Response: A redirect to the view_all_courses page after deletion.
    """
    course = Course.query.filter_by(id=course_id).first()
    professor_id = current_user.id

    if not course:
        flash('Course not found.', 'error')
    elif course.professor_id != professor_id:
        flash('You do not have permission to delete this course.', 'error')
    else:
        db.session.delete(course)
        db.session.commit()
        flash('Course deleted successfully!', 'success')
    return redirect(url_for('course.view_all_courses'))

@course_bp.route('/view/<int:course_id>', methods=['GET'])
@login_required
@role_required('professor')
def view_course(course_id):
    """
    View a specific course by its ID.

    Parameters:
        course_id (int): The ID of the course to view.

    Returns:
        Rendered template for viewing the course details.
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return render_template('404.html'), 404
    return render_template('course/view_course.html', course=course)

@course_bp.route('/view')
@login_required
@role_required('professor')
def view_all_courses():
    """
    View all courses.
    Returns:
        Rendered template for viewing all courses
        Context:
            courses (list): List of Course objects to be displayed in the template
    """
    courses = Course.query.all()
    return render_template('course/view_all.html', courses=courses)