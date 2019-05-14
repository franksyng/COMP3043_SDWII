import datetime

import pymysql
from database import DatabaseOperations
from io import BytesIO
import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import Flask, render_template, request, redirect, send_file
from flask_login import  login_required, UserMixin, login_user, logout_user,current_user,LoginManager
from wtforms import Form, StringField, PasswordField, DateField, validators,SubmitField,SelectField

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = b'UIC-Calendar-20190408'
# 连接数据库
pymysql.install_as_MySQLdb()
# The format should be mysql://username:password@localhost/test
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/udms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds =1)
db = SQLAlchemy(app)


class FileContents(db.Model):
    __tablename__ = 'file_contents'
    file_id = db.Column(db.Integer, primary_key=True)
    doc_name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_record'
    a_id = db.Column(db.BigInteger, primary_key=True)
    status = db.Column(db.Integer)

    def __init__(self, a_id, status):
        self.a_id = a_id
        self.status = status


class Attendance(db.Model):
    __tablename__ = 'attend'
    id = db.Column(db.Integer, primary_key=True)
    a_id = db.Column(db.BigInteger, primary_key=True)

    def __init__(self, udt_id, a_id):
        self.id = udt_id
        self.a_id = a_id

class User(UserMixin):
    """User class for flask-login"""

    def __init__(self, id):
        # student id
        self.id = id
        self.name = 'admin'
        self.password = 'admin'


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    db = DatabaseOperations()
    if request.method == 'POST' and form.validate():
        try:
            user_id = int(form.username.data)
            password = db.query_password(user_id)[0]
        except Exception:
            message = "你输的连王启正都看不下去了" #如果输入不合规范
            return render_template('login/login.html', message=message)
        if form.password.data == password:
            # 判断不同职位进入不同网页
            authority1 =int(db.query_authority(user_id)[0])
            if authority1 == 1: # 管理员
                admin_user = User(user_id)
                login_user(admin_user)
                return redirect('/homepage_a')

            if authority1 == 0:  # 普通用户
                student_user = User(user_id)
                login_user(student_user)
                return redirect('/homepage')
        else:
            message = password  # 真正的密码是啥
            return render_template('login/login.html', message=message)
    else:
        message = "真就登录都白给" #乱来的
        return render_template('login/login.html', message=message)


# for normal user+
@app.route('/homepage', methods=['GET', 'POST'])
@login_required
def homepage():
    userid = int(current_user.id)
    db = DatabaseOperations()
    name = db.query_name(int(userid))[0]
    # 检索数据库得到name
    #检索数据库取得公告板信息赋值给event，
    events = ("大皮今天脱单了么", "大皮你的女朋友呢？", "大皮不要总学习啦 陪陪女朋友吧","大皮什么时候请吃饭啊")
    #四个count数不同的数字 pres excu late abse
    try:
        pre = int(db.query_attendance(userid, 0)[0])
        exc = int(db.query_attendance(userid, 1)[0])
        lat = int(db.query_attendance(userid, 2)[0])
        abs = int(db.query_attendance(userid, 3)[0])
        prerate = str(pre*100/(pre+exc+lat+abs))
        excrate = str(exc*100/(pre+exc+lat+abs))
        latrate = str(lat*100/(pre+exc+lat+abs))
        absrate = str(abs*100/(pre+exc+lat+abs))
    except Exception:
        pre =0
        exc =0
        lat =0
        abs =0
        prerate = 0
        excrate = 0
        latrate = 0
        absrate = 0
    records = db.query_match_info(int(userid))
    try:
        firwin = int(db.query_position_times(userid, 1))
        secwin = int(db.query_position_times(userid, 2))
        thiwin = int(db.query_position_times(userid, 3))
        forwin = int(db.query_position_times(userid, 3))
        firrate = str(firwin * 100 / (firwin + secwin + thiwin + forwin))
        secrate = str(secwin * 100 / (firwin + secwin + thiwin + forwin))
        thirate = str(thiwin * 100 / (firwin + secwin + thiwin + forwin))
        forrate = str(forwin * 100 / (firwin + secwin + thiwin + forwin))
    except Exception:
        firrate = 0
        secrate = 0
        thirate = 0
        forrate = 0
        skilled = "none"

    temp = max(firwin,secwin,thiwin,forwin)
    if firwin == temp:
        skilled = "First"
    if secwin == temp:
        skilled = "Second"
    if thiwin == temp:
        skilled = "third"
    if forwin == temp:
        skilled = "forth"

    return render_template('homepage/homepage.html', name=name, events=events,
                           pre=pre, exc=exc, lat=lat, abs=abs, prerate=prerate,
                           excrate=excrate, latrate=latrate, absrate=absrate,records= records,
                           firrate=firrate, secrate=secrate,thirate=thirate,forrate=forrate,skilled=skilled)

