import requests

from .utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = '0715bdbb242319cc'
# 您的应用密钥
APP_SECRET = 'Geh7hmv2C7cx8kc5WEbpBp8WOubxhmJY'

'''
    @params str string 需要翻译的文本
'''
def createRequest(txt: str):
    """
    note: 将下列变量替换为需要请求的参数
    """
    q = txt
    lang_from = 'en'
    lang_to = 'zh-CHS'

    data = {'q': q, 'from': lang_from, 'to': lang_to}
    addParams = addAuthParams(APP_KEY, APP_SECRET, q)
    for key in addParams:
        data[key] = addParams[key]
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    print(str(res.content, 'utf-8'))
    return res


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
# if __name__ == '__main__':
#     createRequest()
