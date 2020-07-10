import random

from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message
from flask_wtf.file import FileField, FileAllowed
import secrets
from PIL import Image
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ej6swibjsk6920bj14jdzej79hfssr63fgbs'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///little_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///big_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profile_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///picture_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pairing_data.db'

db = SQLAlchemy(app)
little_db = SQLAlchemy(app)
big_db = SQLAlchemy(app)
profile_db = SQLAlchemy(app)
picture_db = SQLAlchemy(app)
pairing_db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USER_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)
confirmed = False

def get_little_list():
    little_list = LittleData.query.all()
    names = []
    for user in little_list:
        names.append(user.name)
    little_list_names = []
    little_list_names.append(("None", "None"))
    for user in names:
        input_list = []
        input_list.append(user)
        input_list.append(user)
        input_tuple = tuple(input_list)
        little_list_names.append(input_tuple)
    return little_list_names

def restart():
    db.drop_all()
    db.create_all()
    little_db.drop_all()
    little_db.create_all()
    big_db.drop_all()
    big_db.create_all()
    profile_db.drop_all()
    profile_db.create_all()
    picture_db.drop_all()
    picture_db.create_all()
    pairing_db.drop_all()
    pairing_db.create_all()
    admin_user = User(first_name = "Admin", last_name = "Admin", username = "admin",
                      email = "admin@vt.edu", kind = "Big", password = "@admin21",
                      key = secret_function())
    db.session.add(admin_user)
    db.session.commit()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template("home.html")

def make_user():
    input_user = User(first_name = "first", last_name = "last", email = "speaks@gmail.com", username = "speaking_admin", password = "jp_speaks_admin")
    db.session.add(input_user)
    db.session.commit()

@app.route("/test", methods = ['GET', 'POST'])
def test():
    return render_template("othertest.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)
            flash('Login Successful', category="success")
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', category="danger")
            return redirect(url_for('login'))
    else:
        return render_template('login.html', title="Login", form=form)


@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        key = secret_function()
        input_user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                          username=form.username.data, password=hashed, kind = form.kind.data, key = key)
        db.session.add(input_user)
        db.session.commit()
        flash("Account Created for {}".format(form.username.data), 'success')
        return redirect(url_for('login'))
    else:
        return render_template("registration.html", form = form)

@app.route("/littleapplication", methods = ['GET', 'POST'])
@login_required
def little_apply():
    form = LittleForm()
    if form.validate_on_submit():
        '''filter the database by email, if it exists, delete that entry'''
        q = LittleData.query.filter_by(email = current_user.email).first()
        if (q is not None):
            LittleData.query.filter_by(email = current_user.email).delete()
        key = secret_function()
        input_little = LittleData(name = form.name.data, grade = form.grade.data, email = form.email.data,
                                  phone = form.phone.data, room_phone = form.room_phone.data, gender = form.gender.data,
                                  birthday = form.birthday.data, birthplace = form.birthplace.data, vt_address = form.vt_address.data,
                                  major = form.major.data, one = form.one.data, two = form.two.data, three = form.three.data,
                                  four = form.four.data, five = form.five.data, six = form.six.data, seven = form.seven.data,
                                  eight = form.eight.data, nine = form.nine.data, ten = form.ten.data, eleven = form.eleven.data,
                                  twelve = form.twelve.data, thirteen = form.thirteen.data, fourteen = form.fourteen.data, sixteen = form.sixteen.data,
                                  seventeen = form.seventeen.data, eighteen = form.eighteen.data, a_19 = form.a_19.data, b_19 = form.b_19.data,
                                  c_19 = form.c_19.data, d_19 = form.d_19.data, e_19 = form.e_19.data, f_19 = form.f_19.data, twenty = form.twenty.data,
                                  twentyone = form.twentyone.data, twentytwo = form.twentytwo.data, twentythree = form.twentythree.data, key = key)
        little_db.session.add(input_little)
        little_db.session.commit()
        flash("Saved Application for {}".format(form.name.data), 'success')
        return redirect(url_for('home'))
    else:
        '''if the current users email is in little_db, find that specific user and set the form fields to that users (credentials)'''
        q = LittleData.query.filter_by(email = current_user.email).first()
        if (q is not None):
            form.name.data = q.name
            form.grade.data = q.grade
            form.email.data = q.email
            form.phone.data = q.phone
            form.room_phone.data = q.room_phone
            form.gender.data = q.gender
            form.birthday.data = q.birthday
            form.birthplace.data = q.birthplace
            form.vt_address.data = q.vt_address
            form.major.data = q.major
            form.one.data = q.one
            form.two.data = q.two
            form.three.data = q.three
            form.four.data = q.four
            form.five.data = q.five
            form.six.data = q.six
            form.seven.data = q.seven
            form.eight.data = q.eight
            form.nine.data = q.nine
            form.ten.data = q.ten
            form.eleven.data = q.eleven
            form.twelve.data = q.twelve
            form.thirteen.data = q.thirteen
            form.fourteen.data = q.fourteen
            form.sixteen.data = q.sixteen
            form.seventeen.data = q.seventeen
            form.eighteen.data = q.eighteen
            form.a_19.data = q.a_19
            form.b_19.data = q.b_19
            form.c_19.data = q.c_19
            form.d_19.data = q.d_19
            form.e_19.data = q.e_19
            form.f_19.data = q.f_19
            form.twenty.data = q.twenty
            form.twentyone.data = q.twentyone
            form.twentytwo.data = q.twentytwo
            form.twentythree.data = q.twentythree
        return render_template("little_application.html", form = form)

