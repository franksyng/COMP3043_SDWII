import pymysql, datetime
from database import DatabaseOperations
from io import BytesIO
from sqlalchemy import and_, func
from flask_sqlalchemy import SQLAlchemy, Pagination
from datetime import timedelta
from flask import Flask, render_template, request, redirect, send_file, jsonify, url_for
from flask_login import login_required, UserMixin, login_user, logout_user, current_user, LoginManager
from wtforms import Form, StringField, PasswordField, DateField, validators, SubmitField, SelectField

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='/'
app.secret_key = b'UIC-Calendar-20190408'
# 连接数据库
pymysql.install_as_MySQLdb()
# The format should be mysql://username:password@localhost/test
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/udms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
db = SQLAlchemy(app)


class Amatch(db.Model):
    __tablename__ = 'amatch'
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_name = db.Column(db.String(30))
    date = db.Column(db.Date)
    win = db.Column(db.Integer)
    side = db.Column(db.Integer)
    opponent = db.Column(db.String(30))


class Assignment(db.Model):
    __tablename__ = 'assignment'
    a_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_date = db.Column(db.DateTime)
    title = db.Column(db.String(30))
    detail = db.Column(db.Text)
    dueDate = db.Column(db.Date)
    dueTime = db.Column(db.Time)


class Attendance(db.Model):
    __tablename__ = 'attend'
    id = db.Column(db.Integer)
    attend_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    m_id = db.Column(db.Integer)


class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_record'
    attend_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)


# A member belongs to a user group
class PermissionGroup(db.Model):
    __tablename__ = 'belong_to'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    group_id = db.Column(db.Integer)


class Creator(db.Model):
    __tablename__ = 'creator'
    a_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)


class FileContents(db.Model):
    __tablename__ = 'file_contents'
    file_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    doc_name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


class HasMatch(db.Model):
    __tablename__ = 'has'
    id = db.Column(db.Integer, primary_key=True)
    r_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer)


# Entity to record meeting information
class MeetingInfo(db.Model):
    __tablename__ = 'meeting'
    m_id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(20))


class Own(db.Model):
    __tablename__ = 'own'
    id = db.Column(db.Integer, primary_key=True)
    info_id = db.Column(db.Integer)


class PersonalInfo(db.Model):
    __tablename__ = 'personal_information'
    info_id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(5))
    major = db.Column(db.String(20))
    last_name = db.Column(db.String(20))


class MatchRecord(db.Model):
    __tablename__ = 'record'
    r_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position = db.Column(db.Integer)
    is_mvp = db.Column(db.Integer)


class Submission(db.Model):
    __tablename__ = 'submission'
    a_id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.BigInteger, primary_key=True)


class Submit(db.Model):
    __tablename__ = 'submit'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.BigInteger, primary_key=True)
    file_grade = db.Column(db.String(3))


class UserTB(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    password = db.Column(db.String(16))
    name = db.Column(db.String(20))


class UserGroup(db.Model):
    __tablename__ = 'user_group'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(15))


class User(UserMixin):
    """User class for flask-login"""

    def __init__(self, id):
        # student id
        self.id = id
        self.name = 'admin'
        self.password = 'admin'


class DateForm(Form):
    year = StringField('year', [validators.DataRequired()])
    month = StringField('month', [validators.DataRequired()])
    day = StringField('day', [validators.DataRequired()])


