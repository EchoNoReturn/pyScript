from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from TranslateDemo.apidemo.TranslateDemo import createRequest
import psycopg2
import pandas as pd
from time import sleep

from db.sb_config import engine, Rule, db_session, RulesParameter, Issue, RuleDescSection

psql_engine = create_engine("postgresql://psql_admin:psql_admin@127.0.0.1:5432/sonar")
Session = sessionmaker(bind=psql_engine)


def translate(text):
    r = createRequest(text)
    return r.json().get('translation')[0]


# def get_rule():
#     # 查询数据
#     data = pd.read_sql("select * from rules", con=psql_engine)
#     data = data[data['language'] == "ts"]
#     print(data)
#     for index, row in data.iterrows():
#         try:
#             row['name'] = translate(data.at[index, 'name'])
#             print(index, data.at[index, 'name'], row['name'])
#             print("===" * 30)
#             sleep(3)
#         except Exception as e:
#             print(e)
#         finally:
#             # 添加到sqlite数据库
#             with engine.connect() as sqlite_conn:
#                 print(Rule(**row.to_dict()))
#                 db_session.add(Rule(**row.to_dict()))
#                 db_session.commit()
#                 db_session.close()


if __name__ == '__main__':
    # 查询数据
    data = pd.read_sql("select * from rule_desc_sections", con=psql_engine)
    print(data)
    # 创建一个字典来存储已经翻译过的name字段
    translated_names = {}
    key='content'
    for index, row in data.iterrows():
        if index < 2580: # 2926
            continue
        try:
            if row[key] in translated_names:
                print("查字典：", translated_names[row[key]])
                # 字典中有就直接取
                row[key] = translated_names[row[key]]
                continue
            translate_txt = translate(data.at[index, key])
            row[key] = translate_txt
            # 把字段中没有的保存下来
            translated_names[row[key]] = translate_txt
            sleep(3)
        except Exception as e:
            print(e)
        finally:
            print(index, data.at[index, key], row[key])
            print("===" * 30)
            # 添加到sqlite数据库
            with engine.connect() as sqlite_conn:
                print(RuleDescSection(**row.to_dict()))
                db_session.add(RuleDescSection(**row.to_dict()))
                db_session.commit()
                db_session.close()