@app.route("/bigapplication", methods = ['GET', 'POST'])
@login_required
def big_apply():
    form = BigForm()
    if form.validate_on_submit():
        '''filter the database by email, if it exists, delete that entry'''
        q = BigData.query.filter_by(email=current_user.email).first()
        if (q is not None):
            BigData.query.filter_by(email=current_user.email).delete()
        key = secret_function()
        input_big = BigData(name = form.name.data, grade = form.grade.data, email = form.email.data,
                            phone = form.phone.data, gender = form.gender.data, birthplace = form.birthplace.data,
                            vt_address = form.vt_address.data, major = form.major.data, one = form.one.data, two = form.two.data,
                            three = form.three.data, four = form.four.data, five = form.five.data, six = form.six.data,
                            seven = form.seven.data, eight = form.eight.data, ten = form.ten.data,
                            eleven = form.eleven.data, twelve = form.twelve.data, thirteen = form.thirteen.data,
                            fourteen = form.thirteen.data, sixteen = form.sixteen.data, fifteen = form.fifteen.data,
                            eighteen = form.eighteen.data, a_19 = form.a_19.data, b_19 = form.b_19.data, c_19 = form.c_19.data,
                            d_19 = form.d_19.data, e_19 = form.e_19.data, f_19 = form.f_19.data, twenty = form.twenty.data,
                            twentyone = form.twentyone.data, key = key)
        big_db.session.add(input_big)
        big_db.session.commit()
        flash("Saved Application for {}".format(form.name.data), 'success')
        return redirect(url_for('home'))
    else:
        '''if the current users email is in big_db, find that specific user and set the form fields to that users (credentials)'''
        q = BigData.query.filter_by(email=current_user.email).first()
        if (q is not None):
            form.name.data = q.name
            form.grade.data = q.grade
            form.email.data = q.email
            form.phone.data = q.phone
            form.gender.data = q.gender
            form.birthplace.data = q.birthplace
            form.vt_address.data = q.vt_address
            form.major.data = q.major
            form.one.data = q.one
            form.two.data = q.two
            form.three.data = q.three
            form.four.data = q.four
            form.five.data = q.five
            form.six.data = q.six
            form.seven.data = q.seven
            form.eight.data = q.eight
            form.ten.data = q.ten
            form.eleven.data = q.eleven
            form.twelve.data = q.twelve
            form.thirteen.data = q.thirteen
            form.fourteen.data = q.fourteen
            form.fifteen.data = q.fifteen
            form.sixteen.data = q.sixteen
            form.a_19.data = q.a_19
            form.b_19.data = q.b_19
            form.c_19.data = q.c_19
            form.d_19.data = q.d_19
            form.e_19.data = q.e_19
            form.f_19.data = q.f_19
            form.eighteen.data = q.eighteen
            form.twenty.data = q.twenty
            form.twentyone.data = q.twentyone
        return render_template("big_application.html", form = form)

@app.route("/bigview", methods = ['GET', 'POST'])
@login_required
def big_view():
    big_data = BigData.query.filter_by(email = current_user.email).first()
    form = BigBoxForm()
    if big_data is not None:
        form.four.data = big_data.four
        form.five.data = big_data.five
        form.six.data = big_data.six
        form.seven.data = big_data.seven
        form.eight.data = big_data.eight
        form.ten.data = big_data.ten
        form.eleven.data = big_data.eleven
        form.twelve.data = big_data.twelve
        form.thirteen.data = big_data.thirteen
        form.fourteen.data = big_data.fourteen
        form.fifteen.data = big_data.fifteen
        form.sixteen.data = big_data.sixteen
        form.eighteen.data = big_data.eighteen
        form.twenty.data = big_data.twenty
        form.twentyone.data = big_data.twentyone
    return render_template("bigview.html", big_data = big_data, form = form)

@app.route("/littleview", methods = ['GET', 'MOST'])
@login_required
def little_view():
    little_data = LittleData.query.filter_by(email = current_user.email).first()
    form = LittleBoxForm()
    if (little_data is not None):
        form.one.data = little_data.one
        form.two.data = little_data.two
        form.three.data = little_data.three
        form.four.data = little_data.four
        form.five.data = little_data.five
        form.six.data = little_data.six
        form.seven.data = little_data.seven
        form.eight.data = little_data.eight
        form.nine.data = little_data.nine
        form.ten.data = little_data.ten
        form.eleven.data = little_data.eleven
        form.twelve.data = little_data.twelve
        form.thirteen.data = little_data.thirteen
        form.fourteen.data = little_data.fourteen
        form.sixteen.data = little_data.sixteen
        form.seventeen.data = little_data.seventeen
        form.eighteen.data = little_data.eighteen
        form.twenty.data = little_data.twenty
        form.twentyone.data = little_data.twentyone
        form.twentytwo.data = little_data.twentytwo
        form.twentythree.data = little_data.twentythree
    return render_template("littleview.html", little_data = little_data, form = form)

@app.route("/bigmales", methods = ['GET', 'MOST'])
@login_required
def bigmales():
    profile_list = PicutreData.query.all()
    bigmale_list = []
    for user in profile_list:
        if str(user.gender) == str("Male") and str(user.kind) == str("Big"):
            bigmale_list.append(user)
    iterations = len(bigmale_list) // 4
    passing_list = []
    if (len(bigmale_list) % 4 is not 0):
        iterations = iterations + 1
    pin = 0
    for i in range(iterations):
        end = pin + 4
        if end > len(bigmale_list):
            end = len(bigmale_list)
        input_list = bigmale_list[pin: end]
        passing_list.append(input_list)
        pin = pin + 4
    return render_template("bigmale.html", bigmale_list = bigmale_list, passing_list = passing_list)

@app.route("/littlemales", methods = ['GET', 'POST'])
@login_required
def littlemales():
    profile_list = PicutreData.query.all()
    littlemale_list = []
    for user in profile_list:
        if str(user.gender) == str("Male") and str(user.kind) == str("Little"):
            littlemale_list.append(user)
    iterations = len(littlemale_list) // 4
    passing_list = []
    if (len(littlemale_list) % 4 is not 0):
        iterations = iterations + 1
    pin = 0
    for i in range(iterations):
        end = pin + 4
        if end > len(littlemale_list):
            end = len(littlemale_list)
        input_list = littlemale_list[pin: end]
        passing_list.append(input_list)
        pin = pin + 4
    return render_template("littlemale.html", littlemale_list=littlemale_list, passing_list=passing_list)

@app.route("/bigfemales", methods = ['GET', 'POST'])
@login_required
def bigfemales():
    profile_list = PicutreData.query.all()
    bigfemale_list = []
    for user in profile_list:
        if str(user.gender) == str("Female") and str(user.kind) == str("Big"):
            bigfemale_list.append(user)
    iterations = len(bigfemale_list) // 4
    passing_list = []
    if (len(bigfemale_list) % 4 is not 0):
        iterations = iterations + 1
    pin = 0
    for i in range(iterations):
        end = pin + 4
        if end > len(bigfemale_list):
            end = len(bigfemale_list)
        input_list = bigfemale_list[pin: end]
        passing_list.append(input_list)
        pin = pin + 4
    return render_template("bigfemale.html", bigfemale_list=bigfemale_list, passing_list=passing_list)

@app.route("/littlefemales", methods = ['GET', 'POST'])
@login_required
def littlefemales():
    profile_list = PicutreData.query.all()
    littlefemale_list = []
    for user in profile_list:
        if str(user.gender) == str("Female") and str(user.kind) == str("Little"):
            littlefemale_list.append(user)
    iterations = len(littlefemale_list) // 4
    passing_list = []
    if (len(littlefemale_list) % 4 is not 0):
        iterations = iterations + 1
    pin = 0
    for i in range(iterations):
        end = pin + 4
        if end > len(littlefemale_list):
            end = len(littlefemale_list)
        input_list = littlefemale_list[pin: end]
        passing_list.append(input_list)
        pin = pin + 4
    return render_template("littlefemale.html", littlefemale_list=littlefemale_list, passing_list=passing_list)

