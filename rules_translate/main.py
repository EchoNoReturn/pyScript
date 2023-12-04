from TranslateDemo.apidemo.TranslateDemo import createRequest
import psycopg2
import pandas as pd
from time import sleep

from db.sb_config import engine

def translate(text):
    data = createRequest(text)
    return data.json().get('translation')[0]

if __name__ == '__main__':
    # 创建数据库连接
    # conn = psycopg2.connect(database="sonar", user="psql_admin", password="psql_admin", host="localhost", port="5432")
    # 查询数据
    # data = pd.read_sql("select * from rules", con=conn)
    data = pd.read_sql("select * from rules", con=engine.connect())
    data = data[data['language'] == "java"]
    print(data)
    li = data['name']
    index = 0
    for key in data['name']:
        # to_str = translate(parts[0]) + " (" + parts[1] if len(parts) > 1 else translate(parts[0])
        # print(key, to_str)
        try: 
            sleep(1.5)
            li[index] = translate(key)
            print(index, key, li[index])
        except Exception as e:
            print(e)
        finally:
            index += 1
            data['name'] = li
            # 添加到sqlite数据库
            with engine.connect() as connnect:
                data.to_sql('rules', con=connnect, if_exists='replace', index=False)
    # print(data['name']) # 打印看下
    # conn.close()
