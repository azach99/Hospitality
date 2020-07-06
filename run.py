from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message
import secrets
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ej6swibjsk6920bj14jdzej79hfssr63fgbs'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///little_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///big_data.db'
db = SQLAlchemy(app)
little_db = SQLAlchemy(app)
big_db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USER_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)
confirmed = False






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
        input_user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                          username=form.username.data, password=hashed)
        db.session.add(input_user)
        db.session.commit()
        flash("Account Created for {}".format(form.username.data), 'success')
        return redirect(url_for('login'))
    else:
        return render_template("registration.html", form = form)

@app.route("/littleapplication", methods = ['GET', 'POST'])
def little_apply():
    form = LittleForm()
    if form.validate_on_submit():
        '''filter the database by email, if it exists, delete that entry'''
        q = LittleData.query.filter_by(email = current_user.email).first()
        if (q is not None):
            LittleData.query.filter_by(email = current_user.email).delete()
        input_little = LittleData(name = form.name.data, grade = form.grade.data, email = form.email.data,
                                  phone = form.phone.data, room_phone = form.room_phone.data, gender = form.gender.data,
                                  birthday = form.birthday.data, birthplace = form.birthplace.data, vt_address = form.vt_address.data,
                                  major = form.major.data, one = form.one.data, two = form.two.data, three = form.three.data,
                                  four = form.four.data, five = form.five.data, six = form.six.data, seven = form.seven.data,
                                  eight = form.eight.data, nine = form.nine.data, ten = form.ten.data, eleven = form.eleven.data,
                                  twelve = form.twelve.data, thirteen = form.thirteen.data, fourteen = form.fourteen.data, sixteen = form.sixteen.data,
                                  seventeen = form.seventeen.data, eighteen = form.eighteen.data, a_19 = form.a_19.data, b_19 = form.b_19.data,
                                  c_19 = form.c_19.data, d_19 = form.d_19.data, e_19 = form.e_19.data, f_19 = form.f_19.data, twenty = form.twenty.data,
                                  twentyone = form.twentyone.data, twentytwo = form.twentytwo.data, twentythree = form.twentythree.data)
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
def big_apply():
    form = BigForm()
    if form.validate_on_submit():
        flash("Saved Application for {}".format(form.name.data), 'success')
        return redirect(url_for('home'))
    else:
        '''if the current users email is in big_db, find that specific user and set the form fields to that users (credentials)'''
        return render_template("big_application.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out", "success")
    return (redirect(url_for("home")))



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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(20))
    email = db.Column(db.String(120))
    kind = db.Column(db.String(120))
    password = db.Column(db.String(60))

    def __repr__(self):
        return "User({}, {}, {}, {})".format(self.first_name, self.last_name, self.username, self.email)

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
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    grade = db.Column(db.String(25))
    email = db.Column(db.String(120), unique = True)
    phone = db.Column(db.String(20))
    room_phone = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    birthday = db.Column(db.String(30))
    birthplace = db.Column(db.String(100))
    vt_address = db.Column(db.String(150))
    major = db.Column(db.String(200))
    one = db.Column(db.String(1000))
    two = db.Column(db.String(1000))
    three = db.Column(db.String(1000))
    four = db.Column(db.String(1000))
    five = db.Column(db.String(1000))
    six = db.Column(db.String(1000))
    seven = db.Column(db.String(1000))
    eight = db.Column(db.String(1000))
    nine = db.Column(db.String(1000))
    ten = db.Column(db.String(1000))
    eleven = db.Column(db.String(1000))
    twelve = db.Column(db.String(1000))
    thirteen = db.Column(db.String(1000))
    fourteen = db.Column(db.String(1000))
    sixteen = db.Column(db.String(1000))
    seventeen = db.Column(db.String(1000))
    eighteen = db.Column(db.String(1000))
    a_19 = db.Column(db.String(1000))
    b_19 = db.Column(db.String(1000))
    c_19 = db.Column(db.String(1000))
    d_19 = db.Column(db.String(1000))
    e_19 = db.Column(db.String(1000))
    f_19 = db.Column(db.String(1000))
    twenty = db.Column(db.String(1000))
    twentyone = db.Column(db.String(1000))
    twentytwo = db.Column(db.String(1000))
    twentythree = db.Column(db.String(1000))

class BigData(big_db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    grade = db.Column(db.String(25))
    email = db.Column(db.String(120), unique = True)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    birthplace = db.Column(db.String(100))
    vt_address = db.Column(db.String(150))
    major = db.Column(db.String(200))
    one = db.Column(db.String(1000))
    two = db.Column(db.String(1000))
    three = db.Column(db.String(1000))
    four = db.Column(db.String(1000))
    five = db.Column(db.String(1000))
    six = db.Column(db.String(1000))
    seven = db.Column(db.String(1000))
    eight = db.Column(db.String(1000))
    ten = db.Column(db.String(1000))
    eleven = db.Column(db.String(1000))
    twelve = db.Column(db.String(1000))
    thirteen = db.Column(db.String(1000))
    fourteen = db.Column(db.String(1000))
    sixteen = db.Column(db.String(1000))
    fifteen = db.Column(db.String(1000))
    eighteen = db.Column(db.String(1000))
    a_19 = db.Column(db.String(1000))
    b_19 = db.Column(db.String(1000))
    c_19 = db.Column(db.String(1000))
    d_19 = db.Column(db.String(1000))
    e_19 = db.Column(db.String(1000))
    f_19 = db.Column(db.String(1000))
    twenty = db.Column(db.String(1000))
    twentyone = db.Column(db.String(1000))







if __name__ == '__main__':
    app.run(debug = True)

