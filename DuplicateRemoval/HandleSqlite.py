import pandas as pd
from sqlalchemy import create_engine

from rules_translate.db.sb_config import engine

if __name__ == '__main__':
    engine_psql = create_engine("postgresql://psql_admin:psql_admin@127.0.0.1:5432/sonar")
    data_origin = pd.read_sql("select * from rules_parameters", con=engine_psql)
    df = data_origin['Remove' in data_origin['description']]
    df.to_excel('需要翻译的字段.xlsx', index=False)
    # print(data_origin)
    # data = pd.read_sql("select * from rules", con=engine)
    # data.drop_duplicates(keep='first', subset='uuid', inplace=True)
    # print(data)
    # data.to_sql('rules_js', con=engine, if_exists='replace', index=False)
