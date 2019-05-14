from flask import Flask, render_template, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import pymysql
from attendance import DatabaseOperations
import datetime
from datetime import timedelta

# To import module MySQLdb()
pymysql.install_as_MySQLdb()
app = Flask(__name__)
# The format should be mysql://username:password@localhost/test
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/udms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds =1)
db = SQLAlchemy(app)





class Attendance(db.Model):
    __tablename__ = 'attend'
    id = db.Column(db.Integer, primary_key=True)
    a_id = db.Column(db.BigInteger, primary_key=True)

    def __init__(self, udt_id, a_id):
        self.id = udt_id
        self.a_id = a_id


class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_record'
    a_id = db.Column(db.BigInteger, primary_key=True)
    status = db.Column(db.Integer)

    def __init__(self, a_id, status):
        self.a_id = a_id
        self.status = status


@app.route('/upload', methods=['POST'])



@app.route('/assignment_detail/<int:aid>')
def assignment_detail(aid):
    #将改assignment的具体信息po出


    return render_template('./assignment/assignment_detail.html')


@app.route('/attendance')
def attendance():
    return render_template('./attendance/attendance.html')


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


@app.route('/grading_detail/')
def grading_detail():
    return render_template('./grading/grading_detail.html')


@app.route('/download/<int:fid>')
def download(fid):
    file_info = FileContents.query.filter_by(file_id=fid).first()
    return send_file(BytesIO(file_info.data), attachment_filename=file_info.doc_name, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

