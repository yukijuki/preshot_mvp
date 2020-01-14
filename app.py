# from app.tasks import create_image_set
from flask import Flask, request, redirect, session, send_from_directory, jsonify, render_template, make_response, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import datetime, os, secrets
from werkzeug.utils import secure_filename

app = Flask(__name__)
# app.config.from_object("config.DevelopmentConfig")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "superSecret"
app.config["IMAGE_UPLOADS"] = "C:\\Users\\yukij\\Desktop\\Preshot\\static\\img"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

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
    name = db.Column(db.String(80), nullable=False, unique=True)
    filename = db.Column(db.String(255), nullable=False, unique=True, default="default.jpg")
    link = db.Column(db.String(255), nullable=False)
    faculty = db.Column(db.String(80), nullable=False)
    firm = db.Column(db.String(80), nullable=False)
    industry = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(80), nullable=False)
    lab = db.Column(db.String(80), nullable=False)
    club = db.Column(db.String(80), nullable=False)
    wagamanchi = db.Column(db.String(255), nullable=False)
    ask_clicks = db.Column(db.Integer, default=0)

class Ask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(80))
    employee_name = db.Column(db.String(80))
    industry = db.Column(db.String(80))
    position = db.Column(db.String(80))
    created_at = db.Column(db.DateTime())

#----------------------------------------------------------------
# db.drop_all()
# db.create_all()
# db.session.commit()
#User login
def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/")
def index():
    filename = "human.jpeg"
    return render_template("home.html", image_name = filename)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        print(data)

        """
        data = {
            "email":"Str",
            "password" = 6,
        }
        """
        session['Email'] = data["email"]
        print(session['Email'])

        student = Student.query.filter_by(email=data["email"]).first()
        print(student)

        if student is None:

            newuser = Student(
            email = data["email"], 
            password = data["password"], 
            signed_up_at=datetime.datetime.now()
            )
            db.session.add(newuser)
            db.session.commit()
            print("signed up")
            #"account created"
            return redirect(url_for('profile'))
        
        else:
            if student.password == data["password"]:
                print("logged in")
                return redirect(url_for('home'))

            else:  
                #"password is wrong"
                print("password wrong")
                return redirect(request.url)
    return render_template("register.html")

@app.route("/profile", methods=["Get", "POST"])
def profile():
    email = session.get('Email')
    if email is not None:
        print(email)
    else:
        print("no session data stored")
        print(email)
        return redirect(url_for('register'))

    student = Student.query.filter_by(email=email).first()

    if  request.method == "POST":
        data = request.get_json()
        print("check")
        print(data)

        if data["password"] == "":
            print("PASSWORD stay the same")
            data["password"] = student.password
            print(data["password"])

        if data["name"] == '':
            print("name stay the same")
            data["name"] = student.name
            print(data["name"])

        if data["industry"] == '':
            print("industry stay the same")
            data["industry"] = student.industry

        student.password = data["password"]
        student.name = data["name"]
        student.industry = data["industry"]
        db.session.commit()

        session["Industry"] = data["industry"]

        response = make_response(jsonify(data, 200))
        return response

    return render_template("profile.html", data = student)

# @app.route("/home", methods=["GET"])
# def home():

#     try:        
#         """
#         data = {
#             "faculty" = "Str",
#             "firm" = "Str",
#             "industry" = "Str",
#             "position": "Str",
#             "lab" = "Str",
#             "club" = "Str",
#         }
#         """

#         employees = Employee.query.all()

#         #Sort with function
#         # def sort():
#         #     return employees, common

#         response = []

#         for emplyee in employees:
#             employee_data = {}
#             employee_data["name"] = Employee.name
#             employee_data["filename"] = Employee.filename
#             employee_data["link"] = Employee.link
#             employee_data["faculty"] = Employee.faculty
#             employee_data["firm"] = Employee.firm
#             employee_data["industry"] = Employee.industry
#             employee_data["position"] = Employee.position
#             employee_data["lab"] = Employee.lab
#             employee_data["club"] = Employee.club
#             employee_data["wagamanchi"] = Employee.wagamanchi
#             employee_data["ask_clicks"] = Employee.ask_clicks
#             response.append(employee_data)

#         return send_from_directory(app.config["IMAGE_UPLOADS"], filename=filename as_attachment= False)

#     except FileNotFoundError:
#         abort(404)

#     return render_template("home.html", data = response)


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
        if request.files:
            data = request.form

            if allowed_image_filesize(request.cookies.get("filesize")) == False:
                print("file exceeded max size")
                return redirect(request.url)

            image = request.files["image"]

            if image.filename == "":
                print("Image must have a name")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("extension not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                print(filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

            print("image saved")
            return redirect(request.url)
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)