import pymysql
##database连接串 指定要连接的db(Database connection string specifies the DB to connect to)
class DBUtil(object):

    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        return pymysql.connect(host="127.0.0.1", user="root", password="root@123", port=3306, database="london", charset="utf8", autocommit=True)