#for admin 需求和上面几乎一样
@app.route('/homepage_a', methods=['GET', 'POST'])
@login_required
def homepage_a():
    userid = int(current_user.id)
    db = DatabaseOperations()
    name = db.query_name(int(userid))[0]
    #检索数据库取得公告板信息赋值给event，
    events = ("明天秃头不要迟到", "ballball you 要了老命了", "画饼一时爽一直画饼一直爽")
    #四个count数不同的数字 pres excu late abse

    try:
        pre = int(db.query_attendance(userid, 0)[0])
        exc = int(db.query_attendance(userid, 1)[0])
        lat = int(db.query_attendance(userid, 2)[0])
        abs = int(db.query_attendance(userid, 3)[0])
        prerate = str(pre*100/(pre+exc+lat+abs))
        excrate = str(exc*100/(pre+exc+lat+abs))
        latrate = str(lat*100/(pre+exc+lat+abs))
        absrate = str(abs*100/(pre+exc+lat+abs))
    except Exception:
        pre =0
        exc =0
        lat =0
        abs =0
        prerate = 0
        excrate = 0
        latrate = 0
        absrate = 0

    # 从数据库中调record

    records = db.query_match_info(int(userid))
    try:
        firwin = int(db.query_position_times(userid, 1))
        secwin = int(db.query_position_times(userid, 2))
        thiwin = int(db.query_position_times(userid, 3))
        forwin = int(db.query_position_times(userid, 3))
        firrate = str(firwin * 100 / (firwin + secwin + thiwin + forwin))
        secrate = str(secwin * 100 / (firwin + secwin + thiwin + forwin))
        thirate = str(thiwin * 100 / (firwin + secwin + thiwin + forwin))
        forrate = str(forwin * 100 / (firwin + secwin + thiwin + forwin))
    except Exception:
        firrate = 0
        secrate = 0
        thirate = 0
        forrate = 0
        skilled = "none"

    temp = max(firwin, secwin, thiwin, forwin)
    if firwin == temp:
        skilled = "First"
    if secwin == temp:
        skilled = "Second"
    if thiwin == temp:
        skilled = "third"
    if forwin == temp:
        skilled = "forth"

    return render_template('homepage/homepage_admin.html', name=name, events=events,
                           pre=pre, exc=exc, lat=lat, abs=abs, prerate=prerate,
                           excrate=excrate, latrate=latrate, absrate=absrate, records=records,
                           firrate=firrate, secrate=secrate, thirate=thirate, forrate=forrate, skilled=skilled)



@app.route('/assignment', methods=['GET', 'POST'])
@login_required
def assignment():
    #userid = current_user.id 拿到userid
    db = DatabaseOperations()
    assignment = db.query_assignment()
    # a =(("今天过大年","2019-10-31","反正随便写写就好了说的跟真的有人喜欢似的",1),
    #     ("期末考试啦啦啦","2019-11-31","你一布置我就写岂不是显得我很没面子",2))
    return render_template('assignment/assignment.html',assignments = assignment)

@app.route('/assignment_detial/<int:aid>', methods=['GET', 'POST'])
@login_required
def assignment_detail(aid):
    # 将改assignment的具体信息po出
    return render_template('./assignment/assignment_detail.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']

    new_file = FileContents(doc_name=file.filename, data=file.read())
    db.session.add(new_file)
    db.session.commit()
    # 是不是要放一个界面更好一些
    return 'Saved ' + file.filename + ' to the database!'


# here for page of admin
@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    # 数据库判断权限
    return render_template('attendance/attendance.html')


@app.route('/attendance/new/OneYear')
def attendance_new_one_year():
    data = DatabaseOperations()
    members = data.query_attendance_one_year()
    return render_template('./attendance/attendance_new.html', members=members)


