from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import pymysql

# To import module MySQLdb()
pymysql.install_as_MySQLdb()
app = Flask(__name__)
# The format should be mysql://username:password@localhost/test
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class FileContents(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


@app.route('/')
def assignment_detail():
    return render_template('./match/match_del.html')


@app.route('/record')
def record():
    return render_template('./match/match_record.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']

    new_file = FileContents(name=file.filename, data=file.read())
    db.session.add(new_file)
    db.session.commit()

    return 'Saved ' + file.filename + ' to the database!'


@app.route('/grading')
def grading():
    return render_template('./grading/grading.html')


@app.route('/grading_detail')
def grading_detail():
    return render_template('./grading/grading_detail.html')


@app.route('/download')
def download():
    file_data = FileContents.query.filter_by(file_id=1)
    return send_file(BytesIO(file_data.data), attachment_filename= file_name, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

