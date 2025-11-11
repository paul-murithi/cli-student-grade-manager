from flask import render_template, Blueprint
from webapp.utils.decorators import role_required
from webapp.models.models_file import Course, Enrollment
from flask_login import current_user

enrollment_bp = Blueprint('enrollment', __name__, url_prefix='/enrollment')

@enrollment_bp.route('/view')
@role_required('professor')
def view_all_enrollments():
    user_id = current_user.id
    courses = Course.query.filter_by(professor_id=user_id).all()
    enrollments = Enrollment.query.filter(Enrollment.course_id.in_([c.id for c in courses])).all()

    return render_template('enrollments/enrollment.html', enrollments=enrollments)