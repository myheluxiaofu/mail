import pytest
from interface.MemberInterface import MemberInterface
from utils.getkeyword import GetKeyWord
from utils.operation_json import OperationJson


class TestCaseRegister:
    # 验证登入接口
    @pytest.mark.parametrize("login_data", OperationJson.operation_json('login_data.json'))
    def test_register(self, login_data):
        # 发送请求
        reqs = MemberInterface().login(login_data["username"], login_data["password"])
        # print(reqs)
        # 断言
        assert str(GetKeyWord.get_key_word(reqs, "code")) == login_data["code"]
        assert str(GetKeyWord.get_key_word(reqs, "message")) == login_data["message"]

    # 验证 获取会员信息 接口
    def test_info(self):
        # 发送请求
        reqs = MemberInterface().get_info("yang", "123456")
        print(reqs)
        # 断言
        assert GetKeyWord.get_key_word(reqs, "username") == "yang"
        assert GetKeyWord.get_key_word(reqs,
                                       "password") == "$2a$10$LeE9UrKAfP5onbiK8K4Vwu//RWrd1YvnnX8HwLf/Six35lzielRjy"

    # 验证 会员修改密码 接口
    def test_updata_password(self):
        # 发送请求
        reqs = MemberInterface().update_password("yang", "123456", '13329755249', '123456')
        
        assert GetKeyWord.get_key_word(reqs, "code") == 200
        assert GetKeyWord.get_key_word(reqs, "message") == "密码修改成功"