@app.route('/attendance/new/TwoYears')
def attendance_new_two_years():
    data = DatabaseOperations()
    members = data.query_attendance_two_year()
    return render_template('./attendance/attendance_new.html', members=members)


@app.route('/attendance/new/OverTwo')
def attendance_new_over_two():
    data = DatabaseOperations()
    members = data.query_attendance_over_two_year()
    return render_template('./attendance/attendance_new.html', members=members)


@app.route('/attendance/new/admin')
def attendance_admin():
    data = DatabaseOperations()
    members = data.query_attendance_admin()
    return render_template('./attendance/attendance_new.html', members=members)


@app.route('/attendance/new/all')
def attendance_all():
    data = DatabaseOperations()
    members = data.query_attendance_all()
    return render_template('./attendance/attendance_new.html', members=members)


@app.route('/attendance/check', methods=['POST'])
def attendance_check():
    status_in_str = request.form['status']
    udt_id = request.form['id']

    if status_in_str == 'Present':
        status_in_int = 0
    elif status_in_str == 'Excused':
        status_in_int = 1
    elif status_in_str == 'Late':
        status_in_int = 2
    else:
        status_in_int = 3

    d = datetime.datetime.now()
    year = str(getattr(d, 'year'))
    month = str(getattr(d, 'month'))
    day = str(getattr(d, 'day'))
    hour = str(getattr(d, 'hour'))

    a_id = str(udt_id) + year + month + day + hour

    attend = Attendance(a_id=a_id, udt_id=udt_id)
    attendance_record = AttendanceRecord(status=status_in_int, a_id=a_id)
    db.session.add(attend)
    db.session.add(attendance_record)
    db.session.commit()

    # return jsonify({'result': 'success'})
    return 'Id is xx'



class dateForm(Form):
    year = StringField('year', [validators.DataRequired()])
    month = StringField('month', [validators.DataRequired()])
    day = StringField('day', [validators.DataRequired()])


@app.route('/attendance_search', methods=['GET', 'POST'])
@login_required
def attendance_search():
    # 数据库判断权限
    form = dateForm(request.form)
    # message = form.username.data
    if request.method == 'POST' and form.validate():
        if form.year.data =='1' and form.month.data == '1':
            # if it post
            # form.year form.month.form.day 确认时间并查询语句
            # 判断不同职位进入不同
            test_persons = [(1, "吴飞机","今天白给"), (2, "白给大侠","鬼知道去哪里了"), (3,"真的好累阿","约会去了"),
                            (4,"要命命","一个人的旅行")]
            return render_template('attendance/attendance_search.html', people = test_persons)
        else:
            return render_template('attendance/attendance_search.html')
    else:
        return render_template('attendance/attendance_search.html')


@app.route('/attendance_del', methods=['GET', 'POST'])
@login_required
def attendance_del():
    # 数据库判断权限
    form = dateForm(request.form)
    # message = form.username.data
    if request.method == 'POST' and form.validate():
        # if it post
        # 将form.year form.month.form.day 拼接成时间并链接数据库删除
        test_message="一点情面都不留真就把我删除呗"
        return render_template('attendance/attendance_del.html',message = test_message)
    else:
        return render_template('attendance/attendance_del.html')


@app.route('/grading', methods=['GET', 'POST'])
@login_required
def grading():
    # 数据库判断权限
    # 根据创建者id搜索作业然后进行打分的项目
    message = int(current_user.id)
    db = DatabaseOperations()
    assignment = db.query_assignment_creater(int(current_user.id))
    # a = (("今天过大年", "2019-10-31", "反正随便写写就好了说的跟真的有人喜欢似的", 1),
    #      ("期末考试啦啦啦", "2019-11-31", "你一布置我就写岂不是显得我很没面子", 2))
    return render_template('grading/grading.html',assignments = assignment,message = message)


@app.route('/grading_detail/<int:aid>')
def grading_detail(aid):
    return render_template('./grading/grading_detail.html')


@app.route('/download/<int:fid>')
def download(fid):
    file_info = FileContents.query.filter_by(file_id=fid).first()
    return send_file(BytesIO(file_info.data), attachment_filename=file_info.doc_name, as_attachment=True)


class assignmentForm(Form):
    assName = StringField('assName', [validators.DataRequired()])
    assReq = StringField('assReq', [validators.DataRequired()])
    assDate = StringField('assDate', [validators.DataRequired()])
    assTime = StringField('assTime', [validators.DataRequired()])



