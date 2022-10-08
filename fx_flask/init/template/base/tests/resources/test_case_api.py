import pytest

from app import flask_app


class TestCaseApi:
    """测试接口样例"""

    def setup_class(self) -> None:
        """pytest 执行当前类时"""
        self.cur_app = flask_app
        self.cur_app.config['TESTING'] = True
        self.client = self.cur_app.test_client()
        self.header = {'Authorization': 'asdasdadas'}

    def test_case(self, universe_client):  # pylint: disable=W0613
        """

        Args:
            universe_client (_type_): _description_
        """
        case_num = 'T20220413105827H51932163'
        response = self.client.get(f'/case/{case_num}', headers=self.header)
        print(response)
        # assert response.status_code == 200


if __name__ == '__main__':
    pytest.main(['-s', 'test_case_api.py'])
