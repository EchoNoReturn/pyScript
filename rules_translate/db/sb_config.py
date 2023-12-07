import os
import platform

from pandas import DataFrame
from sqlalchemy import create_engine, BigInteger, Boolean, Column, Index, Integer, SmallInteger, String, Text, text, \
    LargeBinary, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base
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
engine = create_engine(SQLITE_URI, echo=False, pool_pre_ping=True)

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


class RulesParameter(Base):
    __tablename__ = 'rules_parameters'
    __table_args__ = (
        Index('rules_parameters_unique', 'rule_uuid', 'name', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(4000))
    param_type = Column(String(512), nullable=False)
    default_value = Column(String(4000))
    rule_uuid = Column(String(40), nullable=False, index=True)


class RuleRepository(Base):
    __tablename__ = 'rule_repositories'

    kee = Column(String(200), primary_key=True)
    language = Column(String(20), nullable=False)
    name = Column(String(4000), nullable=False)
    created_at = Column(BigInteger, nullable=False)


class RulesDefaultImpact(Base):
    __tablename__ = 'rules_default_impacts'
    __table_args__ = (
        Index('uniq_rul_uuid_sof_qual', 'rule_uuid', 'software_quality', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    rule_uuid = Column(String(40), nullable=False)
    software_quality = Column(String(40), nullable=False)
    severity = Column(String(40), nullable=False)


def add_to_rules(data: DataFrame):
    engine.connect()
    use_db_session = session_maker()
    for index, row in data.iterrows():
        try:
            use_db_session.add(Rule(**row.to_dict()))
            use_db_session.commit()
        except Exception as e:
            print(e)
            use_db_session.rollback()
            raise
        finally:
            use_db_session.close()


class RuleDescSection(Base):
    __tablename__ = 'rule_desc_sections'
    __table_args__ = (
        Index('uniq_rule_desc_sections', 'rule_uuid', 'kee', 'context_key', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    rule_uuid = Column(String(40), nullable=False)
    kee = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    context_key = Column(String(50))
    context_display_name = Column(String(50))

class Issue(Base):
    __tablename__ = 'issues'

    kee = Column(String(50), primary_key=True)
    rule_uuid = Column(String(40), index=True)
    severity = Column(String(10))
    manual_severity = Column(Boolean, nullable=False)
    message = Column(String(4000))
    line = Column(Integer)
    gap = Column(Numeric(30, 20))
    status = Column(String(20))
    resolution = Column(String(20), index=True)
    checksum = Column(String(1000))
    assignee = Column(String(255), index=True)
    author_login = Column(String(255))
    effort = Column(Integer)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger, index=True)
    issue_creation_date = Column(BigInteger, index=True)
    issue_update_date = Column(BigInteger)
    issue_close_date = Column(BigInteger)
    tags = Column(String(4000))
    component_uuid = Column(String(50), index=True)
    project_uuid = Column(String(50), index=True)
    locations = Column(LargeBinary)
    issue_type = Column(SmallInteger)
    from_hotspot = Column(Boolean)
    quick_fix_available = Column(Boolean)
    rule_description_context_key = Column(String(50))
    message_formattings = Column(LargeBinary)
    code_variants = Column(String(4000))

# 逆向工程 自动生成模型文件
if __name__ == '__main__':
    # os.system(f'sqlacodegen {SQLITE_URI} > models.py')
    Base.metadata.create_all(engine)
