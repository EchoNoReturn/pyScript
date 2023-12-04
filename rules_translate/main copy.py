from TranslateDemo.apidemo.TranslateDemo import createRequest
import psycopg2
import pandas as pd


if __name__ == '__main__':
    print('hello, python')
    conn = psycopg2.connect(database="sonar", user="psql_admin", password="psql_admin", host="localhost", port="5432")
    # data = pd.read_sql("select * from pg_tables", con=conn) # 获取所有的表格
    data = pd.read_sql("select * from rules", con=conn) # 获取所有的表格
    # cur = conn.cursor()
    # cur.execute("select * from pg_tables")
    # res = cur.fetchall()
    li = []
    for i in range(len(data)):
        item = {}
        for key in data.columns.to_list():
          value = data.loc[i].get(key)
          item[key] = value if value is not None else ''
        li.append(item)
    print(li[0])
    # res = createRequest('hello, world') # 通过调用这个方法获取翻译结果
    # print("翻译结果：", res.content)
    
    conn.close()
