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
            sql="select match_name,opponent,position,win,is_mvp " \
                "from amatch NATURAL join take_part NATURAL JOIN record " \
                "where r_id in (SELECT r_id from has where id = %d) order by date desc" % (user_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            return results[:3]
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
            sql = """SELECT id, name, status FROM user NATURAL JOIN personal_information 
            NATURAL JOIN own NATURAL JOIN attend NATURAL JOIN attendance_record WHERE grade <= 1"""
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