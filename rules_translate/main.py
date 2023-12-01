from TranslateDemo.apidemo.TranslateDemo import createRequest

if __name__ == '__main__':
    print('hello, python')
    res = createRequest('hello, python')
    print("翻译结果：", res.content)
