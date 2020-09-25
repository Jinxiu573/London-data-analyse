from dao.DBUtil import DBUtil
import pymysql

class Data():
    def __init__(self, id, site, species, reading_date_time, value, units, pr):
        self.id = id
        self.site = site
        self.species = species
        self.reading_date_time = reading_date_time
        self.value = value
        self.units = units
        self.pr = pr

class DataDao():

    def save(self, datas: list):
        """
        保存数据(Save data)
        :return:
        """
        sql = 'insert into t_data(site, species, reading_date_time, `value`, units, pr) values(%s, %s, %s, %s, %s,%s);'
        conn = DBUtil.get_connection()
        cursor = conn.cursor()
        # 拼接并执行sql语句(Splice and execute the SQL statement)
        cursor.executemany(sql, datas)
        # 涉及写操作要注意提交(Pay attention to commit when writing operations are involved)
        conn.commit()
        # 关闭连接(Close the connection)
        cursor.close()
        conn.close()

    def delete(self):
        """
        清空所有数据(Clear all data)
        :return:
        """
        sql = 'delete from t_data where 1 = 1'
        conn = DBUtil.get_connection()
        cursor = conn.cursor()
        # 拼接并执行sql语句(Splice and execute the SQL statement)
        cursor.execute(sql)
        # 涉及写操作要注意提交(Pay attention to commit when writing operations are involved)
        conn.commit()
        # 关闭连接(Close the connection)
        cursor.close()
        conn.close()

    def query(self, sql):
        """
        查找所有(Find all)
        :return:
        """
        conn = DBUtil.get_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
