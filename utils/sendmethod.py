import requests


class SendMethod:
    @staticmethod
    # 封装请求
    def send_method(method, url, params=None, data=None, json=None, headers=None):
        if method == "get":
            reqs = requests.get(url=url, params=params, headers=headers)
        elif method == "post":
            reqs = requests.post(url=url, data=data, json=json, headers=headers)
        else:
            reqs = None
            print("请求方式错误")
        # 封装响应
        result = {}
        if reqs is not None:
            result["status_code"] = reqs.status_code  # 获取响应状态码
            result["headers"] = reqs.headers  # 获取响应行
            result["json"] = reqs.json()  # 获取JSON格式的响应体
            result["time"] = reqs.elapsed.microseconds / 1000
            return result
        else:
            return reqs


if __name__ == '__main__':
    method = "post"
    url = "http://47.108.206.100:8080/admin/login"
    body = {
        "username": "admin",
        "password": "macro123"
    }
    print(SendMethod.send_method(method, url, json=body))
