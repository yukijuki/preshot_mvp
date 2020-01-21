from app import app
from flask import Flask, request, redirect, session, send_from_directory, jsonify, render_template, make_response, url_for, abort, flash
from flask_sqlalchemy import SQLAlchemy
import datetime, os, secrets
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/img'
PHISICAL_ROOT = os.path.dirname( os.path.abspath( __file__ ) )

# app.config.from_object("config.DevelopmentConfig")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "superSecret"
app.config["UPLOAD_FOLDER"] = PHISICAL_ROOT + UPLOAD_FOLDER
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 3000 * 3000

#see the img folder
#file_list = os.listdir( app.config['UPLOAD_FOLDER'] )

app.debug = True
db = SQLAlchemy(app)
# Define Models

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), unique=True)
    industry = db.Column(db.String(80))
    password = db.Column(db.Integer, default=0)
    signed_up_at = db.Column(db.DateTime())

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    filename = db.Column(db.String(255), nullable=False, unique=True, default="default.jpg")
    link = db.Column(db.String(255), nullable=False)
    faculty = db.Column(db.String(80), nullable=False)
    firm = db.Column(db.String(80), nullable=False)
    industry = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(80), nullable=False)
    lab = db.Column(db.String(80), nullable=False)
    club = db.Column(db.String(80), nullable=False)
    wagamanchi = db.Column(db.String(255), nullable=False)
    ask_clicks = db.Column(db.Integer)

class Ask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(80))
    employee_name = db.Column(db.String(80))
    industry = db.Column(db.String(80))
    position = db.Column(db.String(80))
    created_at = db.Column(db.DateTime())

#----------------------------------------------------------------
#User login
def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        if data["email"] == "":
            print("email absent")
            return redirect(url_for('register'))

        """
        data = {
            "email":"Str",
            "password" = 6,
        }
        """
        session['Email'] = data["email"]
        print(session['Email'])

        student = Student.query.filter_by(email=data["email"]).first()

        if student is None:

            newuser = Student(
            email = data["email"], 
            password = data["password"], 
            signed_up_at=datetime.datetime.now()
            )
            db.session.add(newuser)
            db.session.commit()
            flash("登録しました")
            #"account created"
            return redirect(url_for('profile'))
        
        else:
            if student.password == data["password"]:
                flash("ログインしました")
                return redirect(url_for('home'))

            else:  
                #"password is wrong"
                flash("パスワードが違います")
                return redirect(request.url)
    return render_template("register.html")

@app.route("/profile", methods=["Get", "POST"])
def profile():
    email = session.get('Email')
    if email is not None:
        print(email)
    else:
        return redirect(url_for('register'))

    student = Student.query.filter_by(email=email).first()

    if  request.method == "POST":
        data = request.get_json()
        print("check")
        print(data)

        if data["password"] == "":
            data["password"] = student.password

        if data["name"] == '':
            data["name"] = student.name

        if data["industry"] == '':
            data["industry"] = student.industry

        student.password = data["password"]
        student.name = data["name"]
        student.industry = data["industry"]
        db.session.commit()
        flash("変更されました。")


        session["Industry"] = data["industry"]

        response = make_response(jsonify(data, 200))
        return response

    return render_template("profile.html", data = student)

@app.route("/home", methods=["GET"])
def home():
    email = session.get('Email')
    if email is not None:
        print(email)
    else:
        flash("ログインしなおしてください。")
        return redirect(url_for('register'))
    
    try:        
        """
        data = {
            "faculty" = "Str",
            "firm" = "Str",
            "industry" = "Str",
            "position": "Str",
            "lab" = "Str",
            "club" = "Str",
        }
        """

        employees = Employee.query.all()

        #Sort with function
        # def sort():
        #     return employees, common

        response = []

        for employee in employees:
            employee_data = {}
            employee_data["id"] = employee.id
            employee_data["name"] = employee.name
            employee_data["filename"] = 'static/img/' + employee.filename
            employee_data["link"] = employee.link
            employee_data["firm"] = employee.firm
            employee_data["industry"] = employee.industry
            employee_data["ask_clicks"] = employee.ask_clicks
            response.append(employee_data)
        print(response)

    except FileNotFoundError:
        abort(404)

    return render_template("home.html", files = response)

@app.route("/employee/<id>", methods=["GET"])
def employee(id):
    email = session.get('Email')
    if email is not None:
        print(email)
    else:
        flash("ログインしなおしてください。")
        return redirect(url_for('register'))
    
    employee_data = {}
    try:        
        employee = Employee.query.filter_by(id=id).first()

        employee_data["id"] = employee.id
        employee_data["name"] = employee.name
        employee_data["filename"] = 'static/img/' + employee.filename
        employee_data["link"] = employee.link
        employee_data["faculty"] = employee.faculty
        employee_data["firm"] = employee.firm
        employee_data["industry"] = employee.industry
        employee_data["position"] = employee.position
        employee_data["lab"] = employee.lab
        employee_data["club"] = employee.club
        employee_data["wagamanchi"] = employee.wagamanchi
        employee_data["ask_clicks"] = employee.ask_clicks
    except FileNotFoundError:
        abort(404)
        flash("バグを運営に報告してください")

    return render_template('employee.html', file=employee_data)


@app.route("/ask_click", methods=["GET","POST"])
def ask_click():
    data = request.get_json()
    """
    data = {
        "email":"Str",
        "employee_name":"Str"
        "industry":"Str",
        "firm":"Str"
        "position":"Str",
        "lab":"Str"
        "club":"Str",
    }
    """
    employee = Employee.query.filter_by(name=data["employee_name"]).first()
    if employee.ask_clicks is None:
        employee.ask_clicks == 1
    else:
        employee.ask_clicks += 1
    asklog = Ask(
        email=data["email"], 
        employee_name=data["employee_name"], 
        industry=data["industry"], 
        position=data["position"], 
        created_at=datetime.datetime.now())

    db.session.add(asklog)
    db.session.commit()


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        print("chekc")
        if request.form:

            data = request.form
            image = request.files["image"]

            if image.filename == "":
                flash("Image must have a name")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                flash("PNG, JPG, JPEGを選んでください")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                emp_file = Employee.query.filter_by(filename=filename).first()
                if emp_file:
                    flash("ファイル名を変更してください")
                    return redirect(request.url)

                image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))

                employee = Employee(
                name = data["name"],
                filename = filename,
                link = data["link"],
                faculty = data["faculty"],
                firm = data["firm"],
                industry = data["industry"],
                position = data["position"],
                lab = data["lab"],
                club = data["club"],
                wagamanchi = data["wagamanchi"],
                ask_clicks = 0
                )

                db.session.add(employee)
                db.session.commit()
                flash("Image saved")

            return redirect(request.url)
    return render_template("upload.html")


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('register'))

@app.route("/delete/<id>", methods=['POST', "GET", "DELETE"])
def employee_delete(id):
    email = session.get('Email')
    if email == "admin@gmail.com":
        print(email)
    else:
        flash("adminに入ってください")
        return redirect(url_for('register'))

    b = Employee.query.filter_by(id=id).first()
    db.session.delete(b)
    db.session.commit()
    flash("deleted")

    return render_template("admin.html")