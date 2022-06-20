import json
import os

"""
    这是一个JSON文件操作类
    os.path.dirname(): 获取文件的绝对路径
    os.path.dirname(__file__) 获取当前脚本的绝对路径
"""


class OperationJson:
    @staticmethod
    def operation_json(path):
        with open(os.path.dirname(os.path.dirname(__file__)) + f"/data/{path}", "r", encoding="UTF-8") as f:
            return json.load(f)


if __name__ == '__main__':
    print(OperationJson.operation_json("login_data.json"))