@app.route("/bigmaleadmin", methods = ['GET', 'POST'])
@login_required
def bigmale_admin():
    profile_list = PicutreData.query.all()
    bigmale_list = []
    for user in profile_list:
        if str(user.gender) == str("Male") and str(user.kind) == str("Big"):
            bigmale_list.append(user)
    iterations = len(bigmale_list) // 4
    passing_list = []
    if (len(bigmale_list) % 4 is not 0):
        iterations = iterations + 1
    pin = 0
    for i in range(iterations):
        end = pin + 4
        if end > len(bigmale_list):
            end = len(bigmale_list)
        input_list = bigmale_list[pin: end]
        passing_list.append(input_list)
        pin = pin + 4
    return render_template("bigmaleadmin.html", bigmale_list=bigmale_list, passing_list=passing_list)

@app.route("/bigfemaleadmin", methods = ['GET', 'POST'])
@login_required
def bigfemale_admin():
    profile_list = PicutreData.query.all()
    bigfemale_list = []
    for user in profile_list:
        if str(user.gender) == str("Female") and str(user.kind) == str("Big"):
            bigfemale_list.append(user)
    iterations = len(bigfemale_list) // 4
    passing_list = []
    if (len(bigfemale_list) % 4 is not 0):
        iterations = iterations + 1
    pin = 0
    for i in range(iterations):
        end = pin + 4
        if end > len(bigfemale_list):
            end = len(bigfemale_list)
        input_list = bigfemale_list[pin: end]
        passing_list.append(input_list)
        pin = pin + 4
    return render_template("bigfemaleadmin.html", bigfemale_list=bigfemale_list, passing_list=passing_list)

@app.route("/littlemaleadmin", methods = ['GET', 'POST'])
@login_required
def littlemale_admin():
    profile_list = PicutreData.query.all()
    littlemale_list = []
    for user in profile_list:
        if str(user.gender) == str("Male") and str(user.kind) == str("Little"):
            littlemale_list.append(user)
    iterations = len(littlemale_list) // 4
    passing_list = []
    if (len(littlemale_list) % 4 is not 0):
        iterations = iterations + 1
    pin = 0
    for i in range(iterations):
        end = pin + 4
        if end > len(littlemale_list):
            end = len(littlemale_list)
        input_list = littlemale_list[pin: end]
        passing_list.append(input_list)
        pin = pin + 4
    return render_template("littlemaleadmin.html", littlemale_list=littlemale_list, passing_list=passing_list)

@app.route("/littlefemaleadmin", methods = ['GET', 'POST'])
@login_required
def littlefemale_admin():
    profile_list = PicutreData.query.all()
    littlefemale_list = []
    for user in profile_list:
        if str(user.gender) == str("Female") and str(user.kind) == str("Little"):
            littlefemale_list.append(user)
    iterations = len(littlefemale_list) // 4
    passing_list = []
    if (len(littlefemale_list) % 4 is not 0):
        iterations = iterations + 1
    pin = 0
    for i in range(iterations):
        end = pin + 4
        if end > len(littlefemale_list):
            end = len(littlefemale_list)
        input_list = littlefemale_list[pin: end]
        passing_list.append(input_list)
        pin = pin + 4
    return render_template("littlefemaleadmin.html", littlefemale_list=littlefemale_list, passing_list=passing_list)



@app.route("/otherprofile/<string:email_string>", methods = ['GET', 'POST'])
@login_required
def other_profile(email_string):
    profile_data = ProfileData.query.filter_by(vt_email=email_string).first()
    form = TextBox()
    if (profile_data is not None):
        form.textbox.data = profile_data.bio
    picture_data = PicutreData.query.filter_by(email=email_string).first()
    return render_template("otherprofile.html", profile_data=profile_data, form=form, picture_data=picture_data, pic = picture_data.pic)

