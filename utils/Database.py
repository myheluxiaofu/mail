"""
对pymysql进行二次封装 , 方便之后调用
"""
# 导入pymysql
import pymysql


class Database(object):
    def __init__(self, host="47.108.206.100", user="student", password='stu2022', database='mall', charset='utf8',
                 port=3306):
        # 创建连接对象
        self.cnn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            port=port
        )

    def readall(self, sql, args=None):
        """
        读取所有数据
        :param sql: 需要执行的sql语句
        :param args: sql语句需要的参数
        :return:
        """
        # 创建游标对象
        with self.cnn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            # 使用游标对象执行sql
            cursor.execute(sql, args)
            # 获取结果
            data = cursor.fetchall()
        # 关闭游标(不用关闭)

        # 返回数据
        return data

    def readone(self, sql, args=None):
        """
        读取一条数据
        :param sql: 需要执行的sql语句
        :param args: sql语句需要的参数
        :return:
        """
        # 创建游标对象
        with self.cnn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            # 使用游标对象执行sql
            cursor.execute(sql, args)
            # 获取结果
            data = cursor.fetchone()
        # 关闭游标(不用关闭)

        # 返回数据
        return data

    def write(self, sql, args=None):
        """
        写入数据
        :param sql:  sql语句
        :param args:  sql的参数
        :return:
        """
        try:
            # 创建游标对象
            with self.cnn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                # 开启事务
                # 执行sql
                rows = cursor.execute(sql, args)
                if rows == 0:
                    # 说明执行失败
                    raise Exception("受影响的行数为0")
                # 提交事务
                self.cnn.commit()
                # 返回true
                return True
        except Exception as e:
            # 捕获异常说明执行失败,回滚
            self.cnn.rollback()
            print("执行失败!", e)
            return False

    def __del__(self):
        # 对象被销毁自动执行
        # 关闭连接
        self.cnn.close()


if __name__ == '__main__':
    """
    常见的数据库操作有三个:
    1. 根据sql读取所有数据
    2. 根据sql读取一条数据
    3. 根据sql写入操作
    """
    db = Database()
    sql = "SELECT id,status FROM oms_order WHERE member_id= 19;"
    # arg = '诸葛亮'
    result = db.readone(sql)
    print(result)
    # print(type(result))
    # result_1 = db.readall(sql,arg)
    # print(type(result_1))
    # print(result_1)
