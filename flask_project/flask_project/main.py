from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///userapp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'User {self.id}'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable = False)
    

    def __repr__(self):
        return f'Student {self.id}'

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100))
    
    def __repr__(self):
        return f'Department {self.id}'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department  = db.Column(db.String(100))
    course_name = db.Column(db.String(100))
    teacher = db.Column(db.String(100))

    def __repr__(self,):
        return f'Course {self.id}'

class SC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_id  = db.Column(db.Integer)
    course_name = db.Column(db.String(100))

    def __repr__(self,):
        return f'SC {self.id}'

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __repr__(self,):
        return f'Teacher {self.id}'


#this is the main page
#this page sends you to the homepage
@app.route("/",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usercheck = User.query.filter_by(username=username).first()
        if usercheck:
            if usercheck.password == password:
                session['id'] = usercheck.id
                return redirect(url_for('welcome'))
        return redirect(url_for('login'))
    else:
            return render_template('login.html')



#this page sends you to the welcome page
@app.route("/home")
def index():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/students",methods = ["GET","POST"])
def students():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        new = Student(name = name, age = age)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('students'))
    all_students = Student.query.all()
    return render_template("students.html",students = all_students)

@app.route("/editstudent/<int:id>",methods = ["GET","POST"])
def edit_student(id):
    student = Student.query.get(id)
    if request.method == "POST":
        student.name = request.form['name']
        student.age = request.form['age']
        db.session.commit()
        return redirect(url_for('students'))
    students_course = SC.query.filter_by(s_id = id).all() 
    all_courses = Course.query.all()
    return render_template("studentsedit.html", student = student, courses = all_courses, s_courses = students_course )

@app.route("/editdepartment/<int:id>",methods = ["GET","POST"])
def edit_department(id):
    department = Department.query.get(id)
    if request.method == "POST":
        department.department_name = request.form['department_name']
        db.session.commit()
        return redirect(url_for('department'))
    return render_template("departmentedit.html",department = department )

@app.route("/delstudent/<int:id>")
def del_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))

@app.route("/del/<int:id1>/<int:id2>")
def del_sc(id1,id2):
    sc = SC.query.get(id2)
    db.session.delete(sc)
    db.session.commit()
    return redirect(f'/editstudent/{id1}')


@app.route("/addcourse/<int:id>",methods = ["GET","POST"])
def add_course(id):
    if request.method == "POST":
        s_id = id
        course = request.form['course']
        new = SC(s_id = s_id, course_name = course)
        db.session.add(new)
        db.session.commit()
        return redirect(f'/editstudent/{id}')

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/editinstructor/<int:id>",methods = ["GET","POST"])
def edit_instructor(id):
    instructor = Teacher.query.get(id)
    if request.method == "POST":
        instructor.department = request.form['department']
        instructor.name = request.form['name']
        db.session.commit()
        return redirect(url_for('teachers'))
    department = Department.query.all()
    return render_template("edit_Teachers.html", instructor = instructor, departments = department )

@app.route("/deleteinstructor/<int:id>")
def deleteinstructor(id):
    instructor = Teacher.query.get(id)
    db.session.delete(instructor)
    db.session.commit()
    return redirect(url_for('teachers'))

@app.route("/editcourse/<int:id>", methods = ["GET","POST"])
def editcourse(id):
    course = Course.query.get(id)
    if request.method == "POST":
        teacher = request.form['teacher']
        course.teacher = teacher
        course.course_name = request.form['course_name']
        course.department = Teacher.query.filter_by(name = teacher).first().department
        db.session.commit()
        return redirect(url_for('course'))
    all_teachers = Teacher.query.all()
    return render_template("courseedit.html",teachers = all_teachers, course = course)

@app.route("/deletecourse/<int:id>")
def deletecourse(id):
    course = Course.query.get(id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('course'))



@app.route("/teachers",methods=["GET","POST"])
def teachers():
    if request.method == "POST":
        name= request.form['name']
        department = request.form['department']
        new = Teacher(department = department, name = name)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('teachers'))
    teacher = Teacher.query.all()
    department = Department.query.all()
    return render_template("teachers.html",teachers = teacher, departments = department) 

@app.route("/department",methods=["GET","POST"])
def department():
    if request.method == "POST":
        name= request.form['department_name']
        new = Department(department_name = name)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('department'))
    department = Department.query.all()
    return render_template("department.html",departments = department)

@app.route("/course",methods=["GET","POST"])
def course():
    if request.method == "POST":
        teacher = request.form['teacher']
        course_name = request.form['course_name']
        department = Teacher.query.filter_by(name = teacher).first().department
        new_course = Course(teacher = teacher, department = department, course_name = course_name)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('course'))
    all_teachers = Teacher.query.all()
    all_courses = Course.query.all()
    return render_template("course.html",teachers = all_teachers, courses = all_courses)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)