@app.route('/assignment_new', methods=['GET', 'POST'])
@login_required
def assignment_new():
    # 数据库判断权限
    form = assignmentForm(request.form)
    # message = form.username.data
    if request.method == 'POST':
        # 将form内的各种信息写到数据库内 并返回至list界面
        return redirect("/grading")
    else:
        return render_template('assignment/assignment_create.html')


class searchForm(Form):
    select = SelectField('select', [validators.DataRequired()])
    input = StringField('input', [validators.DataRequired()])


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = searchForm(request.form)
    if request.method == 'POST':
        message = form.select.data
        message1 = form.input.data
        db = DatabaseOperations()
        result = db.query_search(str(form.select.data), str(form.input.data))
        return render_template('search/list.html',results = result,number = len(result))

    else:
        return render_template('search/search.html')


@app.route('/search_a', methods=['GET', 'POST'])
def search_a():
    form = searchForm(request.form)
    if request.method == 'POST':

        result = (("1730026109", "qizheng", "wang", "cst"),
                  ("1730026119", "shuyang", "wu", "cst"))
        return render_template('search/list_admin.html',results = result,number=len(result))
    else:
        return render_template('search/search_admin.html')


@app.route('/information/<int:user_id>', methods=['GET', 'POST'])
def information(user_id):
    db = DatabaseOperations()
    name = db.query_name(int(user_id))[0]
    # 检索数据库取得公告板信息赋值给event，
    # 从数据库中调record
    # 数据库拿到其他信息
    records = db.query_match_info(int(user_id))
    try:
        firwin = int(db.query_position_times(user_id, 1))
        secwin = int(db.query_position_times(user_id, 2))
        thiwin = int(db.query_position_times(user_id, 3))
        forwin = int(db.query_position_times(user_id, 3))
        firrate = str(firwin * 100 / (firwin + secwin + thiwin + forwin))
        secrate = str(secwin * 100 / (firwin + secwin + thiwin + forwin))
        thirate = str(thiwin * 100 / (firwin + secwin + thiwin + forwin))
        forrate = str(forwin * 100 / (firwin + secwin + thiwin + forwin))
    except Exception:
        firrate = 0
        secrate = 0
        thirate = 0
        forrate = 0
        skilled = "none"

    temp = max(firwin, secwin, thiwin, forwin)
    if firwin == temp:
        skilled = "First"
    if secwin == temp:
        skilled = "Second"
    if thiwin == temp:
        skilled = "third"
    if forwin == temp:
        skilled = "forth"
    return render_template('/search/information.html', name=name, firrate=firrate, secrate=secrate,
                           thirate=thirate, forrate=forrate, skilled=skilled,records = records)


@app.route('/information_a/<int:user_id>', methods=['GET', 'POST'])
def information_a(user_id):
    db = DatabaseOperations()
    name = db.query_name(int(user_id))[0]
    # 检索数据库取得公告板信息赋值给event，
    # 从数据库中调record
    # 数据库拿到其他信息
    records = db.query_match_info(int(user_id))
    try:
        firwin = int(db.query_position_times(user_id, 1))
        secwin = int(db.query_position_times(user_id, 2))
        thiwin = int(db.query_position_times(user_id, 3))
        forwin = int(db.query_position_times(user_id, 3))
        firrate = str(firwin * 100 / (firwin + secwin + thiwin + forwin))
        secrate = str(secwin * 100 / (firwin + secwin + thiwin + forwin))
        thirate = str(thiwin * 100 / (firwin + secwin + thiwin + forwin))
        forrate = str(forwin * 100 / (firwin + secwin + thiwin + forwin))
    except Exception:
        firrate = 0
        secrate = 0
        thirate = 0
        forrate = 0
        skilled = "none"

    temp = max(firwin, secwin, thiwin, forwin)
    if firwin == temp:
        skilled = "First"
    if secwin == temp:
        skilled = "Second"
    if thiwin == temp:
        skilled = "third"
    if forwin == temp:
        skilled = "forth"
    return render_template('search/information_admin.html', name=name,
                           firrate=firrate, secrate=secrate, thirate=thirate, forrate=forrate,
                           skilled=skilled,records = records)


# warning page
@app.route('/authority', methods=['GET', 'POST'])
@login_required
def authority():
    return render_template('warning/authority.html')









