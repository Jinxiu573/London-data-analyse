from dao.DBUtil import DBUtil
import pymysql

class User():
    def __init__(self, username, password, auth):
        self.username = username
        self.password = password
        self.auth = auth


class UserDao():
    """
    用户操作Dao(User Operated Dao)
    """
    def save(self, user: User):
       """
       保存(keep)
       :param user:
       :return:
       """
       sql = 'insert into t_user values ("%s", "%s", "%s")' % (user.username, user.password, user.auth)
       conn = DBUtil.get_connection()
       cursor = conn.cursor()
       cursor.execute(sql)
       cursor.close()
       conn.close()

    def get(self, user: User):
        """
        获取(get)
        :param user:
        :return:
        """
        sql = "select * from t_user"
        if user != None:
            sql += " where"
            if user.username != None:
                sql += " username = '" + user.username + "'"
            if user.password != None:
                sql += " and password = '" + user.password + "'"
            if user.auth != None:
                sql += " and auth = '" + user.auth + "'"
        conn = DBUtil.get_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results