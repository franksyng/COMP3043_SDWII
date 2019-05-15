# Server-side code here.
# If you cannot understand the code below, go to 2.Flask-Templates.

# © 2019-current,
# authors at Computer Science and Technology,
# Division of Science and Technology,
# BNU-HKBU United International College

from flask import Flask, render_template
import datetime
from flask import Flask, render_template, request, redirect,url_for
from wtforms import Form, StringField, PasswordField, SubmitField,DateField
from wtforms.validators import DataRequired
import pymysql
from flask_login import LoginManager, UserMixin,login_user,login_required,logout_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = b'_5#y2L"F4Q8zvnfxec]/'


class CalendarAdmin(UserMixin):
    """User class for flask-login"""
    def __init__(self, id):
        self.id = id
        self.name = 'admin'
        self.password = 'admin'


@login_manager.user_loader
def load_user(user_id):
    return CalendarAdmin(user_id)


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


class DataForm(Form):
    date = DateField('date', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DatabaseOperations():
    # Fill in the information of your database server.
    __db_url = 'localhost'
    __db_username = 'root'
    __db_password = ''
    __db_name = 'test'
    __db = ''

    def __init__(self):
        """Connect to database when the object is created."""
        self.__db = self.db_connect()

    def __del__(self):
        """Disconnect from database when the object is destroyed."""
        self.__db.close()

    def db_connect(self):
        self.__db = pymysql.connect(self.__db_url, self.__db_username,
                                    self.__db_password, self.__db_name)
        return self.__db

    def query_events_by_date(self, date):
        db = self.db_connect()
        cursor = db.cursor()
        sql = """SELECT event_name FROM `events` WHERE `event_id` in
        (SELECT `event_id` FROM `dates` INNER JOIN `dates_events`
        ON dates.date_id = dates_events.date_id WHERE `date` =
        str_to_date("2019-05-05","%Y-%m-%d"))"""
        cursor.execute(sql)
        temp = cursor.fetchall()
        results = set()
        for i in temp:
            results.add(i)
        return results


@app.route('/')
def index():
    # Get the current time.
    dt = datetime.datetime.now()
    # Assign the variables, convert to string.
    date = dt.strftime("%Y-%m-%d")
    # Render the template with arguments.
    return render_template('index.html', date=date)


@app.route('/login/cnmd', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.username.data == 'admin' and form.password.data == 'admin':
            # Create an object of the authorized user class.
            test_admin_user = CalendarAdmin('admin')
            # Pass the user object ot `flask-login` method `login_user()`.
            login_user(test_admin_user)
            # Exit this function by redirect to the next page.
            return redirect('./admin')
    else:
        message = 'Test username: admin, password: admin'
        return render_template('login.html', message=message)


@app.route('/query', methods=['GET', 'POST'])
def query():
    form = DataForm(request.form)
    message = ""
    results = ""
    if request.method == 'POST':
        message = str(form.date.data)
    # return render_template('query.html', date='Input a date on the right',
    # events=['Input a date on the right'])
        db = DatabaseOperations()
        results = db.query_events_by_date(message)
    return render_template('query.html', events=results, date=message)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Redirect to homepage
    return render_template('index.html')

