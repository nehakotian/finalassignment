from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Connecting to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:neha@localhost/studentclass'
app.config['SECRET_KEY'] = "nrkotian"

db = SQLAlchemy(app)


# Creating student table
class Student(db.Model):  # pylint: disable=too-few-public-methods
    __tablename__ = 'student'
    student_id = db.Column('id', db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    classes = db.relationship("Classes", foreign_keys='Classes.class_leader')
    created_on = db.Column(db.DateTime(), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(), server_default=db.func.now())

    def __init__(self, student_name, class_id):
        self.student_name = student_name
        self.class_id = class_id


# Creating table classes
class Classes(db.Model):  # pylint: disable=too-few-public-methods
    __tablename__ = "classes"
    class_id = db.Column('id', db.Integer, primary_key=True)
    class_name = db.Column(db.String(100))
    student = db.relationship("Student", foreign_keys='Student.class_id')
    class_leader = db.Column(db.Integer, db.ForeignKey('student.id'))
    created_on = db.Column(db.DateTime(), default=db.func.now())
    updated_on = db.Column(db.DateTime(), default=db.func.now())

    def __init__(self, class_name):
        self.class_name = class_name


# Displays all students
@app.route('/', methods=['GET', 'POST'])
def show_all():
    return render_template('show_all.html', students=Student.query.all())


# Adds new student
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all details', 'error')
        else:
            class_leader = request.form.get("class_leader")
            if class_leader == "Yes":
                student = Student(request.form["name"],
                                  request.form['selected_id'])
                class_info = Classes.query.filter_by(class_id=request.form['selected_id']).first()
                db.session.add(student)
                db.session.commit()
                class_info.class_leader = student.student_id
                class_info.updated_on = db.func.now()

                db.session.add(class_info)

            else:
                student = Student(request.form['name'],
                                  request.form['selected_id'])
                db.session.add(student)
                db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new_student.html', class_details=Classes.query.all())


# Passes selected student's data for updating
@app.route('/update_student', methods=['post', 'get'])
def update_student():
    current_id = request.form.get("student_id")
    student_update = Student.query.filter_by(student_id=current_id).first()
    return render_template("update_student.html", student=student_update)


# Updates existing student information
@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        if not request.form['student_name'] or not request.form['student_id'] \
                or not request.form['class_id']:
            flash('Please enter all details', 'error')
        else:
            old_id = request.form['old_id']
            class_id = request.form['class_id']
            class_leader = request.form.get("class_leader")
            student_id = request.form.get("student_id")
            student_name = request.form.get("student_name")
            if class_leader == "Yes":
                class_update = Classes.query.filter_by(class_id=class_id).first()
                class_update.class_leader = request.form['student_id']
            student = Student.query.filter_by(student_id=old_id).first()
            student.student_name = student_name
            student.class_id = class_id
            student.student_id = student_id
            student.updated_on = db.func.now()
            db.session.commit()
            flash('Record was successfully updated')
            return redirect(url_for('show_all'))
    return redirect(url_for('show_all'))


# Deletes student details
@app.route("/delete", methods=["POST"])
def delete():
    student_id = request.form.get("id")
    student = Student.query.filter_by(student_id=student_id).first()
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('show_all'))
    except IntegrityError:
        flash('This student is the current class leader. Change the leader and try again.')
        return redirect(url_for('show_all'))


# Displays all the classes
@app.route("/show_class", methods=['GET', 'POST'])
def show_class():
    return render_template("show_class.html", classes=Classes.query.all())


# Adds new class
@app.route("/new_class", methods=['GET', 'POST'])
def new_class():
    if request.method == 'POST':
        if not request.form['class_name']:
            flash('Please enter name of the class', 'error')
        else:
            class_info = Classes(request.form['class_name'])
            db.session.add(class_info)
            db.session.commit()
            return redirect(url_for('show_class'))
    return render_template('new_class.html', classes=Classes.query.all())


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
