from webapp import db

VALID_ROLES = ("student", "professor")

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), nullable=False)

    courses = db.relationship('Course', back_populates='professor', cascade='all, delete')
    enrollments = db.relationship('Enrollment', back_populates='student', cascade='all, delete')

    def set_role(self, role):
        if role not in VALID_ROLES:
            raise ValueError(f"Invalid role {role}")
        self.role = role


class Program(db.Model):
    __tablename__ = 'program'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    courses = db.relationship('Course', back_populates='program', cascade='all, delete')


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), unique=True, nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    semester = db.Column(db.Integer, nullable=False)

    professor = db.relationship('User', back_populates='courses')
    program = db.relationship('Program', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course', cascade='all, delete')


class Enrollment(db.Model):
    __tablename__ = 'enrollment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    score = db.Column(db.Float)
    letter_grade = db.Column(db.String(2))
    date_enrolled = db.Column(db.DateTime)

    student = db.relationship('User', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')
