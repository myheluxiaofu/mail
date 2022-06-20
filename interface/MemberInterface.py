from utils.getkeyword import GetKeyWord
from utils.sendmethod import SendMethod


class MemberInterface:
    #  TODO 发送验证码请求
    def __init__(self):
        self.url = "http://47.108.206.100:8085"

    def get_auth_cod(self, telephone):
        method = "get"
        url = self.url + "/sso/getAuthCode"
        params = {
            "telephone": telephone
        }
        return SendMethod.send_method(method, url, params=params)

    # TODO 提取验证码
    def get_verify_cod(self, telephone):
        code = self.get_auth_cod(telephone)
        return GetKeyWord.get_key_word(code, "data")

    # TODO 会员注册
    def register(self, username, password, telephone):
        method = "post"
        url = self.url + "/sso/register"
        data = {
            "username": username,
            "password": password,
            "telephone": telephone,
            "authCode": self.get_verify_cod(telephone)
        }
        return SendMethod.send_method(method, url, data=data)

    # TODO 登入
    def login(self, username, password):
        method = "post"
        url = self.url + "/sso/login"
        data = {
            "username": username,
            "password": password
        }
        return SendMethod.send_method(method, url, data=data)

    # TODO 获取用户登入令牌
    def get_member_token(self, username, password):
        code = self.login(username, password)
        resp = GetKeyWord.get_key_word(code, 'token')
        return {"Authorization": f"Bearer {resp}"}  # Bearer 后面有空格

    # TODO 获取会员信息
    def get_info(self, username, password):
        method = "get"
        url = self.url + "/sso/info"
        params = username
        headers = self.get_member_token(username, password)
        return SendMethod.send_method(method, url, params=params, headers=headers)

    # TODO 会员修改密码
    def update_password(self, username, password, telephone, uppassword):
        method = "post"
        url = self.url + "/sso/updatePassword"
        headers = self.get_member_token(username, password)
        data = {
            "password": uppassword,
            "telephone": telephone,
            "authCode": self.get_verify_cod(telephone)
        }
        return SendMethod.send_method(method, url, data=data, headers=headers)


if __name__ == '__main__':
    # print(MemberInterface().update_password("yang", "12346", '133456789123', '123456'))
    print(MemberInterface().get_member_token("yang", '123456'))
