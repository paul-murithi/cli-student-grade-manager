from functools import wraps
from flask import session, redirect, url_for, flash
from webapp.models.models_file import User
from flask import abort, current_app
from flask_login import current_user
from flask import render_template, request, redirect, url_for, flash


def role_required(*roles):
    """
        Decorator to restrict access to users with specific roles.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if not current_user.is_authenticated:
                flash("Please sign in to access that page.", "warning")
                return redirect(url_for('auth.login') + f"?next={request.full_path}")

            user_role = getattr(current_user, "role", None)

            if isinstance(user_role, (list, tuple, set)):
                allowed = set(roles)
                has_role = bool(allowed & set(user_role))
            else:
                has_role = user_role in roles

            if not has_role:
                current_app.logger.warning(
                    f"Unauthorized access attempt by user {getattr(current_user, 'id', 'unknown')} with role {
                        user_role} on endpoint {request.path}"
                )
                flash(
                    'access denied. You do not have permission to view that page', 'warning')
                if user_role == 'student':
                    return redirect(url_for('dashboard.student_dashboard'))
                elif user_role == 'professor':
                    return redirect(url_for('dashboard.professor_dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
