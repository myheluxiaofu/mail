import pymysql


class Mysql:
    @staticmethod
    def extract_mysql(sql):
        # 创建连接对象
        conn = pymysql.connect(
            host="47.108.206.100",
            user="student",
            password="stu2022",
            database="mall",
            port=3306,
            charset='utf8'
        )
        # 获取游标对象
        # sql = "SELECT id,status FROM oms_order WHERE member_id= 19 ;"
        cursor = conn.cursor()
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有的数据
        mysql_data = cursor.fetchall()
        return mysql_data

    def __del__(self):
        # 对象被销毁自动执行
        # 关闭连接
        self.conn.close()


if __name__ == '__main__':
    newest_status = Mysql.extract_mysql("SELECT id,status FROM oms_order WHERE member_id= 19 ;")
    print(newest_status)