@app.route("/bigprofileall/<string:email_string>", methods = ['GET', 'POST'])
@login_required
def big_profile_all(email_string):
    big_data = BigData.query.filter_by(email = email_string).first()
    big_profile = ProfileData.query.filter_by(vt_email = email_string).first()
    form = AllBigForm()
    if big_data is not None:
        form.four.data = big_data.four
        form.five.data = big_data.five
        form.six.data = big_data.six
        form.seven.data = big_data.seven
        form.eight.data = big_data.eight
        form.ten.data = big_data.ten
        form.eleven.data = big_data.eleven
        form.twelve.data = big_data.twelve
        form.thirteen.data = big_data.thirteen
        form.fourteen.data = big_data.fourteen
        form.fifteen.data = big_data.fifteen
        form.sixteen.data = big_data.sixteen
        form.eighteen.data = big_data.eighteen
        form.twenty.data = big_data.twenty
        form.twentyone.data = big_data.twentyone
    if big_profile is not None:
        form.textbox.data = big_profile.bio
    pairing_form = PairingForm()
    if pairing_form.validate_on_submit():
        if not str(pairing_form.little_a.data) == str("None"):
            find_1 = LittleData.query.filter_by(name = pairing_form.little_a.data).first()
            input_1 = LittleData(name = find_1.name, grade = find_1.grade, email = find_1.email, phone = find_1.phone,
                                 room_phone = find_1.room_phone, gender = find_1.gender, birthday = find_1.birthday,
                                 birthplace = find_1.birthplace, vt_address = find_1.vt_address, major = find_1.major,
                                 one = find_1.one, two = find_1.two, three = find_1.three, four = find_1.four, five = find_1.five,
                                 six = find_1.six, seven = find_1.seven, eight = find_1.eight, nine = find_1.nine,
                                 ten = find_1.ten, eleven = find_1.eleven, twelve = find_1.twelve, thirteen = find_1.thirteen,
                                 fourteen = find_1.fourteen, sixteen = find_1.sixteen, seventeen = find_1.seventeen,
                                 eighteen = find_1.eighteen, a_19 = find_1.a_19, b_19 = find_1.b_19, c_19 = find_1.c_19,
                                 d_19 = find_1.d_19, e_19 = find_1.e_19, f_19 = find_1.f_19, twenty = find_1.twenty,
                                 twentyone = find_1.twentyone, twentytwo = find_1.twentytwo, twentythree = find_1.twentythree,
                                 key = find_1.key, big_key = big_data.key)
            LittleData.query.filter_by(name = pairing_form.little_a.data).delete()
            little_db.session.add(input_1)
            little_db.session.commit()
        if not str(pairing_form.little_b.data) == str("None"):
            find_2 = LittleData.query.filter_by(name = pairing_form.little_b.data).first()
            input_2 = LittleData(name = find_2.name, grade = find_2.grade, email = find_2.email, phone = find_2.phone,
                                 room_phone = find_2.room_phone, gender = find_2.gender, birthday = find_2.birthday,
                                 birthplace = find_2.birthplace, vt_address = find_2.vt_address, major = find_2.major,
                                 one = find_2.one, two = find_2.two, three = find_2.three, four = find_2.four, five = find_2.five,
                                 six = find_2.six, seven = find_2.seven, eight = find_2.eight, nine = find_2.nine,
                                 ten = find_2.ten, eleven = find_2.eleven, twelve = find_2.twelve, thirteen = find_2.thirteen,
                                 fourteen = find_2.fourteen, sixteen = find_2.sixteen, seventeen = find_2.seventeen,
                                 eighteen = find_2.eighteen, a_19 = find_2.a_19, b_19 = find_2.b_19, c_19 = find_2.c_19,
                                 d_19 = find_2.d_19, e_19 = find_2.e_19, f_19 = find_2.f_19, twenty = find_2.twenty,
                                 twentyone = find_2.twentyone, twentytwo = find_2.twentytwo, twentythree = find_2.twentythree,
                                 key = find_2.key, big_key = big_data.key)
            LittleData.query.filter_by(name = pairing_form.little_b.data).delete()
            little_db.session.add(input_2)
            little_db.session.commit()
        if not str(pairing_form.little_c.data) == str("None"):
            find_3 = LittleData.query.filter_by(name = pairing_form.little_c.data).first()
            input_3 = LittleData(name = find_3.name, grade = find_3.grade, email = find_3.email, phone = find_3.phone,
                                 room_phone = find_3.room_phone, gender = find_3.gender, birthday = find_3.birthday,
                                 birthplace = find_3.birthplace, vt_address = find_3.vt_address, major = find_3.major,
                                 one = find_3.one, two = find_3.two, three = find_3.three, four = find_3.four, five = find_3.five,
                                 six = find_3.six, seven = find_3.seven, eight = find_3.eight, nine = find_3.nine,
                                 ten = find_3.ten, eleven = find_3.eleven, twelve = find_3.twelve, thirteen = find_3.thirteen,
                                 fourteen = find_3.fourteen, sixteen = find_3.sixteen, seventeen = find_3.seventeen,
                                 eighteen = find_3.eighteen, a_19 = find_3.a_19, b_19 = find_3.b_19, c_19 = find_3.c_19,
                                 d_19 = find_3.d_19, e_19 = find_3.e_19, f_19 = find_3.f_19, twenty = find_3.twenty,
                                 twentyone = find_3.twentyone, twentytwo = find_3.twentytwo, twentythree = find_3.twentythree,
                                 key = find_3.key, big_key = big_data.key)
            LittleData.query.filter_by(name = pairing_form.little_c.data).delete()
            little_db.session.add(input_3)
            little_db.session.commit()
        b = PairingData.query.filter_by(pairing_key = big_data.key).first()
        if (b is not None):
            PairingData.query.filter_by(pairing_key = big_data.key).delete()
        input_pair = PairingData(big_email = big_data.email, little_email_one = LittleData.query.filter_by(name = pairing_form.little_a.data).first().email,
                                 little_email_two = LittleData.query.filter_by(name = pairing_form.little_b.data).first().email,
                                 little_email_three = LittleData.query.filter_by(name = pairing_form.little_c.data).first().email,
                                 pairing_key = secret_function())
        pairing_db.session.add(input_pair)
        pairing_db.session.commit()
        flash("Saved Pairing", "success")
        return redirect(url_for("admin_home"))
    else:
        q = PairingData.query.filter_by(pairing_key = big_data.key).first()
        if q is not None:
            if LittleData.query.filter_by(email=q.little_email_one).first() is not None:
                pairing_form.little_a.data = LittleData.query.filter_by(email = q.little_email_one).first().name
            if LittleData.query.filter_by(email = q.little_email_two).first() is not None:
                pairing_form.little_b.data = LittleData.query.filter_by(email = q.little_email_two).first().name
            if LittleData.query.filter_by(email = q.little_email_three).first() is not None:
                pairing_form.little_c.data = LittleData.query.filter_by(email = q.little_email_three).first().name
        return render_template("bigprofileall.html", form = form, big_data = big_data, profile_data = big_profile, pairing_form = pairing_form)

@app.route("/littleprofileall/<string:email_string>", methods = ['GET', 'POST'])
@login_required
def little_profile_all(email_string):
    little_data = LittleData.query.filter_by(email = email_string).first()
    little_profile = ProfileData.query.filter_by(vt_email = email_string).first()
    form = AllLittleForm()
    if little_data is not None:
        form.one.data = little_data.one
        form.two.data = little_data.two
        form.three.data = little_data.three
        form.four.data = little_data.four
        form.five.data = little_data.five
        form.six.data = little_data.six
        form.seven.data = little_data.seven
        form.eight.data = little_data.eight
        form.nine.data = little_data.nine
        form.ten.data = little_data.ten
        form.eleven.data = little_data.eleven
        form.twelve.data = little_data.twelve
        form.thirteen.data = little_data.thirteen
        form.fourteen.data = little_data.fourteen
        form.sixteen.data = little_data.sixteen
        form.seventeen.data = little_data.seventeen
        form.eighteen.data = little_data.eighteen
        form.twenty.data = little_data.twenty
        form.twentyone.data = little_data.twentyone
        form.twentytwo.data = little_data.twentytwo
        form.twentythree.data = little_data.twentythree
    if little_profile is not None:
        form.textbox.data = little_profile.bio
    return render_template("littleprofileall.html", form = form, little_data = little_data, profile_data = little_profile)


def secret_function():
    characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r' ,'s','t', 'u', 'v', 'w', 'x', 'y', 'z',
                  '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    start = ""
    for i in range(8):
        n = random.randint(0, len(characters) - 1)
        start = "{}{}".format(start, characters[n])
    return start

