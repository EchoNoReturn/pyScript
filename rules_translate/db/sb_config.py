import os
import platform

from sqlalchemy import create_engine, BigInteger, Boolean, Column, Index, Integer, SmallInteger, String, Text, text
from sqlalchemy.orm import sessionmaker,declarative_base
from contextlib import contextmanager

"""
Sqlite连接
"""
# 获取当前文件的绝对路径
SQLITE_URI = None
if str(platform.system().lower()) == 'windows':
    path = __file__.replace(fr"\{os.path.basename(__file__)}", "").replace("\\\\", "\\")
    SQLITE_URI = fr'sqlite:///{path}\rulesInfo.db''?check_same_thread=False'
    print(f'数据库路径：{SQLITE_URI}')
elif str(platform.system().lower()) == 'linux':
    path = __file__.replace(fr"/{os.path.basename(__file__)}", "").replace("//", "/")
    SQLITE_URI = fr'sqlite:///{path}/rulesInfo.db''?check_same_thread=False'
    print(f'数据库路径：{SQLITE_URI}')
else:
    print(f"未知系统：{platform.system().lower()}")

# 操作数据库句柄
engine = create_engine(SQLITE_URI, echo=False)

Base = declarative_base(engine)

DbSession = sessionmaker(bind=engine)

db_session = DbSession()

@contextmanager
def session_maker(session=db_session):
    try:
        yield session
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()


class Rule(Base):
    __tablename__ = 'rules'
    __table_args__ = (
        Index('rules_repo_key', 'plugin_rule_key', 'plugin_name', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    name = Column(String(200))
    plugin_rule_key = Column(String(200), nullable=False)
    plugin_key = Column(String(200))
    plugin_config_key = Column(String(200))
    plugin_name = Column(String(255), nullable=False)
    scope = Column(String(20), nullable=False)
    priority = Column(Integer)
    status = Column(String(40))
    language = Column(String(20))
    def_remediation_function = Column(String(20))
    def_remediation_gap_mult = Column(String(20))
    def_remediation_base_effort = Column(String(20))
    gap_description = Column(String(4000))
    system_tags = Column(String(4000))
    is_template = Column(Boolean, nullable=False, server_default=text("false"))
    description_format = Column(String(20))
    rule_type = Column(SmallInteger)
    security_standards = Column(String(4000))
    is_ad_hoc = Column(Boolean, nullable=False)
    is_external = Column(Boolean, nullable=False)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    template_uuid = Column(String(40))
    note_data = Column(Text)
    note_user_uuid = Column(String(255))
    note_created_at = Column(BigInteger)
    note_updated_at = Column(BigInteger)
    remediation_function = Column(String(20))
    remediation_gap_mult = Column(String(20))
    remediation_base_effort = Column(String(20))
    tags = Column(String(4000))
    ad_hoc_name = Column(String(200))
    ad_hoc_description = Column(Text)
    ad_hoc_severity = Column(String(10))
    ad_hoc_type = Column(SmallInteger)
    education_principles = Column(String(255))
    clean_code_attribute = Column(String(40))

# 逆向工程 自动生成模型文件
if __name__ == '__main__':
    os.system(f'sqlacodegen {SQLITE_URI} > models.py')