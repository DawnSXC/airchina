import requests
import json


class ReqTest:

    # 发送post请求
    def req_post(self, url, data):
        res = requests.post(url=url, data=data).json()
        return json.dumps(res, indent=2)

    # 发送get请求
    def req_get(self, url, data):
        res = requests.get(url=url, data=data).json()
        return json.dumps(res, indent=2)

    def run_req(self, url, method, data=None):
        res = None
        if method == "POST":
            res = self.req_post(url, data)
        else:
            res = self.req_get(url, data)
        return res


if __name__ == '__main__':
    url = "http://127.0.0.1:8000/login/"
    data = {
        'username': 'test',
        'password': 'test'
    }
    req = ReqTest(url, 'POST', data)
    print(req.res)