def save_picture(form_picture):
    random_hex = secret_function()
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = "{}{}".format(random_hex, f_ext)
    picture_path = os.path.join(app.root_path, 'static/assets/img', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/modifyprofile", methods = ['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        q = ProfileData.query.filter_by(vt_email=current_user.email).first()
        if q is not None:
            ProfileData.query.filter_by(vt_email = current_user.email).delete()
        key = secret_function()
        input_profile = ProfileData(name = form.name.data, username = form.username.data, bio = form.bio.data,
                                    instagram = form.instagram.data, twitter = form.twitter.data, snapchat = form.snapchat.data,
                                    vt_email = form.vt_email.data, kind = form.kind.data, gender = form.gender.data, key = key)
        profile_db.session.add(input_profile)
        profile_db.session.commit()
        flash("Updated Profile", 'success')
        return redirect(url_for("home"))
    else:
        q = ProfileData.query.filter_by(vt_email=current_user.email).first()
        if (q is not None):
            form.name.data = q.name
            form.username.data = q.username
            form.bio.data = q.bio
            form.instagram.data = q.instagram
            form.twitter.data = q.twitter
            form.snapchat.data = q.snapchat
            form.vt_email.data = q.vt_email
            form.kind.data = q.kind
            form.gender.data = q.gender
        return render_template("profile.html", form = form)

@app.route("/viewprofile", methods = ['GET', 'POST'])
@login_required
def view_profile():
    profile_data = ProfileData.query.filter_by(vt_email = current_user.email).first()
    form = TextBox()
    if (profile_data is not None):
        form.textbox.data = profile_data.bio
    picture_data = PicutreData.query.filter_by(email = current_user.email).first()
    return render_template("viewprofile.html", profile_data = profile_data, form = form, picture_data = picture_data)

@app.route("/updatepicture", methods = ['GET', 'POST'])
@login_required
def update_picture():
    form = UpdatePicture()
    if form.validate_on_submit():
        quest = ProfileData.query.filter_by(vt_email = current_user.email).first()
        if (quest is None):
            flash("Complete the Profile Form first to update your profile picture", "danger")
            return redirect(url_for("profile"))
        elif (quest.vt_email is None):
            flash("Enter your VT Email in the Profile form to update your profile pic", "danger")
            return (redirect(url_for("profile")))
        else:
            q = PicutreData.query.filter_by(email = current_user.email).first()
            if q is not None:
                PicutreData.query.filter_by(email = current_user.email).delete()
            key = secret_function()
            email = current_user.email
            pic = save_picture(form.picture.data)
            kind = quest.kind
            gender = quest.gender
            enter = PicutreData(key = key, email = email, kind = kind,
                                gender = gender, pic = pic, name = quest.name)
            picture_db.session.add(enter)
            picture_db.session.commit()
            flash("Successful Picture Change", 'success')
            return redirect(url_for("update_picture"))
    else:
        return render_template("updatepicture.html", form = form)

@app.route("/adminlogin", methods = ['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if str(form.email.data) == str("admin@vt.edu") and str(form.password.data) == str("@admin21"):
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user)
            flash("Successful admin login", "success")
            return redirect(url_for("admin_home"))
        else:
            flash("Incorrect credentials", "danger")
            return redirect(url_for("admin_login"))
    else:
        return render_template("adminlogin.html", form = form)

@app.route("/adminhome", methods = ['GET', 'POST'])
def admin_home():
    return render_template("adminhome.html")

@app.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out", "success")
    return (redirect(url_for("home")))

class AllBigForm(FlaskForm):
    four = TextAreaField("What extracurricular activities are you currently involved in?",
                         validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    five = TextAreaField("What are your favorite movies/TV shows?", validators=[Length(min=0, max=1000)],
                         render_kw={"rows": 5, "cols": 0})
    six = TextAreaField("What is your favorite song/artist/music genre?", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    seven = TextAreaField("What are your hobbies and talents", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    eight = TextAreaField("What is your biggest pet peeve?", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    ten = TextAreaField("What is your favorite YouTube video?", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    eleven = TextAreaField("What would you do with $1,000", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    twelve = TextAreaField("If you had a drink named after you, what would be in it and why?",
                           validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    thirteen = TextAreaField("What is your dream job/passion?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    fourteen = TextAreaField("What qualities do you look for in a friend?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    fifteen = TextAreaField("Are you a morning or night person?", validators=[Length(min=0, max=1000)],
                            render_kw={"rows": 5, "cols": 0})
    sixteen = TextAreaField("What is your guilty pleasure?", validators=[Length(min=0, max=1000)],
                            render_kw={"rows": 5, "cols": 0})
    eighteen = TextAreaField("Why do you want a little?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    twenty = TextAreaField("What does being a big mean to you?", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    twentyone = TextAreaField("Is there anything else you want to share about yourself?",
                              validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    textbox = TextAreaField("", render_kw={"rows": 5, "cols": 0})

class AllLittleForm(FlaskForm):
    one = TextAreaField("Do you have any preference for an Ate [female Big] or a Kuya [male Big]?",
                        validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    two = TextAreaField("What is/are your favorite food(s)/drink(s)", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    three = TextAreaField("Do you have any allergies?", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    four = TextAreaField("Do you prefer to hang out in big groups or small groups?",
                         validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    five = TextAreaField("What extracurricular activities are you currently involved in?",
                         validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    six = TextAreaField("What are your favorite movies/TV shows?", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    seven = TextAreaField("What is your favorite song/artist/music genre?", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    eight = TextAreaField("What are your hobbies and talents?", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    nine = TextAreaField("What is your biggest pet peeve?", validators=[Length(min=0, max=1000)],
                         render_kw={"rows": 5, "cols": 0})
    ten = TextAreaField("What is your favorite YouTube video?", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    eleven = TextAreaField("What would you do with $1,000?", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    twelve = TextAreaField("What is your dream job/passion?", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    thirteen = TextAreaField("If you had a drink named after you, what would be in it?",
                             validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    fourteen = TextAreaField("What qualities do you look for in a friend?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    sixteen = TextAreaField("What is your favorite color?", validators=[Length(min=0, max=1000)],
                            render_kw={"rows": 5, "cols": 0})
    seventeen = TextAreaField("Are you a morning or night person?", validators=[Length(min=0, max=1000)],
                              render_kw={"rows": 5, "cols": 0})
    eighteen = TextAreaField("What is your guilty pleasure?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    twenty = TextAreaField("Why do you want an Ate/Kuya", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    twentyone = TextAreaField("What is your class schedule? Include location/room numbers and class",
                              validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    twentytwo = TextAreaField("Is there anything else you want to share about yourself?",
                              validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    twentythree = TextAreaField("Provide a message to your future big!", validators=[Length(min=0, max=1000)],
                                render_kw={"rows": 5, "cols": 0})
    textbox = TextAreaField("", render_kw={"rows": 5, "cols": 0})

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired(), Length(min = 2, max = 30)])
    last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 2, max = 30)])
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 30)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    kind = SelectField('Applicant', validators = [DataRequired()], choices = [("Select", "Select"), ("Big", "Big"), ("Little", "Little")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email_string = User.query.filter_by(email = email.data).first()
        if email_string:
            raise ValidationError('That email is taken. Please choose a different one.')

class AdminLoginForm(FlaskForm):
    email_correct = "admin@vt.edu"
    password_correct = "@admin21"
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField('Login')

class LittleForm(FlaskForm):
    name = StringField("Name", validators = [Length(min = 0, max = 100)])
    grade = SelectField("Grade", validators = [Length(min = 0, max = 100)], choices = [("Select", "Select"), ("Freshmen", "Freshmen"), ("Sophomore", "Sophomore"), ("Junior", "Junior"), ("Senior", "Senior"), ("Super Senior", "Super Senior")])
    email = StringField("Email", validators = [Email()])
    phone = StringField("Phone Number", validators = [Length(min = 0, max = 20)])
    room_phone = StringField("Roommate's Phone", validators = [Length(min = 0, max = 20)])
    gender = SelectField("Gender", validators = [Length(min = 0, max = 100)], choices = [("Select", "Select"), ("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    birthday = StringField("Birthday", validators = [Length(min = 0, max = 30)])
    birthplace = StringField("Birthplace/Hometown", validators = [Length(min = 0, max = 100)])
    vt_address = StringField("VT Address", validators = [Length(min = 0, max = 150)])
    major = StringField("Major(s)/Minor(s)", validators = [Length(min = 0, max = 200)])
    one = TextAreaField("Do you have any preference for an Ate [female Big] or a Kuya [male Big]?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    two = TextAreaField("What is/are your favorite food(s)/drink(s)", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    three = TextAreaField("Do you have any allergies?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    four = TextAreaField("Do you prefer to hang out in big groups or small groups?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    five = TextAreaField("What extracurricular activities are you currently involved in?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    six = TextAreaField("What are your favorite movies/TV shows?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    seven = TextAreaField("What is your favorite song/artist/music genre?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    eight = TextAreaField("What are your hobbies and talents?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    nine = TextAreaField("What is your biggest pet peeve?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    ten = TextAreaField("What is your favorite YouTube video?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    eleven = TextAreaField("What would you do with $1,000?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    twelve = TextAreaField("What is your dream job/passion?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    thirteen = TextAreaField("If you had a drink named after you, what would be in it?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    fourteen = TextAreaField("What qualities do you look for in a friend?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    sixteen = TextAreaField("What is your favorite color?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    seventeen = TextAreaField("Are you a morning or night person?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    eighteen = TextAreaField("What is your guilty pleasure?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    a_19 = SelectField("1", validators = [Length(min = 0, max = 50)], choices = [("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"), ("Play videogames", "Play videogames"), ("Going out on the weekend", "Going out on the weekend"), ("Workout/Play sports", "Workout/Play sports"), ("Hang out and chills", "Hang out and chills")])
    b_19 = SelectField("2", validators = [Length(min = 0, max = 50)], choices = [("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"), ("Play videogames", "Play videogames"), ("Going out on the weekend", "Going out on the weekend"), ("Workout/Play sports", "Workout/Play sports"), ("Hang out and chills", "Hang out and chills")])
    c_19 = SelectField("3", validators = [Length(min = 0, max = 50)], choices = [("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"), ("Play videogames", "Play videogames"), ("Going out on the weekend", "Going out on the weekend"), ("Workout/Play sports", "Workout/Play sports"), ("Hang out and chills", "Hang out and chills")])
    d_19 = SelectField("4", validators = [Length(min = 0, max = 50)], choices = [("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"), ("Play videogames", "Play videogames"), ("Going out on the weekend", "Going out on the weekend"), ("Workout/Play sports", "Workout/Play sports"), ("Hang out and chills", "Hang out and chills")])
    e_19 = SelectField("5", validators = [Length(min = 0, max = 50)], choices = [("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"), ("Play videogames", "Play videogames"), ("Going out on the weekend", "Going out on the weekend"), ("Workout/Play sports", "Workout/Play sports"), ("Hang out and chills", "Hang out and chills")])
    f_19 = SelectField("6", validators = [Length(min = 0, max = 50)], choices = [("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"), ("Play videogames", "Play videogames"), ("Going out on the weekend", "Going out on the weekend"), ("Workout/Play sports", "Workout/Play sports"), ("Hang out and chills", "Hang out and chills")])
    twenty = TextAreaField("Why do you want an Ate/Kuya", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    twentyone = TextAreaField("What is your class schedule? Include location/room numbers and class", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    twentytwo = TextAreaField("Is there anything else you want to share about yourself?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    twentythree = TextAreaField("Provide a message to your future big!", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    submit = SubmitField("Save and/or Submit")

class BigForm(FlaskForm):
    name = StringField("Name", validators=[Length(min = 0, max=100)])
    grade = SelectField("Grade", validators=[Length(min = 0, max=100)],
                        choices=[("Select", "Select"), ("Freshmen", "Freshmen"), ("Sophomore", "Sophomore"),
                                 ("Junior", "Junior"), ("Senior", "Senior"), ("Super Senior", "Super Senior")])
    email = StringField("Email", validators=[Email()])
    phone = StringField("Phone Number", validators=[Length(min=0, max=20)])
    gender = SelectField("Gender", validators=[Length(min = 0, max=100)],
                         choices=[("Select", "Select"), ("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    birthplace = StringField("Birthplace/Hometown", validators=[Length(min = 0, max=100)])
    vt_address = StringField("VT Address", validators=[Length(min = 0, max=150)])
    major = StringField("Major(s)/Minor(s)", validators=[Length(min = 0, max=200)])
    one = SelectField("Do you have any gender preference for a male or female little?", validators = [Length(min = 0, max = 50)], choices = [("Select", "Select"), ("Male", "Male"), ("Female", "Female"), ("None", "None")])
    two = SelectField("Do you mind having more than one little?", validators = [Length(min = 0, max = 100)], choices = [("Select", "Select"), ("Yes", "Yes"), ("No", "No")])
    three = SelectField("Do you prefer to hang out in big groups or small groups", validators = [Length(min = 0, max = 100)], choices = [("Select", "Select"), ("Big groups", "Big groups"), ("Small groups", "Small groups")])
    four = TextAreaField("What extracurricular activities are you currently involved in?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    five = TextAreaField("What are your favorite movies/TV shows?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    six = TextAreaField("What is your favorite song/artist/music genre?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    seven = TextAreaField("What are your hobbies and talents", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    eight = TextAreaField("What is your biggest pet peeve?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    ten = TextAreaField("What is your favorite YouTube video?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    eleven = TextAreaField("What would you do with $1,000", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    twelve = TextAreaField("If you had a drink named after you, what would be in it and why?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    thirteen = TextAreaField("What is your dream job/passion?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    fourteen = TextAreaField("What qualities do you look for in a friend?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    fifteen = TextAreaField("Are you a morning or night person?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    sixteen = TextAreaField("What is your guilty pleasure?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    a_19 = SelectField("1", validators=[Length(min=2, max=50)],
                       choices=[("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"),
                                ("Play videogames", "Play videogames"),
                                ("Going out on the weekend", "Going out on the weekend"),
                                ("Workout/Play sports", "Workout/Play sports"),
                                ("Hang out and chills", "Hang out and chills")])
    b_19 = SelectField("2", validators=[Length(min=2, max=50)],
                       choices=[("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"),
                                ("Play videogames", "Play videogames"),
                                ("Going out on the weekend", "Going out on the weekend"),
                                ("Workout/Play sports", "Workout/Play sports"),
                                ("Hang out and chills", "Hang out and chills")])
    c_19 = SelectField("3", validators=[Length(min=2, max=50)],
                       choices=[("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"),
                                ("Play videogames", "Play videogames"),
                                ("Going out on the weekend", "Going out on the weekend"),
                                ("Workout/Play sports", "Workout/Play sports"),
                                ("Hang out and chills", "Hang out and chills")])
    d_19 = SelectField("4", validators=[Length(min=2, max=50)],
                       choices=[("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"),
                                ("Play videogames", "Play videogames"),
                                ("Going out on the weekend", "Going out on the weekend"),
                                ("Workout/Play sports", "Workout/Play sports"),
                                ("Hang out and chills", "Hang out and chills")])
    e_19 = SelectField("5", validators=[Length(min=2, max=50)],
                       choices=[("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"),
                                ("Play videogames", "Play videogames"),
                                ("Going out on the weekend", "Going out on the weekend"),
                                ("Workout/Play sports", "Workout/Play sports"),
                                ("Hang out and chills", "Hang out and chills")])
    f_19 = SelectField("6", validators=[Length(min=2, max=50)],
                       choices=[("Select", "Select"), ("Have lunch/dinner", "Have lunch/dinner"), ("Do homework", "Do homework"),
                                ("Play videogames", "Play videogames"),
                                ("Going out on the weekend", "Going out on the weekend"),
                                ("Workout/Play sports", "Workout/Play sports"),
                                ("Hang out and chills", "Hang out and chills")])
    eighteen = TextAreaField("Why do you want a little?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    twenty = TextAreaField("What does being a big mean to you?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    twentyone = TextAreaField("Is there anything else you want to share about yourself?", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    submit = SubmitField("Save and/or Submit")

class BigBoxForm(FlaskForm):
    four = TextAreaField("What extracurricular activities are you currently involved in?",
                         validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    five = TextAreaField("What are your favorite movies/TV shows?", validators=[Length(min=0, max=1000)],
                         render_kw={"rows": 5, "cols": 0})
    six = TextAreaField("What is your favorite song/artist/music genre?", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    seven = TextAreaField("What are your hobbies and talents", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    eight = TextAreaField("What is your biggest pet peeve?", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    ten = TextAreaField("What is your favorite YouTube video?", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    eleven = TextAreaField("What would you do with $1,000", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    twelve = TextAreaField("If you had a drink named after you, what would be in it and why?",
                           validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    thirteen = TextAreaField("What is your dream job/passion?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    fourteen = TextAreaField("What qualities do you look for in a friend?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    fifteen = TextAreaField("Are you a morning or night person?", validators=[Length(min=0, max=1000)],
                            render_kw={"rows": 5, "cols": 0})
    sixteen = TextAreaField("What is your guilty pleasure?", validators=[Length(min=0, max=1000)],
                            render_kw={"rows": 5, "cols": 0})
    eighteen = TextAreaField("Why do you want a little?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    twenty = TextAreaField("What does being a big mean to you?", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    twentyone = TextAreaField("Is there anything else you want to share about yourself?",
                              validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})

class LittleBoxForm(FlaskForm):
    one = TextAreaField("Do you have any preference for an Ate [female Big] or a Kuya [male Big]?",
                        validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    two = TextAreaField("What is/are your favorite food(s)/drink(s)", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    three = TextAreaField("Do you have any allergies?", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    four = TextAreaField("Do you prefer to hang out in big groups or small groups?",
                         validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    five = TextAreaField("What extracurricular activities are you currently involved in?",
                         validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    six = TextAreaField("What are your favorite movies/TV shows?", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    seven = TextAreaField("What is your favorite song/artist/music genre?", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    eight = TextAreaField("What are your hobbies and talents?", validators=[Length(min=0, max=1000)],
                          render_kw={"rows": 5, "cols": 0})
    nine = TextAreaField("What is your biggest pet peeve?", validators=[Length(min=0, max=1000)],
                         render_kw={"rows": 5, "cols": 0})
    ten = TextAreaField("What is your favorite YouTube video?", validators=[Length(min=0, max=1000)],
                        render_kw={"rows": 5, "cols": 0})
    eleven = TextAreaField("What would you do with $1,000?", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    twelve = TextAreaField("What is your dream job/passion?", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    thirteen = TextAreaField("If you had a drink named after you, what would be in it?",
                             validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    fourteen = TextAreaField("What qualities do you look for in a friend?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    sixteen = TextAreaField("What is your favorite color?", validators=[Length(min=0, max=1000)],
                            render_kw={"rows": 5, "cols": 0})
    seventeen = TextAreaField("Are you a morning or night person?", validators=[Length(min=0, max=1000)],
                              render_kw={"rows": 5, "cols": 0})
    eighteen = TextAreaField("What is your guilty pleasure?", validators=[Length(min=0, max=1000)],
                             render_kw={"rows": 5, "cols": 0})
    twenty = TextAreaField("Why do you want an Ate/Kuya", validators=[Length(min=0, max=1000)],
                           render_kw={"rows": 5, "cols": 0})
    twentyone = TextAreaField("What is your class schedule? Include location/room numbers and class",
                              validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    twentytwo = TextAreaField("Is there anything else you want to share about yourself?",
                              validators=[Length(min=0, max=1000)], render_kw={"rows": 5, "cols": 0})
    twentythree = TextAreaField("Provide a message to your future big!", validators=[Length(min=0, max=1000)],
                                render_kw={"rows": 5, "cols": 0})

class ProfileForm(FlaskForm):
    name = StringField("Name", validators = [Length(min = 0, max = 50)])
    username = StringField("Username", validators = [Length(min = 0, max = 50)])
    bio = TextAreaField("Tell us about yourself", validators = [Length(min = 0, max = 1000)], render_kw={"rows": 5, "cols": 0})
    instagram = StringField("Instagram", validators = [Length(min = 0, max = 50)])
    twitter = StringField("Twitter", validators=[Length(min=0, max=50)])
    snapchat = StringField("Snapchat", validators = [Length(min = 0, max = 50)])
    vt_email = StringField("Email", validators = [Length(min = 0, max = 50)])
    kind = SelectField('Applicant', validators=[DataRequired()],
                       choices=[("Select", "Select"), ("Big", "Big"), ("Little", "Little")])
    gender = SelectField("Gender (will not be part of public profile)", validators = [Length(min = 0, max = 100)], choices = [("Select", "Select"), ("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    submit = SubmitField("Save and/or Submit")


class TextBox(FlaskForm):
    textbox = TextAreaField("", render_kw={"rows": 5, "cols": 0})

class UpdatePicture(FlaskForm):
    picture = FileField("Update Profile Picture", validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(20))
    email = db.Column(db.String(120))
    kind = db.Column(db.String(120))
    password = db.Column(db.String(60))
    key = db.Column(db.String(128))

    def __repr__(self):
        return "User({}, {}, {}, {}, {})".format(self.first_name, self.last_name, self.username, self.email, self.kind)

    '''new'''
    def get_reset_token(self, expires_sec = 3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class LittleData(little_db.Model):
    id = little_db.Column(little_db.Integer, primary_key = True)
    name = little_db.Column(little_db.String(50))
    grade = little_db.Column(little_db.String(25))
    email = little_db.Column(little_db.String(120), unique = True)
    phone = little_db.Column(little_db.String(20))
    room_phone = little_db.Column(little_db.String(20))
    gender = little_db.Column(little_db.String(20))
    birthday = little_db.Column(little_db.String(30))
    birthplace = little_db.Column(little_db.String(100))
    vt_address = little_db.Column(little_db.String(150))
    major = little_db.Column(little_db.String(200))
    one = little_db.Column(little_db.String(1000))
    two = little_db.Column(little_db.String(1000))
    three = little_db.Column(little_db.String(1000))
    four = little_db.Column(little_db.String(1000))
    five = little_db.Column(little_db.String(1000))
    six = little_db.Column(little_db.String(1000))
    seven = little_db.Column(little_db.String(1000))
    eight = little_db.Column(little_db.String(1000))
    nine = little_db.Column(little_db.String(1000))
    ten = little_db.Column(little_db.String(1000))
    eleven = little_db.Column(little_db.String(1000))
    twelve = little_db.Column(little_db.String(1000))
    thirteen = little_db.Column(little_db.String(1000))
    fourteen = little_db.Column(little_db.String(1000))
    sixteen = little_db.Column(little_db.String(1000))
    seventeen = little_db.Column(little_db.String(1000))
    eighteen = little_db.Column(little_db.String(1000))
    a_19 = little_db.Column(little_db.String(1000))
    b_19 = little_db.Column(little_db.String(1000))
    c_19 = little_db.Column(little_db.String(1000))
    d_19 = little_db.Column(little_db.String(1000))
    e_19 = little_db.Column(little_db.String(1000))
    f_19 = little_db.Column(little_db.String(1000))
    twenty = little_db.Column(little_db.String(1000))
    twentyone = little_db.Column(little_db.String(1000))
    twentytwo = little_db.Column(little_db.String(1000))
    twentythree = little_db.Column(little_db.String(1000))
    key = little_db.Column(little_db.String(128))
    big_key = little_db.Column(little_db.String(16))

class BigData(big_db.Model):
    id = big_db.Column(big_db.Integer, primary_key = True)
    name = big_db.Column(big_db.String(50))
    grade = big_db.Column(big_db.String(25))
    email = big_db.Column(big_db.String(120), unique = True)
    phone = big_db.Column(big_db.String(20))
    gender = big_db.Column(big_db.String(20))
    birthplace = big_db.Column(big_db.String(100))
    vt_address = big_db.Column(big_db.String(150))
    major = big_db.Column(big_db.String(200))
    one = big_db.Column(big_db.String(1000))
    two = big_db.Column(big_db.String(1000))
    three = big_db.Column(big_db.String(1000))
    four = big_db.Column(big_db.String(1000))
    five = big_db.Column(big_db.String(1000))
    six = big_db.Column(big_db.String(1000))
    seven = big_db.Column(big_db.String(1000))
    eight = big_db.Column(big_db.String(1000))
    ten = big_db.Column(big_db.String(1000))
    eleven = big_db.Column(big_db.String(1000))
    twelve = big_db.Column(big_db.String(1000))
    thirteen = big_db.Column(big_db.String(1000))
    fourteen = big_db.Column(big_db.String(1000))
    sixteen = big_db.Column(big_db.String(1000))
    fifteen = big_db.Column(big_db.String(1000))
    eighteen = big_db.Column(big_db.String(1000))
    a_19 = big_db.Column(big_db.String(1000))
    b_19 = big_db.Column(big_db.String(1000))
    c_19 = big_db.Column(big_db.String(1000))
    d_19 = big_db.Column(big_db.String(1000))
    e_19 = big_db.Column(big_db.String(1000))
    f_19 = big_db.Column(big_db.String(1000))
    twenty = big_db.Column(big_db.String(1000))
    twentyone = big_db.Column(big_db.String(1000))
    key = big_db.Column(big_db.String(128))

class ProfileData(profile_db.Model):
    id = profile_db.Column(profile_db.Integer, primary_key=True)
    name = profile_db.Column(profile_db.String(50))
    username = profile_db.Column(profile_db.String(50))
    bio = profile_db.Column(profile_db.String(1000))
    instagram = profile_db.Column(profile_db.String(50))
    twitter = profile_db.Column(profile_db.String(50))
    snapchat = profile_db.Column(profile_db.String(50))
    vt_email = profile_db.Column(profile_db.String(50))
    kind = profile_db.Column(profile_db.String(50))
    gender = profile_db.Column(profile_db.String(100))
    key = profile_db.Column(profile_db.String(128))

    def __repr__(self):
        return "{}, {}, {}, {}".format(self.name, self.gender, self.kind, self.vt_email)

class PicutreData(picture_db.Model):
    id = picture_db.Column(picture_db.Integer, primary_key = True)
    key = picture_db.Column(picture_db.String(128))
    email = picture_db.Column(picture_db.String(50))
    kind = picture_db.Column(picture_db.String(50))
    gender = picture_db.Column(picture_db.String(100))
    pic = picture_db.Column(picture_db.String(500))
    name = picture_db.Column(picture_db.String(50))

    def __repr__(self):
        return "Picture({}, {}, {}, {})".format(self.email, self.kind, self.gender, self.pic)

class PairingData(pairing_db.Model):
    id = pairing_db.Column(pairing_db.Integer, primary_key = True)
    big_email = pairing_db.Column(pairing_db.String(50))
    little_email_one = pairing_db.Column(pairing_db.String(50))
    little_email_two = pairing_db.Column(pairing_db.String(50))
    little_email_three = pairing_db.Column(pairing_db.String(50))
    pairing_key = pairing_db.Column(pairing_db.String(16))

class PairingForm(FlaskForm):
    little_a = SelectField("Little A", choices = get_little_list())
    little_b = SelectField("Little B", choices = get_little_list())
    little_c = SelectField("Little C", choices = get_little_list())
    submit = SubmitField("Save/Submit Pairing")



if __name__ == '__main__':
    app.run(debug = True)

