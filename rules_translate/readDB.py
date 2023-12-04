import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def connect(user, password, db, host='lcoalhost', port='5432'):
    """Returns a connection and a metadata object"""
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    engine = sqlalchemy.create_engine(url, client_encoding='utf8', echo=True)

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=engine)

    return engine, meta