class AssignmentForm(Form):
    assName = StringField('assName', [validators.DataRequired()])
    assReq = StringField('assReq', [validators.DataRequired()])
    assDate = StringField('assDate', [validators.DataRequired()])
    assTime = StringField('assTime', [validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


class ChangepwdForm(Form):
    oldpwd = StringField('origin_pwd', [validators.DataRequired()])
    newpwd = StringField('new_pwd', [validators.DataRequired()])


class SearchForm(Form):
    select = SelectField('select', [validators.DataRequired()])
    input = StringField('input', [validators.DataRequired()])


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    db = DatabaseOperations()
    if request.method == 'POST' and form.validate():
        try:
            user_id = int(form.username.data)
            password = db.query_password(user_id)[0]
        except Exception:
            message = "Invalid input"  # 如果输入不合规范
            return render_template('login/login.html', message=message)
        if form.password.data == password:
            # 判断不同职位进入不同网页
            authority1 = int(db.query_authority(user_id)[0])
            if authority1 == 1: # 管理员
                admin_user = User(user_id)
                login_user(admin_user)
                return redirect('/homepage_a')

            if authority1 == 0:  # 普通用户
                student_user = User(user_id)
                login_user(student_user)
                return redirect('/homepage')
        else:
            message = "Wrong password"  # 真正的密码是啥
            return render_template('login/login.html', message=message)
    else:
        message = "Welcome"  # 乱来的
        return render_template('login/login.html', message=message)


# for ordinary user to change pwd
@app.route('/change_pwd', methods=['GET', 'POST'])
def change_pwd():
    # form = ChangepwdForm(request.form)
    dbs = DatabaseOperations()
    userid = int(current_user.id)
    name = dbs.query_name(int(userid))[0]
    if request.method == 'POST':
        try:
            password = dbs.query_password(int(current_user.id))[0]
        except Exception:
            message = "Invalid format"  # 如果输入不合规范
            return render_template('homepage/change_pwd.html', message=message, name=name)
        # 白给成功允许修改
        if request.values.get("origin_pwd") == password:
            dbs.update_password(int(current_user.id),request.values.get("new_pwd"))
            return redirect('/')
        else:
            message = "Wrong password"
            return render_template('homepage/change_pwd.html', message=request.values.get("new_pwd"), name=name)
    else:
        message = ""
        return render_template('homepage/change_pwd.html',message =request.values.get("new_pwd"), name=name)


# for admin to change pwd
@app.route('/change_pwd_admin', methods=['POST', 'GET'])
@login_required
def change_pwd_admin():
    # form = ChangepwdForm(request.form)
    dbs = DatabaseOperations()
    userid = int(current_user.id)
    name = dbs.query_name(int(userid))[0]
    if not int(dbs.query_authority(int(current_user.id))[0]):
        return redirect("/authority")
    if request.method == 'POST':
        try:
            password = dbs.query_password(int(current_user.id))[0]
        except Exception:
            message = "Invalid format"  # 如果输入不合规范
            return render_template('homepage/change_pwd_admin.html', message=message, name=name)
        # 白给成功允许修改
        if request.values.get("origin_pwd") == password:
            dbs.update_password(int(current_user.id), request.values.get("new_pwd"))
            return redirect('/')
        else:
            message = "Wrong password"
            return render_template('homepage/change_pwd_admin.html', message=request.values.get("new_pwd"), name=name)
    else:
        message = ""
        return render_template('homepage/change_pwd_admin.html', message=request.values.get("new_pwd"), name=name)


# for admin to change notice
@app.route('/change_notice', methods=['GET', 'POST'])
def change_notice():
    dbs = DatabaseOperations()
    userid = int(current_user.id)
    name = dbs.query_name(int(userid))[0]
    if request.method == 'POST':
        list1=request.values.get("board").split("\r\n")
        dbs.drop_notice()
        dbs.creat_notice()
        for i in list1:
            dbs.insert_notice(i)
        # return render_template('homepage/homepage_admin.html', message=list1)
        return redirect('/homepage_a')
    else:
        # events = dbs.query_notice()
        # string = ""
        # for i in events:
        #     string = string +str(i) +"\r\n"
        return render_template('homepage/change_notice.html', name=name)


# for normal user+
@app.route('/homepage', methods=['GET', 'POST'])
@login_required
def homepage():
    db_sql = DatabaseOperations()
    userid = int(current_user.id)
    name = db_sql.query_name(int(userid))[0]
    page = request.values.get('page', 1, type=int)
    winning_rate = 0
    mvp_rate = 0
    events = db_sql.query_notice()
    # 检索数据库得到name
    # 检索数据库取得公告板信息赋值给event，
    # events = ("大皮今天脱单了么", "大皮你的女朋友呢？", "大皮不要总学习啦 陪陪女朋友吧","大皮什么时候请吃饭啊")
    # 四个count数不同的数字 pres excu late abse
    try:
        pre = int(db_sql.query_attendance(userid, 0)[0])
        exc = int(db_sql.query_attendance(userid, 1)[0])
        lat = int(db_sql.query_attendance(userid, 2)[0])
        abs = int(db_sql.query_attendance(userid, 3)[0])
        prerate = str(pre*100/(pre+exc+lat+abs))
        excrate = str(exc*100/(pre+exc+lat+abs))
        latrate = str(lat*100/(pre+exc+lat+abs))
        absrate = str(abs*100/(pre+exc+lat+abs))
    except Exception:
        pre = 0
        exc = 0
        lat = 0
        abs = 0
        prerate = 0
        excrate = 0
        latrate = 0
        absrate = 0

    # Query match record from database and do pagination
    records = db.session.query(Amatch, HasMatch, MatchRecord, UserTB).join\
        (HasMatch, and_(Amatch.match_id == HasMatch.match_id)).join(MatchRecord, and_\
        (HasMatch.r_id == MatchRecord.r_id)).join(UserTB, and_(HasMatch.id == UserTB.id)).\
        filter(UserTB.id.like('%' + str(userid) + '%')).order_by(Amatch.date.desc())

    pagination = records.paginate(page=page, per_page=5, error_out=False)
    results = pagination.items

    try:
        firwin = int(db_sql.query_position_times(userid, 1))
        secwin = int(db_sql.query_position_times(userid, 2))
        thiwin = int(db_sql.query_position_times(userid, 3))
        forwin = int(db_sql.query_position_times(userid, 4))
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
    elif secwin == temp:
        skilled = "Second"
    elif thiwin == temp:
        skilled = "third"
    elif forwin == temp:
        skilled = "forth"
    else:
        skilled = ""

    return render_template('homepage/homepage.html', name=name, events=events, member_id=userid,
                           pre=pre, exc=exc, lat=lat, abs=abs, prerate=prerate,
                           excrate=excrate, latrate=latrate, absrate=absrate, pagination=pagination, results=results,
                           firrate=firrate, secrate=secrate, thirate=thirate, forrate=forrate, skilled=skilled)


@app.route('/detail_records')
def detail_records():
    db_sql = DatabaseOperations()
    userid = int(current_user.id)
    name = db_sql.query_name(int(userid))[0]
    page = request.values.get('page', 1, type=int)
    winning_rate = 0
    mvp_rate = 0

    # Query match record from database and do pagination
    records = db.session.query(Amatch, HasMatch, MatchRecord, UserTB).join\
        (HasMatch, and_(Amatch.match_id == HasMatch.match_id)).join(MatchRecord, and_\
        (HasMatch.r_id == MatchRecord.r_id)).join(UserTB, and_(HasMatch.id == UserTB.id)).\
        filter(UserTB.id.like('%' + str(userid) + '%')).order_by(Amatch.date.desc())

    win_num = db.session.query(Amatch, HasMatch, MatchRecord, UserTB).join(HasMatch, and_\
        (Amatch.match_id == HasMatch.match_id)).join(MatchRecord, and_(HasMatch.r_id == MatchRecord.r_id)).\
        join(UserTB, and_(HasMatch.id == UserTB.id)).filter(UserTB.id.like('%' + str(userid) + '%'), Amatch.win == 1).count()

    mvp_num = db.session.query(Amatch, HasMatch, MatchRecord, UserTB).join(HasMatch, and_\
        (Amatch.match_id == HasMatch.match_id)).join(MatchRecord, and_(HasMatch.r_id == MatchRecord.r_id)).\
        join(UserTB, and_(HasMatch.id == UserTB.id)).filter(UserTB.id.like('%' + str(userid) + '%'), MatchRecord.is_mvp == 1).count()

    record_num = records.count()

    if winning_rate != 0:
        winning_rate = request.values.get('winning_rate')
    else:
        winning_rate = format(win_num / record_num, '.2%')

    if mvp_rate != 0:
        mvp_rate = request.values.get('mvp_rate')
    else:
        mvp_rate = format(mvp_num / record_num, '.2%')

    pagination = records.paginate(page=page, per_page=5, error_out=False)
    results = pagination.items

    return render_template('homepage/detail_records.html', pagination=pagination, results=results,
                           member_id=userid, name=name, mvp_rate=mvp_rate, winning_rate=winning_rate, record_num=record_num)


# for admin 需求和上面几乎一样
@app.route('/homepage_a', methods=['GET', 'POST'])
@login_required
def homepage_a():
    userid = int(current_user.id)
    db_sql = DatabaseOperations()
    if not int(db_sql.query_authority(int(current_user.id))[0]):
        return redirect("/authority")
    name = db_sql.query_name(int(userid))[0]
    page = request.values.get('page', 1, type=int)
    # 检索数据库取得公告板信息赋值给event，
    # events = ("明天秃头不要迟到", "ballball you 要了老命了", "画饼一时爽一直画饼一直爽")
    # 四个count数不同的数字 pres excu late abse
    events = db_sql.query_notice()
    try:
        pre = int(db_sql.query_attendance(userid, 0)[0])
        exc = int(db_sql.query_attendance(userid, 1)[0])
        lat = int(db_sql.query_attendance(userid, 2)[0])
        abs = int(db_sql.query_attendance(userid, 3)[0])
        prerate = str(pre*100/(pre+exc+lat+abs))
        excrate = str(exc*100/(pre+exc+lat+abs))
        latrate = str(lat*100/(pre+exc+lat+abs))
        absrate = str(abs*100/(pre+exc+lat+abs))
    except Exception:
        pre = 0
        exc = 0
        lat = 0
        abs = 0
        prerate = 0
        excrate = 0
        latrate = 0
        absrate = 0

    try:
        firwin = int(db_sql.query_position_times(userid, 1))
        secwin = int(db_sql.query_position_times(userid, 2))
        thiwin = int(db_sql.query_position_times(userid, 3))
        forwin = int(db_sql.query_position_times(userid, 4))
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
    elif secwin == temp:
        skilled = "Second"
    elif thiwin == temp:
        skilled = "third"
    elif forwin == temp:
        skilled = "forth"
    else:
        skilled = ""

    # Query match record from database and do pagination
    records = db.session.query(Amatch, HasMatch, MatchRecord, UserTB).join\
        (HasMatch, and_(Amatch.match_id == HasMatch.match_id)).join(MatchRecord, and_\
        (HasMatch.r_id == MatchRecord.r_id)).join(UserTB, and_(HasMatch.id == UserTB.id)).\
        filter(UserTB.id.like('%' + str(userid) + '%')).order_by(Amatch.date.desc())

    pagination = records.paginate(page=page, per_page=5, error_out=False)
    results = pagination.items




    return render_template('homepage/homepage_admin.html', name=name, events=events, results=results,
                           pre=pre, exc=exc, lat=lat, abs=abs, prerate=prerate, pagination=pagination,
                           excrate=excrate, latrate=latrate, absrate=absrate, records=records, member_id=userid,
                           firrate=firrate, secrate=secrate, thirate=thirate, forrate=forrate, skilled=skilled)


@app.route('/detail_records_admin')
def detail_records_admin():
    db_sql = DatabaseOperations()
    userid = int(current_user.id)
    name = db_sql.query_name(int(userid))[0]
    page = request.values.get('page', 1, type=int)
    winning_rate = 0
    mvp_rate = 0

    # Query match record from database and do pagination
    records = db.session.query(Amatch, HasMatch, MatchRecord, UserTB).join \
        (HasMatch, and_(Amatch.match_id == HasMatch.match_id)).join(MatchRecord, and_ \
        (HasMatch.r_id == MatchRecord.r_id)).join(UserTB, and_(HasMatch.id == UserTB.id)). \
        filter(UserTB.id.like('%' + str(userid) + '%')).order_by(Amatch.date.desc())

    win_num = db.session.query(Amatch, HasMatch, MatchRecord, UserTB).join(HasMatch, and_ \
        (Amatch.match_id == HasMatch.match_id)).join(MatchRecord, and_(HasMatch.r_id == MatchRecord.r_id)). \
        join(UserTB, and_(HasMatch.id == UserTB.id)).filter(UserTB.id.like('%' + str(userid) + '%'),
                                                            Amatch.win == 1).count()

    mvp_num = db.session.query(Amatch, HasMatch, MatchRecord, UserTB).join(HasMatch, and_ \
        (Amatch.match_id == HasMatch.match_id)).join(MatchRecord, and_(HasMatch.r_id == MatchRecord.r_id)). \
        join(UserTB, and_(HasMatch.id == UserTB.id)).filter(UserTB.id.like('%' + str(userid) + '%'),
                                                            MatchRecord.is_mvp == 1).count()

    record_num = records.count()

    if winning_rate != 0:
        winning_rate = request.values.get('winning_rate')
    else:
        winning_rate = format(win_num / record_num, '.2%')

    if mvp_rate != 0:
        mvp_rate = request.values.get('mvp_rate')
    else:
        mvp_rate = format(mvp_num / record_num, '.2%')

    pagination = records.paginate(page=page, per_page=5, error_out=False)
    results = pagination.items

    return render_template('homepage/detail_records_admin.html', pagination=pagination, results=results,
                           member_id=userid, name=name, mvp_rate=mvp_rate, winning_rate=winning_rate, record_num=record_num)


@app.route('/assignment', methods=['GET', 'POST'])
@login_required
def assignment():
    # userid = current_user.id 拿到userid
    page = request.values.get("page", 1, type=int)

    pagination = db.session.query(Assignment).paginate(page=page, per_page=3, error_out=False)

    assignment_list = pagination.items
    # a =(("今天过大年","2019-10-31","反正随便写写就好了说的跟真的有人喜欢似的",1),
    #     ("期末考试啦啦啦","2019-11-31","你一布置我就写岂不是显得我很没面子",2))
    return render_template('assignment/assignment.html', pagination=pagination, assignment_list=assignment_list)


@app.route('/assignment_detail/<int:aid>', methods=['GET', 'POST'])
@login_required
def assignment_detail(aid):
    dbs = DatabaseOperations()
    detail = dbs.query_assignment_detail(int(current_user.id), aid)
    submission = dbs.query_assignment_submission(aid,int(current_user.id))
    grading = dbs.query_assignment_grading(aid,int(current_user.id))
    # 需要assignment_title detail submission status grading status duedate time remaining
    return render_template('.'
                           '/assignment/assignment_detail.html', assignment=detail,aid = aid, submission=submission
                           ,grading=grading)


@app.route('/upload/<int:aid>', methods=['POST'])
def upload(aid):
    file = request.files['inputFile']
    file_id = int(str(aid) + current_user.id)  # Use assignment id and user id to specify a file
    dbs = DatabaseOperations()
    already_submit = dbs.query_already_upload(int(current_user.id), aid)
    # check if document already been submitted
    if already_submit:
        exist_id = int(already_submit[0])
        dbs.delete_file(exist_id)
        # old_submission = db.session.query(FileContents).filter_by(file_id=exist_id)
        # db.session.delete(old_submission)
        # db.session.commit()
        new_file = FileContents(file_id=exist_id, doc_name=file.filename, data=file.read())
        db.session.add(new_file)
        db.session.commit()
        assignment_num = str(aid)
        return redirect('/assignment_detail/' + assignment_num)
    else:
        new_file = FileContents(file_id=file_id, doc_name=file.filename, data=file.read())
        db.session.add(new_file)
        # 是不是要放一个界面更好一些
        new_submit = Submit(file_id=file_id, id=current_user.id, file_grade=0)
        db.session.add(new_submit)
        new_submission = Submission(file_id=file_id, a_id=aid)
        db.session.add(new_submission)
        db.session.commit()
        assignment_num = str(aid)
        return redirect('/assignment_detail/' + assignment_num)
        # return 'Saved ' + file.filename + ' to the database!'


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
    curr_status = "primary"
    status_in_str = "Unchecked"
    return render_template('./attendance/attendance_new.html', members=members, status_colour=curr_status,
                           current_status=status_in_str)


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

    attend = Attendance(id=udt_id)
    attendance_record = AttendanceRecord(status=status_in_int, timestamp=d)
    db.session.add(attend)
    db.session.add(attendance_record)
    db.session.commit()

    return jsonify({'curr_status': status_in_str, 'int_status': status_in_int})


@app.route('/attendance_search', methods=['GET', 'POST'])
@login_required
def attendance_search():
    # 数据库判断权限
    dbs = DatabaseOperations()
    # message = form.username.data
    if request.method == 'POST' :
        year = request.values.get("year")
        month = request.values.get("month")
        day = request.values.get("day")
        # if it post
        date = year +"-"+month+"-"+day
        persons =dbs.query_attendance_date(date)

        # form.year form.month.form.day 确认时间并查询语句
        # 判断不同职位进入不同
        # test_persons = [(1, "吴飞机","今天白给"), (2, "白给大侠","鬼知道去哪里了"), (3,"真的好累阿","约会去了"),
        #                 (4,"要命命","一个人的旅行")]
        return render_template('attendance/attendance_search.html', people = persons)
    else:
        return render_template('attendance/attendance_search.html')


@app.route('/attendance_del', methods=['GET', 'POST'])
@login_required
def attendance_del():
    # 数据库判断权限
    form = DateForm(request.form)
    # message = form.username.data
    if request.method == 'POST' and form.validate():
        # if it post
        # 将form.year form.month.form.day 拼接成时间并链接数据库删除
        test_message="一点情面都不留真就把我删除呗"
        return render_template('attendance/attendance_del.html', message=test_message)
    else:
        return render_template('attendance/attendance_del.html')


@app.route('/grading', methods=['GET', 'POST'])
@login_required
def grading():
    # 数据库判断权限
    # 根据创建者id搜索作业然后进行打分的项目
    # message = int(current_user.id)
    # dbs = DatabaseOperations()
    # assignments = dbs.query_assignment_creater(int(current_user.id))
    page = request.values.get('page', 1, type=int)
    udt_id = str(current_user.id)
    pagination = db.session.query(Assignment, Creator).join\
        (Creator, and_(Assignment.a_id == Creator.a_id)).filter\
        (Creator.id.like('%' + udt_id + '%')).order_by(Assignment.a_date.desc()).paginate(page=page, per_page=3, error_out=False)

    assignments = pagination.items
    # a = (("今天过大年", "2019-10-31", "反正随便写写就好了说的跟真的有人喜欢似的", 1),
    #      ("期末考试啦啦啦", "2019-11-31", "你一布置我就写岂不是显得我很没面子", 2))
    # return render_template('grading/grading.html', assignments=assignments, message=message)
    return render_template('grading/grading.html', assignments=assignments, pagination=pagination, udt_id=udt_id)


@app.route('/grading_detail/<int:aid>', methods=['POST', 'GET'])
def grading_detail(aid):
    dbs = DatabaseOperations()
    assignment = dbs.query_assignment_information(aid)
    number = dbs.query_assignment_number(aid)
    homeworks = dbs.query_homework_information(aid)
    aid = aid * 10000000000

    return render_template('./grading/grading_detail.html', a_id=aid, assignment=assignment, number=number, homeworks=homeworks)


@app.route('/grading_detail/grade', methods=['POST'])
def grade_action():
    db_sql = DatabaseOperations()
    grade = request.form['grade']
    file_id = request.form['file_id']
    db_sql.update_grade(file_id, grade)
    return jsonify({'grade': grade})


@app.route('/download/<int:fid>')
def download(fid):
    file_info = FileContents.query.filter_by(file_id=fid).first()
    return send_file(BytesIO(file_info.data), attachment_filename=file_info.doc_name, as_attachment=True)


@app.route('/assignment_new', methods=['GET', 'POST'])
@login_required
def assignment_new():
    # 数据库判断权限
    form = AssignmentForm(request.form)
    # message = form.username.data
    if request.method == 'POST':
        # 将form内的各种信息写到数据库内 并返回至list界面
        title = request.values.get("assName")
        detail = request.values.get("assReq")
        dueDate = request.values.get("assDueDate")
        dueTime = request.values.get("assDueTime")
        dbs = DatabaseOperations()
        dbs.insert_new_assignment(int(current_user.id), title, detail, dueDate, dueTime)
        return redirect("/grading")
        # return render_template('assignment/assignment_create.html',title=title,detail=detail,dueDate=dueDate,dueTime=dueTime)
    else:
        return render_template('assignment/assignment_create.html')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template('search/search.html')


@app.route('/search_a', methods=['GET', 'POST'])
@login_required
def search_a():
    return render_template('search/search_admin.html')


@app.route('/list', methods=['GET', 'POST'])
@login_required
def result_list():
    input = request.values.get('input', "", type=str)
    select = request.values.get('select', "", type=str)
    page = request.values.get("page", 1, type=int)
    result_num = 0

    # If selected programme
    if select == "major":
        large_table = db.session.query(PersonalInfo, Own, UserTB).join \
            (Own, and_(PersonalInfo.info_id == Own.info_id)).join \
            (UserTB, and_(Own.id == UserTB.id)).filter \
            (PersonalInfo.major.like('%' + input + '%')).order_by \
            (UserTB.id.desc())
        pagination = large_table.paginate(page=page, per_page=5, error_out=False)
    # If selected id
    elif select == "id":
        large_table = db.session.query(PersonalInfo, Own, UserTB).join \
            (Own, and_(PersonalInfo.info_id == Own.info_id)).join \
            (UserTB, and_(Own.id == UserTB.id)).filter \
            (UserTB.id.like('%' + input + '%')).order_by \
            (UserTB.id.desc())
        pagination = large_table.paginate(page=page, per_page=5, error_out=False)
    # If selected name
    else:
        large_table = db.session.query(PersonalInfo, Own, UserTB).join \
            (Own, and_(PersonalInfo.info_id == Own.info_id)).join \
            (UserTB, and_(Own.id == UserTB.id)).filter \
            (UserTB.name.like('%' + input + '%')).order_by \
            (UserTB.id.desc())
        pagination = large_table.paginate(page=page, per_page=5, error_out=False)

    if result_num != 0:
        result_num = request.values.get('result_num')
    else:
        result_num = large_table.count()
    results = pagination.items

    return render_template('search/list.html', pagination=pagination, results=results, current_user=current_user,
                           form_input=input, form_select=select, result_num=result_num)


@app.route('/list_admin', methods=['GET', 'POST'])
@login_required
def result_list_admin():
    input = request.values.get('input', "", type=str)
    select = request.values.get('select', "", type=str)
    page = request.values.get("page", 1, type=int)
    result_num = 0

    # If selected programme
    if select == "major":
        large_table = db.session.query(PersonalInfo, Own, UserTB).join \
            (Own, and_(PersonalInfo.info_id == Own.info_id)).join \
            (UserTB, and_(Own.id == UserTB.id)).filter \
            (PersonalInfo.major.like('%' + input + '%')).order_by \
            (UserTB.id.desc())
        pagination = large_table.paginate(page=page, per_page=5, error_out=False)
    # If selected id
    elif select == "id":
        large_table = db.session.query(PersonalInfo, Own, UserTB).join \
            (Own, and_(PersonalInfo.info_id == Own.info_id)).join \
            (UserTB, and_(Own.id == UserTB.id)).filter \
            (UserTB.id.like('%' + input + '%')).order_by \
            (UserTB.id.desc())
        pagination = large_table.paginate(page=page, per_page=5, error_out=False)
    # If selected name
    else:
        large_table = db.session.query(PersonalInfo, Own, UserTB).join \
            (Own, and_(PersonalInfo.info_id == Own.info_id)).join \
            (UserTB, and_(Own.id == UserTB.id)).filter \
            (UserTB.name.like('%' + input + '%')).order_by \
            (UserTB.id.desc())
        pagination = large_table.paginate(page=page, per_page=5, error_out=False)

    if result_num != 0:
        result_num = request.values.get('result_num')
    else:
        result_num = large_table.count()
    results = pagination.items

    return render_template('search/list_admin.html', pagination=pagination, results=results, current_user=current_user,
                           form_input=input, form_select=select, result_num=result_num)


@app.route('/match_create',methods = ['GET', 'POST'])
@login_required
def match_create():
    if request.method == 'POST':
        matchName = request.values.get("matchName")
        matchDate = request.values.get("matchDate")
        matchOppo = request.values.get("matchOppo")
        firstPosition = int(request.values.get("firstPosition"))
        secondPosition = int(request.values.get("secondPosition"))
        thirdPosition = int(request.values.get("thirdPosition"))
        fourthPosition = int(request.values.get("fourthPosition"))
        side = request.values.get("side")
        mvp = int(request.values.get("mvp"))
        result = request.values.get("result")
        dbs = DatabaseOperations()
        dbs.insert_match_record(matchName, matchDate, matchOppo,int(side),int(result))
        matchID = int(dbs.query_match_id(matchName, matchDate, matchOppo,int(side),int(result))[0])
        #insert to take_part and record and has
        #insert into record return r_id
        r_id1 = int(dbs.insert_record(1, mvp == 1)[0])
        r_id2 = int(dbs.insert_record(2, mvp == 2)[0])
        r_id3 = int(dbs.insert_record(3, mvp == 3)[0])
        r_id4 = int(dbs.insert_record(4, mvp == 4)[0])
        dbs.insert_take_part(matchID, r_id1)
        dbs.insert_take_part(matchID, r_id2)
        dbs.insert_take_part(matchID, r_id3)
        dbs.insert_take_part(matchID, r_id4)
        dbs.insert_has(firstPosition, r_id1)
        dbs.insert_has(secondPosition, r_id2)
        dbs.insert_has(thirdPosition, r_id3)
        dbs.insert_has(fourthPosition, r_id4)
        return render_template('match/match_record.html',matchName=matchName,matchDate=matchDate,side=side,result=result
                               ,matchOppo = matchOppo)
    else:
        return render_template('match/match_record.html')


@app.route('/match_del/<int:mid>',methods = ['GET', 'POST'])
@login_required
def match_del(mid):
    dbs = DatabaseOperations()
    if mid!=0:
        r_id=dbs.query_r_id(mid)
        # return render_template('match/match_del.html',matchs = r_id,r_id = r_id)
        for i in r_id:
            dbs.delete_record(i[0])
            dbs.delete_has(i[0])
            dbs.delete_take_part(i[0])
        dbs.delete_match(mid)
        return redirect('/match_del/0')
    if request.method == 'POST':
        dbs=DatabaseOperations()
        matchDate = request.values.get("date")
        matchs = dbs.query_match_del(matchDate)
        return render_template('match/match_del.html',matchs = matchs)

    return render_template('match/match_del.html')


@app.route('/information/<int:user_id>', methods=['GET', 'POST'])
def information(user_id):
    dbs = DatabaseOperations()
    name = dbs.query_name(int(user_id))[0]
    # 检索数据库取得公告板信息赋值给event，
    # 从数据库中调record
    # 数据库拿到其他信息
    records = dbs.query_match_info(int(user_id))
    try:
        firwin = int(dbs.query_position_times(user_id, 1))
        secwin = int(dbs.query_position_times(user_id, 2))
        thiwin = int(dbs.query_position_times(user_id, 3))
        forwin = int(dbs.query_position_times(user_id, 3))
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
    dbs = DatabaseOperations()
    name = dbs.query_name(int(user_id))[0]
    # 检索数据库取得公告板信息赋值给event，
    # 从数据库中调record
    # 数据库拿到其他信息
    records = dbs.query_match_info(int(user_id))
    try:
        firwin = int(dbs.query_position_times(user_id, 1))
        secwin = int(dbs.query_position_times(user_id, 2))
        thiwin = int(dbs.query_position_times(user_id, 3))
        forwin = int(dbs.query_position_times(user_id, 3))
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

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")

# warning page
@app.route('/authority', methods=['GET', 'POST'])
@login_required
def authority():
    return render_template('warning/authority.html')

