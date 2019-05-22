import pymysql

class DatabaseOperations():
    __db_url = '127.0.0.1'
    __db_username = 'root'
    __db_password = ''
    __db_name = 'udms'
    __db = ''

    def __init__(self):
        """Connect to database when the object is created."""
        self.__db = self.db_connect()

    def __del__(self):
        """Disconnect from database when the object is destroyed."""
        self.__db.close()

    def db_connect(self):
        self.__db = pymysql.connect(
            self.__db_url, self.__db_username, self.__db_password, self.__db_name)
        return self.__db

    def query_password (self, user_id):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = "SELECT password from user where id = %d" % user_id
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
        except Exception as e:
            return None

    def query_name(self, user_id):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = "SELECT name from user where id = %d" % user_id
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
        except Exception as e:
            return None

    def query_authority(self, user_id):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = "SELECT group_id from belong_to where id = %d" % user_id
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
        except Exception as e:
            return None

    def query_attendance(self, user_id,status):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = "select count(attendance_record.status) " \
                  "from attendance_record natural join attend " \
                  "where attendance_record.status = %d and attend.id = %d" % (status, user_id)
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
        except Exception as e:
            return None

    def query_assignment(self):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = "select a_id,title,a_date,detail " \
                  "from assignment"
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def query_assignment_creater(self,user_id):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = "select title,a_date,detail,a_id from assignment where create_id = %d" % user_id
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def query_assignment_detail(self, user_id, a_id):
        cursor = self.__db.cursor()
        try:
            sql = "select title,detail,dueDate,dueTime from assignment where a_id = %d" % a_id
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            result = results[:]
            # sqls = "select file_id from submit natural join submission where a_id = %d and id = %d" % (a_id,user_id)
            # cursor2.execute(sqls)
            # self.__db.commit()
            # temp1 = cursor2.fetchall()
            # if temp1:
            #     result = result + (1,)
            #     sql = "select doc_grade from submit natural join submission where a_id = %d and id = %d" % (a_id, user_id)
            #     cursor.execute(sql)
            #     self.__db.commit()
            #     temp2 = cursor.fetchall()
            #     result = result + temp2[0]
            # else:
            #     result = result + (0, '0')

            return result
        except Exception as e:
            return None

    def query_assignment_submission(self, a_id, user_id):
        cursor = self.__db.cursor()
        try:
            sqls = "select file_id from submit natural join submission where a_id = %d and id = %d" % (a_id,user_id)
            cursor.execute(sqls)
            temp1 = cursor.fetchall()
            if temp1:
                return 1
            else:
                return 0
            #     sql = "select doc_grade from submit natural join submission where a_id = %d and id = %d" % (a_id, user_id)
            #     cursor.execute(sql)
            #     self.__db.commit()
            #     temp2 = cursor.fetchall()
            #     result = result + temp2[0]
            # else:
            #     result = result + (0, '0')
        except Exception as e:
            return None
    def query_assignment_grading(self, a_id, user_id):
        cursor = self.__db.cursor()
        try:
            sql = "select file_grade from submit natural join submission where a_id = %d and id = %d" % (a_id, user_id)
            cursor.execute(sql)
            temp2 = cursor.fetchall()[0][0]
            if temp2 == '0':
                return 0
            else:
                return 1

        except Exception as e:
            return None


    def query_assignment_information(self, a_id):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = "select title, detail, dueDate, dueTime from assignment where a_id = %d" % a_id
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
        except Exception as e:
            return None

    def query_assignment_number(self, a_id):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = "select COUNT(file_id) from submission where a_id = %d " % a_id
            cursor.execute(sql)
            results = cursor.fetchall()[0][0]
            return results
        except Exception as e:
            return None

    def query_homework_information(self, a_id):
        cursor = self.__db.cursor()
        try:
            sql = "select id,name,doc_name,file_id " \
                  "from submission natural join submit natural join user natural join file_contents " \
                  "where a_id = %d " % a_id
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def insert_new_assignment(self, user_id, title , detail,dueDate,dueTime):
        cursor = self.__db.cursor()
        try:
            sql = "INSERT INTO assignment" \
                  "(a_date, title, detail, create_id, dueDate, dueTime) " \
                  "VALUES ('2019-5-20','%s','%s',%d,'%s','%s')" % (title,detail,user_id,dueDate,dueTime)
            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return

    def query_search(self,select,input):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        sql = ""
        if select =="major":
            sql = "select id,name,last_name,major " \
                  "from user NATURAL join own NATURAL JOIN personal_information " \
                  "where major like '%%%s%%' " % input
        elif select == "name":
            sql = "select id,name,last_name major " \
                  "from user NATURAL join own NATURAL JOIN personal_information " \
                  "where name like  '%%%s%%' " % input
        else:
            sql = "select id,name,last_name major " \
                  "from user NATURAL join own NATURAL JOIN personal_information " \
                  "where id like  '%%%s%%' " % input
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None
    def query_match_info(self,user_id):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql="select match_name,opponent,position,win,is_mvp,side " \
                "from amatch NATURAL join take_part NATURAL JOIN record " \
                "where r_id in (SELECT r_id from has where id = %d) order by date desc" % (user_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            return results[:3]
        except Exception as e:
            return None
    def query_match_del(self,date):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql="select match_name,win,side,opponent,match_id " \
                "from amatch where date = '%s'" % date
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def query_position_times(self,user_id,position):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql="select count(win) " \
                "from amatch natural join take_part NATURAL join record NATURAL join has " \
                "where position = %d and win=1 and id = %d" % (position,user_id)
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            results = results[0]
            return results
        except Exception as e:
            return None

    def query_group (self, date):
        """Transfer Python datetime object to string, then do query."""
        cursor = self.__db.cursor()
        try:
            sql = 'SELECT event FROM `events` WHERE `event_id` = ' \
                  '(SELECT `event_id` FROM `dates` INNER JOIN `dates_events` ON dates.date_id = dates_events.date_id ' \
                  'WHERE `date` = str_to_date("{0}","%Y-%m-%d"))'.format(
                str(date))
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
        except Exception as e:
            return None

    def query_attendance_one_year(self):
        cursor = self.__db.cursor()
        try:
            # sql = """SELECT id, name, status FROM user NATURAL JOIN own
            # NATURAL JOIN personal_information NATURAL JOIN attend NATURAL JOIN attendance_record WHERE grade <= 1"""
            sql = """SELECT id, name FROM user NATURAL JOIN own
            NATURAL JOIN personal_information WHERE grade <= 1"""
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def query_attendance_two_year(self):
        cursor = self.__db.cursor()
        try:
            sql = """SELECT id, name FROM user NATURAL JOIN personal_information 
            NATURAL JOIN own WHERE grade > 1 AND grade <= 2"""
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def query_attendance_over_two_year(self):
        cursor = self.__db.cursor()
        try:
            sql = """SELECT id, name FROM user NATURAL JOIN personal_information 
            NATURAL JOIN own WHERE grade > 2"""
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def query_attendance_admin(self):
        cursor = self.__db.cursor()
        try:
            sql = """SELECT id, name FROM user NATURAL JOIN belong_to 
            WHERE group_id = 1"""
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def query_attendance_all(self):
        cursor = self.__db.cursor()
        try:
            sql = """SELECT id, name FROM user"""
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def insert_record(self, position,is_mvp):
        if is_mvp:
            is_mvp = 1
        else:
            is_mvp = 0
        cursor = self.__db.cursor()
        try:
            sql = "INSERT INTO record" \
                  "(position, is_mvp) " \
                  "VALUES (%d,%d)" % (position, is_mvp)
            cursor.execute(sql)
            self.__db.commit()
            sql = "select max(r_id) from record"
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
        except Exception as e:
            return

    def insert_take_part(self, m_id, r_id):
        cursor = self.__db.cursor()
        try:
            sql = "INSERT INTO take_part" \
                  "(match_id, r_id) " \
                  "VALUES (%d,%d)" % (m_id, r_id)
            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return

    def insert_has(self, user_id, r_id):
        cursor = self.__db.cursor()
        try:
            sql = "INSERT INTO has" \
                  "(id, r_id) " \
                  "VALUES (%d,%d)" % (user_id, r_id)
            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return

    def insert_match_record(self, matchName ,matchDate, matchOppo, side, result):
        cursor = self.__db.cursor()
        try:

            sql = "insert into amatch (match_name, date, win, side, opponent)  values" \
                  "('%s','%s','%d','%d','%s') " % (matchName, matchDate, result, side, matchOppo)

            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return

    def query_match_id(self, matchName ,matchDate, matchOppo, side, result):
        cursor = self.__db.cursor()
        try:

            sql = "select max(match_id) from amatch "


            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
            return
        except Exception as e:
            return

    def query_r_id(self, m_id):
        cursor = self.__db.cursor()
        try:

            sql = "select r_id from take_part where match_id = %d  " % m_id
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return

    def delete_record(self,r_id):
        cursor = self.__db.cursor()
        try:

            sql = "delete from record where r_id = %d" % r_id
            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return
    def delete_has(self,r_id):
        cursor = self.__db.cursor()
        try:

            sql = "delete from has where r_id = %d" % r_id
            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return
    def delete_take_part(self,r_id):
        cursor = self.__db.cursor()
        try:

            sql = "delete from take_part where match_id = %d" % r_id
            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return
    def delete_match(self,m_id):
        cursor = self.__db.cursor()
        try:

            sql = "delete from amatch where match_id = %d" % m_id
            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return

    def update_password(self, user_id, new_pwd):
        cursor = self.__db.cursor()
        try:
            sql = "UPDATE user SET password ='%s' WHERE id = %d" % (new_pwd, user_id)
            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return

    def insert_notice(self, text):
        cursor = self.__db.cursor()
        try:
            # sql = "create table notice(" \
            #       "text varchar(255))"
            # cursor.execute(sql)
            sql = "insert into notice values ('%s')" % text
            cursor.execute(sql)
            self.__db.commit()
            return
        except Exception as e:
            return

    def query_notice(self):
        cursor = self.__db.cursor()
        try:
            # sql = "create table notice(" \
            #       "text varchar(255))"
            # cursor.execute(sql)
            sql = "select * from notice"
            cursor.execute(sql)
            results = cursor.fetchall()
            result = ()
            for i in results:
                result = result + i
            return result
        except Exception as e:
            return

    def drop_notice(self):
        cursor = self.__db.cursor()
        try:
            sql = "drop table notice"
            cursor.execute(sql)
            # for i in text:
            #     sql ="insert into notice values = %s" % i
            #     cursor.execute(sql)
            return
        except Exception as e:
            return

    def creat_notice(self):
        cursor = self.__db.cursor()
        try:
            # sql = "drop table notice"
            # cursor.execute(sql)
            sql = "create table notice(" \
                  "text varchar(255))"
            cursor.execute(sql)
            # for i in text:
            #     sql ="insert into notice values = %s" % i
            #     cursor.execute(sql)
            return
        except Exception as e:
            return

    def query_already_upload(self,user_id,a_id):
        cursor = self.__db.cursor()
        try:
            sql = """SELECT file_id 
            from submit NATURAL join submission 
            where id = %d and a_id = %d """ % (user_id,a_id)
            cursor.execute(sql)
            results = cursor.fetchall()[0]
            return results
        except Exception as e:
            return None
    def query_attendance_date(self,date):
        cursor = self.__db.cursor()
        try:
            sql = """select id,name,status from attendance_record natural join attend natural join user
            where timestamp between '%s 0:00:00' and '%s 23:59:59'""" %(date,date)
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            return None

    def delete_file(self, file_id):
        cursor = self.__db.cursor()
        try:
            sql = "delete from file_contents where file_id = %d" % file_id
            cursor.execute(sql)
            self.__db.commit()
            # for i in text:
            #     sql ="insert into notice values = %s" % i
            #     cursor.execute(sql)
            return
        except Exception as e:
            return

