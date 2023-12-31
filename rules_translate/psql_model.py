# coding: utf-8
# 使用到的 psql 数据库的所有表格模型
from sqlalchemy import create_engine, BigInteger, Boolean, Column, DateTime, Index, Integer, LargeBinary, Numeric, SmallInteger, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# username = "psql_admin"
# password = "psql_admin"
# hostname = "127.0.0.1"
# port = "5432"
# database_name = "sonar"
# 使用下面两个东西去操作数据库
# engine = create_engine(f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}")
psql_engine = create_engine("postgresql://psql_admin:psql_admin@127.0.0.1:5432/sonar")
Session = sessionmaker(bind=psql_engine)

Base = declarative_base()
metadata = Base.metadata


class ActiveRuleParameter(Base):
    __tablename__ = 'active_rule_parameters'

    uuid = Column(String(40), primary_key=True)
    value = Column(String(4000))
    rules_parameter_key = Column(String(128))
    active_rule_uuid = Column(String(40), nullable=False, index=True)
    rules_parameter_uuid = Column(String(40), nullable=False)


class ActiveRule(Base):
    __tablename__ = 'active_rules'
    __table_args__ = (
        Index('uniq_profile_rule_uuids', 'profile_uuid', 'rule_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    failure_level = Column(Integer, nullable=False)
    inheritance = Column(String(10))
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    profile_uuid = Column(String(40), nullable=False)
    rule_uuid = Column(String(40), nullable=False)


class AlmPat(Base):
    __tablename__ = 'alm_pats'
    __table_args__ = (
        Index('uniq_alm_pats', 'user_uuid', 'alm_setting_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    pat = Column(String(2000), nullable=False)
    user_uuid = Column(String(256), nullable=False)
    alm_setting_uuid = Column(String(40), nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)


class AlmSetting(Base):
    __tablename__ = 'alm_settings'

    uuid = Column(String(40), primary_key=True)
    alm_id = Column(String(40), nullable=False)
    kee = Column(String(200), nullable=False, unique=True)
    url = Column(String(2000))
    app_id = Column(String(80))
    private_key = Column(String(2500))
    pat = Column(String(2000))
    updated_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    client_id = Column(String(80))
    client_secret = Column(String(160))
    webhook_secret = Column(String(160))


class AnalysisProperty(Base):
    __tablename__ = 'analysis_properties'

    uuid = Column(String(40), primary_key=True)
    analysis_uuid = Column(String(40), nullable=False, index=True)
    kee = Column(String(512), nullable=False)
    text_value = Column(String(4000))
    clob_value = Column(Text)
    is_empty = Column(Boolean, nullable=False)
    created_at = Column(BigInteger, nullable=False)


class AnticipatedTransition(Base):
    __tablename__ = 'anticipated_transitions'

    uuid = Column(String(40), primary_key=True)
    project_uuid = Column(String(40), nullable=False)
    user_uuid = Column(String(255), nullable=False)
    transition = Column(String(20), nullable=False)
    transition_comment = Column(String(4000))
    line = Column(Integer)
    message = Column(String(4000))
    line_hash = Column(String(255))
    rule_key = Column(String(200), nullable=False)
    file_path = Column(String(1500), nullable=False)
    created_at = Column(BigInteger, nullable=False)


class AppBranchProjectBranch(Base):
    __tablename__ = 'app_branch_project_branch'
    __table_args__ = (
        Index('uniq_app_branch_proj', 'application_branch_uuid', 'project_branch_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    application_uuid = Column(String(40), nullable=False, index=True)
    application_branch_uuid = Column(String(40), nullable=False, index=True)
    project_uuid = Column(String(40), nullable=False, index=True)
    project_branch_uuid = Column(String(40), nullable=False, index=True)
    created_at = Column(BigInteger, nullable=False)


class AppProject(Base):
    __tablename__ = 'app_projects'
    __table_args__ = (
        Index('uniq_app_projects', 'application_uuid', 'project_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    application_uuid = Column(String(40), nullable=False, index=True)
    project_uuid = Column(String(40), nullable=False, index=True)
    created_at = Column(BigInteger, nullable=False)


class Audit(Base):
    __tablename__ = 'audits'

    uuid = Column(String(40), primary_key=True)
    user_uuid = Column(String(255), nullable=False)
    user_login = Column(String(255), nullable=False)
    category = Column(String(25), nullable=False)
    operation = Column(String(50), nullable=False)
    new_value = Column(String(4000))
    created_at = Column(BigInteger, nullable=False, index=True)
    user_triggered = Column(Boolean, nullable=False, server_default=text("true"))


class CeActivity(Base):
    __tablename__ = 'ce_activity'
    __table_args__ = (
        Index('ce_activity_islast', 'is_last', 'status'),
        Index('ce_activity_main_islast', 'main_is_last', 'status')
    )

    uuid = Column(String(40), primary_key=True)
    task_type = Column(String(40), nullable=False)
    entity_uuid = Column(String(40), index=True)
    component_uuid = Column(String(40), index=True)
    status = Column(String(15), nullable=False)
    main_is_last = Column(Boolean, nullable=False)
    main_is_last_key = Column(String(80), nullable=False, index=True)
    is_last = Column(Boolean, nullable=False)
    is_last_key = Column(String(80), nullable=False, index=True)
    submitter_uuid = Column(String(255))
    submitted_at = Column(BigInteger, nullable=False)
    started_at = Column(BigInteger)
    executed_at = Column(BigInteger)
    execution_count = Column(Integer, nullable=False)
    execution_time_ms = Column(BigInteger)
    analysis_uuid = Column(String(50))
    error_message = Column(String(1000))
    error_stacktrace = Column(Text)
    error_type = Column(String(20))
    worker_uuid = Column(String(40))
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    node_name = Column(String(100))


class CeQueue(Base):
    __tablename__ = 'ce_queue'

    uuid = Column(String(40), primary_key=True)
    task_type = Column(String(40), nullable=False)
    entity_uuid = Column(String(40), index=True)
    component_uuid = Column(String(40), index=True)
    status = Column(String(15))
    submitter_uuid = Column(String(255))
    started_at = Column(BigInteger)
    worker_uuid = Column(String(40))
    execution_count = Column(Integer, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class CeScannerContext(Base):
    __tablename__ = 'ce_scanner_context'

    task_uuid = Column(String(40), primary_key=True)
    context_data = Column(LargeBinary, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class CeTaskCharacteristic(Base):
    __tablename__ = 'ce_task_characteristics'

    uuid = Column(String(40), primary_key=True)
    task_uuid = Column(String(40), nullable=False, index=True)
    kee = Column(String(512), nullable=False)
    text_value = Column(String(512))


class CeTaskInput(Base):
    __tablename__ = 'ce_task_input'

    task_uuid = Column(String(40), primary_key=True)
    input_data = Column(LargeBinary)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class CeTaskMessage(Base):
    __tablename__ = 'ce_task_message'

    uuid = Column(String(40), primary_key=True)
    task_uuid = Column(String(40), nullable=False, index=True)
    message = Column(String(4000), nullable=False)
    created_at = Column(BigInteger, nullable=False)
    message_type = Column(String(255), nullable=False, index=True)


t_components = Table(
    'components', metadata,
    Column('uuid', String(50), nullable=False, unique=True),
    Column('kee', String(1000)),
    Column('deprecated_kee', String(400)),
    Column('name', String(2000)),
    Column('long_name', String(2000)),
    Column('description', String(2000)),
    Column('enabled', Boolean, nullable=False, server_default=text("true")),
    Column('scope', String(3)),
    Column('qualifier', String(10), index=True),
    Column('private', Boolean, nullable=False),
    Column('language', String(20)),
    Column('copy_component_uuid', String(50)),
    Column('path', String(2000)),
    Column('uuid_path', String(1500), nullable=False),
    Column('branch_uuid', String(50), nullable=False, index=True),
    Column('b_changed', Boolean),
    Column('b_name', String(500)),
    Column('b_long_name', String(500)),
    Column('b_description', String(2000)),
    Column('b_enabled', Boolean),
    Column('b_qualifier', String(10)),
    Column('b_language', String(20)),
    Column('b_copy_component_uuid', String(50)),
    Column('b_path', String(2000)),
    Column('b_uuid_path', String(1500)),
    Column('created_at', DateTime),
    Index('components_kee_branch_uuid', 'kee', 'branch_uuid', unique=True)
)


class DefaultQprofile(Base):
    __tablename__ = 'default_qprofiles'

    language = Column(String(20), primary_key=True)
    qprofile_uuid = Column(String(255), nullable=False, unique=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class DeprecatedRuleKey(Base):
    __tablename__ = 'deprecated_rule_keys'
    __table_args__ = (
        Index('uniq_deprecated_rule_keys', 'old_repository_key', 'old_rule_key', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    old_repository_key = Column(String(255), nullable=False)
    old_rule_key = Column(String(200), nullable=False)
    created_at = Column(BigInteger, nullable=False)
    rule_uuid = Column(String(40), nullable=False, index=True)


class DuplicationsIndex(Base):
    __tablename__ = 'duplications_index'
    __table_args__ = (
        Index('duplication_analysis_component', 'analysis_uuid', 'component_uuid'),
    )

    uuid = Column(String(40), primary_key=True)
    analysis_uuid = Column(String(50), nullable=False)
    component_uuid = Column(String(50), nullable=False)
    hash = Column(String(50), nullable=False, index=True)
    index_in_file = Column(Integer, nullable=False)
    start_line = Column(Integer, nullable=False)
    end_line = Column(Integer, nullable=False)


class EsQueue(Base):
    __tablename__ = 'es_queue'

    uuid = Column(String(40), primary_key=True)
    doc_type = Column(String(40), nullable=False)
    doc_id = Column(String(4000), nullable=False)
    doc_id_type = Column(String(20))
    doc_routing = Column(String(4000))
    created_at = Column(BigInteger, nullable=False, index=True)


class EventComponentChange(Base):
    __tablename__ = 'event_component_changes'
    __table_args__ = (
        Index('event_component_changes_unique', 'event_uuid', 'change_category', 'component_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    event_uuid = Column(String(40), nullable=False)
    event_component_uuid = Column(String(50), nullable=False, index=True)
    event_analysis_uuid = Column(String(50), nullable=False, index=True)
    change_category = Column(String(12), nullable=False)
    component_uuid = Column(String(50), nullable=False)
    component_key = Column(String(400), nullable=False)
    component_name = Column(String(2000), nullable=False)
    component_branch_key = Column(String(255))
    created_at = Column(BigInteger, nullable=False)


class Event(Base):
    __tablename__ = 'events'

    uuid = Column(String(40), primary_key=True)
    analysis_uuid = Column(String(50), nullable=False, index=True)
    name = Column(String(400))
    category = Column(String(50))
    description = Column(String(4000))
    event_data = Column(String(4000))
    event_date = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    component_uuid = Column(String(50), nullable=False, index=True)


class ExternalGroup(Base):
    __tablename__ = 'external_groups'
    __table_args__ = (
        Index('uniq_ext_grp_ext_id_provider', 'external_identity_provider', 'external_group_id', unique=True),
    )

    group_uuid = Column(String(40), primary_key=True)
    external_group_id = Column(String(255), nullable=False)
    external_identity_provider = Column(String(100), nullable=False)


class FileSource(Base):
    __tablename__ = 'file_sources'

    uuid = Column(String(40), primary_key=True)
    project_uuid = Column(String(50), nullable=False, index=True)
    file_uuid = Column(String(50), nullable=False, unique=True)
    line_hashes = Column(Text)
    line_hashes_version = Column(Integer)
    data_hash = Column(String(50))
    src_hash = Column(String(50))
    revision = Column(String(100))
    line_count = Column(Integer, nullable=False)
    binary_data = Column(LargeBinary)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False, index=True)


class GithubOrgsGroup(Base):
    __tablename__ = 'github_orgs_groups'

    group_uuid = Column(String(40), primary_key=True)
    organization_name = Column(String(100), nullable=False)


class GroupRole(Base):
    __tablename__ = 'group_roles'
    __table_args__ = (
        Index('uniq_group_roles', 'group_uuid', 'entity_uuid', 'role', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    role = Column(String(64), nullable=False)
    entity_uuid = Column(String(40), index=True)
    group_uuid = Column(String(40))


class Group(Base):
    __tablename__ = 'groups'

    uuid = Column(String(40), primary_key=True)
    name = Column(String(500), nullable=False, unique=True)
    description = Column(String(200))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


t_groups_users = Table(
    'groups_users', metadata,
    Column('group_uuid', String(40), nullable=False, index=True),
    Column('user_uuid', String(255), nullable=False, index=True),
    Index('groups_users_unique', 'user_uuid', 'group_uuid', unique=True)
)


class InternalComponentProp(Base):
    __tablename__ = 'internal_component_props'
    __table_args__ = (
        Index('unique_component_uuid_kee', 'component_uuid', 'kee', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    component_uuid = Column(String(50), nullable=False)
    kee = Column(String(512), nullable=False)
    value = Column(String(4000))
    updated_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)


class InternalProperty(Base):
    __tablename__ = 'internal_properties'

    kee = Column(String(40), primary_key=True)
    is_empty = Column(Boolean, nullable=False)
    text_value = Column(String(4000))
    clob_value = Column(Text)
    created_at = Column(BigInteger, nullable=False)


class IssueChange(Base):
    __tablename__ = 'issue_changes'
    __table_args__ = (
        Index('issue_changes_issue_key_type', 'issue_key', 'change_type'),
    )

    uuid = Column(String(40), primary_key=True)
    kee = Column(String(50), index=True)
    issue_key = Column(String(50), nullable=False, index=True)
    user_login = Column(String(255))
    change_type = Column(String(20))
    change_data = Column(Text)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    issue_change_creation_date = Column(BigInteger)
    project_uuid = Column(String(50), nullable=False, index=True)


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


class IssuesImpact(Base):
    __tablename__ = 'issues_impacts'
    __table_args__ = (
        Index('uniq_iss_key_sof_qual', 'issue_key', 'software_quality', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    issue_key = Column(String(40), nullable=False)
    software_quality = Column(String(40), nullable=False)
    severity = Column(String(40), nullable=False)


class LiveMeasure(Base):
    __tablename__ = 'live_measures'
    __table_args__ = (
        Index('live_measures_component', 'component_uuid', 'metric_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    project_uuid = Column(String(50), nullable=False, index=True)
    component_uuid = Column(String(50), nullable=False)
    metric_uuid = Column(String(40), nullable=False)
    value = Column(Numeric(38, 20))
    text_value = Column(String(4000))
    measure_data = Column(LargeBinary)
    update_marker = Column(String(40))
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class Metric(Base):
    __tablename__ = 'metrics'

    uuid = Column(String(40), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    description = Column(String(255))
    direction = Column(Integer, nullable=False, server_default=text("0"))
    domain = Column(String(64))
    short_name = Column(String(64))
    qualitative = Column(Boolean, nullable=False, server_default=text("false"))
    val_type = Column(String(8))
    enabled = Column(Boolean, server_default=text("true"))
    worst_value = Column(Numeric(38, 20))
    best_value = Column(Numeric(38, 20))
    optimized_best_value = Column(Boolean)
    hidden = Column(Boolean)
    delete_historical_data = Column(Boolean)
    decimal_scale = Column(Integer)


class NewCodePeriod(Base):
    __tablename__ = 'new_code_periods'
    __table_args__ = (
        Index('uniq_new_code_periods', 'project_uuid', 'branch_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    project_uuid = Column(String(40))
    branch_uuid = Column(String(40))
    type = Column(String(30), nullable=False, index=True)
    value = Column(String(255), index=True)
    updated_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    previous_non_compliant_value = Column(String(255))


class NewCodeReferenceIssue(Base):
    __tablename__ = 'new_code_reference_issues'

    uuid = Column(String(40), primary_key=True)
    issue_key = Column(String(50), nullable=False, unique=True)
    created_at = Column(BigInteger, nullable=False)


class Notification(Base):
    __tablename__ = 'notifications'

    uuid = Column(String(40), primary_key=True)
    data = Column(LargeBinary)
    created_at = Column(BigInteger, nullable=False)


class OrgQprofile(Base):
    __tablename__ = 'org_qprofiles'

    uuid = Column(String(255), primary_key=True)
    rules_profile_uuid = Column(String(255), nullable=False, index=True)
    parent_uuid = Column(String(255), index=True)
    last_used = Column(BigInteger)
    user_updated_at = Column(BigInteger)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class PermTemplatesGroup(Base):
    __tablename__ = 'perm_templates_groups'

    uuid = Column(String(40), primary_key=True)
    permission_reference = Column(String(64), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    template_uuid = Column(String(40), nullable=False)
    group_uuid = Column(String(40))


class PermTemplatesUser(Base):
    __tablename__ = 'perm_templates_users'

    uuid = Column(String(40), primary_key=True)
    permission_reference = Column(String(64), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    template_uuid = Column(String(40), nullable=False)
    user_uuid = Column(String(255), nullable=False)


class PermTplCharacteristic(Base):
    __tablename__ = 'perm_tpl_characteristics'
    __table_args__ = (
        Index('uniq_perm_tpl_charac', 'template_uuid', 'permission_key', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    permission_key = Column(String(64), nullable=False)
    with_project_creator = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    template_uuid = Column(String(40), nullable=False)


class PermissionTemplate(Base):
    __tablename__ = 'permission_templates'

    uuid = Column(String(40), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(4000))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    key_pattern = Column(String(500))


class Plugin(Base):
    __tablename__ = 'plugins'

    uuid = Column(String(40), primary_key=True)
    kee = Column(String(200), nullable=False, unique=True)
    base_plugin_key = Column(String(200))
    file_hash = Column(String(200), nullable=False)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    type = Column(String(10), nullable=False)
    removed = Column(Boolean, nullable=False, server_default=text("false"))


class PortfolioProjBranch(Base):
    __tablename__ = 'portfolio_proj_branches'

    uuid = Column(String(40), primary_key=True)
    portfolio_project_uuid = Column(String(40), nullable=False)
    branch_uuid = Column(String(40), nullable=False)
    created_at = Column(BigInteger, nullable=False)


class PortfolioProject(Base):
    __tablename__ = 'portfolio_projects'
    __table_args__ = (
        Index('uniq_portfolio_projects', 'portfolio_uuid', 'project_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    portfolio_uuid = Column(String(40), nullable=False)
    project_uuid = Column(String(40), nullable=False)
    created_at = Column(BigInteger, nullable=False)


class PortfolioReference(Base):
    __tablename__ = 'portfolio_references'
    __table_args__ = (
        Index('uniq_portfolio_references', 'portfolio_uuid', 'reference_uuid', 'branch_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    portfolio_uuid = Column(String(40), nullable=False)
    reference_uuid = Column(String(40), nullable=False)
    created_at = Column(BigInteger, nullable=False)
    branch_uuid = Column(String(255))


class Portfolio(Base):
    __tablename__ = 'portfolios'

    uuid = Column(String(40), primary_key=True)
    kee = Column(String(400), nullable=False, unique=True)
    name = Column(String(2000), nullable=False)
    description = Column(String(2000))
    root_uuid = Column(String(40), nullable=False)
    parent_uuid = Column(String(40))
    private = Column(Boolean, nullable=False)
    selection_mode = Column(String(50), nullable=False)
    selection_expression = Column(String(4000))
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    branch_key = Column(String(255))


class ProjectAlmSetting(Base):
    __tablename__ = 'project_alm_settings'

    uuid = Column(String(40), primary_key=True)
    alm_setting_uuid = Column(String(40), nullable=False, index=True)
    project_uuid = Column(String(50), nullable=False, unique=True)
    alm_repo = Column(String(256))
    alm_slug = Column(String(256), index=True)
    updated_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    summary_comment_enabled = Column(Boolean)
    monorepo = Column(Boolean, nullable=False)


class ProjectBadgeToken(Base):
    __tablename__ = 'project_badge_token'

    uuid = Column(String(40), primary_key=True)
    token = Column(String(255), nullable=False)
    project_uuid = Column(String(40), nullable=False, unique=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class ProjectBranch(Base):
    __tablename__ = 'project_branches'
    __table_args__ = (
        Index('uniq_project_branches', 'branch_type', 'project_uuid', 'kee', unique=True),
    )

    uuid = Column(String(50), primary_key=True)
    project_uuid = Column(String(50), nullable=False, index=True)
    kee = Column(String(255), nullable=False)
    branch_type = Column(String(12), nullable=False)
    merge_branch_uuid = Column(String(50))
    pull_request_binary = Column(LargeBinary)
    manual_baseline_analysis_uuid = Column(String(40))
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    exclude_from_purge = Column(Boolean, nullable=False, server_default=text("false"))
    need_issue_sync = Column(Boolean, nullable=False)
    is_main = Column(Boolean, nullable=False)


class ProjectLink(Base):
    __tablename__ = 'project_links'

    uuid = Column(String(40), primary_key=True)
    project_uuid = Column(String(40), nullable=False, index=True)
    link_type = Column(String(20), nullable=False)
    name = Column(String(128))
    href = Column(String(2048), nullable=False)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class ProjectMeasure(Base):
    __tablename__ = 'project_measures'
    __table_args__ = (
        Index('measures_analysis_metric', 'analysis_uuid', 'metric_uuid'),
    )

    uuid = Column(String(40), primary_key=True)
    value = Column(Numeric(38, 20))
    analysis_uuid = Column(String(50), nullable=False)
    component_uuid = Column(String(50), nullable=False, index=True)
    text_value = Column(String(4000))
    alert_status = Column(String(5))
    alert_text = Column(String(4000))
    person_id = Column(Integer)
    measure_data = Column(LargeBinary)
    metric_uuid = Column(String(40), nullable=False, index=True)


class ProjectQgate(Base):
    __tablename__ = 'project_qgates'
    __table_args__ = (
        Index('uniq_project_qgates', 'project_uuid', 'quality_gate_uuid', unique=True),
    )

    project_uuid = Column(String(40), primary_key=True)
    quality_gate_uuid = Column(String(40), nullable=False)


class ProjectQprofile(Base):
    __tablename__ = 'project_qprofiles'
    __table_args__ = (
        Index('uniq_project_qprofiles', 'project_uuid', 'profile_key', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    project_uuid = Column(String(50), nullable=False)
    profile_key = Column(String(50), nullable=False)


class Project(Base):
    __tablename__ = 'projects'

    uuid = Column(String(40), primary_key=True)
    kee = Column(String(400), nullable=False, unique=True)
    qualifier = Column(String(10), nullable=False, index=True)
    name = Column(String(2000))
    description = Column(String(2000))
    private = Column(Boolean, nullable=False)
    tags = Column(String(500))
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger, nullable=False)
    ncloc = Column(BigInteger)


class Property(Base):
    __tablename__ = 'properties'

    uuid = Column(String(40), primary_key=True)
    prop_key = Column(String(512), nullable=False, index=True)
    is_empty = Column(Boolean, nullable=False)
    text_value = Column(String(4000))
    clob_value = Column(Text)
    created_at = Column(BigInteger, nullable=False)
    entity_uuid = Column(String(40))
    user_uuid = Column(String(255))


class PushEvent(Base):
    __tablename__ = 'push_events'
    __table_args__ = (
        Index('idx_push_even_crea_uuid_proj', 'created_at', 'uuid', 'project_uuid'),
    )

    uuid = Column(String(40), primary_key=True)
    name = Column(String(40), nullable=False)
    project_uuid = Column(String(40), nullable=False)
    payload = Column(LargeBinary, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    language = Column(String(20))


class QgateGroupPermission(Base):
    __tablename__ = 'qgate_group_permissions'

    uuid = Column(String(40), primary_key=True)
    quality_gate_uuid = Column(String(40), nullable=False, index=True)
    group_uuid = Column(String(40), nullable=False)
    created_at = Column(BigInteger, nullable=False)


class QgateUserPermission(Base):
    __tablename__ = 'qgate_user_permissions'

    uuid = Column(String(40), primary_key=True)
    quality_gate_uuid = Column(String(40), nullable=False, index=True)
    user_uuid = Column(String(40), nullable=False)
    created_at = Column(BigInteger, nullable=False)


class QprofileChange(Base):
    __tablename__ = 'qprofile_changes'

    kee = Column(String(40), primary_key=True)
    rules_profile_uuid = Column(String(255), nullable=False, index=True)
    change_type = Column(String(20), nullable=False)
    user_uuid = Column(String(255))
    change_data = Column(Text)
    created_at = Column(BigInteger, nullable=False)


class QprofileEditGroup(Base):
    __tablename__ = 'qprofile_edit_groups'
    __table_args__ = (
        Index('qprofile_edit_groups_unique', 'group_uuid', 'qprofile_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    qprofile_uuid = Column(String(255), nullable=False, index=True)
    created_at = Column(BigInteger, nullable=False)
    group_uuid = Column(String(40), nullable=False)


class QprofileEditUser(Base):
    __tablename__ = 'qprofile_edit_users'
    __table_args__ = (
        Index('qprofile_edit_users_unique', 'user_uuid', 'qprofile_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    qprofile_uuid = Column(String(255), nullable=False, index=True)
    created_at = Column(BigInteger, nullable=False)
    user_uuid = Column(String(255), nullable=False)


class QualityGateCondition(Base):
    __tablename__ = 'quality_gate_conditions'

    uuid = Column(String(40), primary_key=True)
    operator = Column(String(3))
    value_error = Column(String(64))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    metric_uuid = Column(String(40), nullable=False)
    qgate_uuid = Column(String(40), nullable=False)


class QualityGate(Base):
    __tablename__ = 'quality_gates'

    uuid = Column(String(40), primary_key=True)
    name = Column(String(100), nullable=False)
    is_built_in = Column(Boolean, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ReportSchedule(Base):
    __tablename__ = 'report_schedules'
    __table_args__ = (
        Index('uniq_report_schedules', 'portfolio_uuid', 'branch_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    portfolio_uuid = Column(String(40))
    branch_uuid = Column(String(40))
    last_send_time_in_ms = Column(BigInteger, nullable=False)


class ReportSubscription(Base):
    __tablename__ = 'report_subscriptions'
    __table_args__ = (
        Index('uniq_report_subscriptions', 'portfolio_uuid', 'branch_uuid', 'user_uuid', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    portfolio_uuid = Column(String(40))
    branch_uuid = Column(String(40))
    user_uuid = Column(String(40), nullable=False)


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


class RuleRepository(Base):
    __tablename__ = 'rule_repositories'

    kee = Column(String(200), primary_key=True)
    language = Column(String(20), nullable=False)
    name = Column(String(4000), nullable=False)
    created_at = Column(BigInteger, nullable=False)


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


class RulesDefaultImpact(Base):
    __tablename__ = 'rules_default_impacts'
    __table_args__ = (
        Index('uniq_rul_uuid_sof_qual', 'rule_uuid', 'software_quality', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    rule_uuid = Column(String(40), nullable=False)
    software_quality = Column(String(40), nullable=False)
    severity = Column(String(40), nullable=False)


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


class RulesProfile(Base):
    __tablename__ = 'rules_profiles'

    uuid = Column(String(40), primary_key=True)
    name = Column(String(100), nullable=False)
    language = Column(String(20))
    is_built_in = Column(Boolean, nullable=False)
    rules_updated_at = Column(String(100))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SamlMessageId(Base):
    __tablename__ = 'saml_message_ids'

    uuid = Column(String(40), primary_key=True)
    message_id = Column(String(255), nullable=False, unique=True)
    expiration_date = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)


class ScannerAnalysisCache(Base):
    __tablename__ = 'scanner_analysis_cache'

    branch_uuid = Column(String(40), primary_key=True)
    data = Column(LargeBinary, nullable=False)


t_schema_migrations = Table(
    'schema_migrations', metadata,
    Column('version', String(255), nullable=False)
)


class ScimGroup(Base):
    __tablename__ = 'scim_groups'

    scim_uuid = Column(String(40), primary_key=True)
    group_uuid = Column(String(40), nullable=False, unique=True)


class ScimUser(Base):
    __tablename__ = 'scim_users'

    scim_uuid = Column(String(40), primary_key=True)
    user_uuid = Column(String(40), nullable=False, unique=True)


class ScmAccount(Base):
    __tablename__ = 'scm_accounts'

    user_uuid = Column(String(255), primary_key=True, nullable=False)
    scm_account = Column(String(255), primary_key=True, nullable=False, index=True)


class SessionToken(Base):
    __tablename__ = 'session_tokens'

    uuid = Column(String(40), primary_key=True)
    user_uuid = Column(String(255), nullable=False, index=True)
    expiration_date = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class Snapshot(Base):
    __tablename__ = 'snapshots'

    uuid = Column(String(50), primary_key=True)
    root_component_uuid = Column(String(50), nullable=False, index=True)
    status = Column(String(4), nullable=False, server_default=text("'U'::character varying"))
    islast = Column(Boolean, nullable=False, server_default=text("false"))
    version = Column(String(500))
    build_string = Column(String(100))
    revision = Column(String(100))
    analysis_date = Column(BigInteger)
    period1_mode = Column(String(100))
    period1_param = Column(String(100))
    period1_date = Column(BigInteger)
    created_at = Column(BigInteger)
    purged = Column(Boolean, nullable=False)


class UserDismissedMessage(Base):
    __tablename__ = 'user_dismissed_messages'
    __table_args__ = (
        Index('uniq_user_dismissed_messages', 'user_uuid', 'project_uuid', 'message_type', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    user_uuid = Column(String(255), nullable=False)
    project_uuid = Column(String(40), index=True)
    message_type = Column(String(255), nullable=False, index=True)
    created_at = Column(BigInteger, nullable=False)


class UserRole(Base):
    __tablename__ = 'user_roles'

    uuid = Column(String(40), primary_key=True)
    role = Column(String(64), nullable=False)
    entity_uuid = Column(String(40), index=True)
    user_uuid = Column(String(255), index=True)


class UserToken(Base):
    __tablename__ = 'user_tokens'
    __table_args__ = (
        Index('user_tokens_user_uuid_name', 'user_uuid', 'name', unique=True),
    )

    uuid = Column(String(40), primary_key=True)
    user_uuid = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    token_hash = Column(String(255), nullable=False, unique=True)
    last_connection_date = Column(BigInteger)
    created_at = Column(BigInteger, nullable=False)
    type = Column(String(100), nullable=False)
    expiration_date = Column(BigInteger)
    project_uuid = Column(String(40))


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('uniq_external_id', 'external_identity_provider', 'external_id', unique=True),
        Index('uniq_external_login', 'external_identity_provider', 'external_login', unique=True)
    )

    uuid = Column(String(255), primary_key=True)
    login = Column(String(255), nullable=False, unique=True)
    name = Column(String(200))
    email = Column(String(100), index=True)
    crypted_password = Column(String(100))
    salt = Column(String(40))
    hash_method = Column(String(10))
    active = Column(Boolean, server_default=text("true"))
    external_login = Column(String(255), nullable=False)
    external_identity_provider = Column(String(100), nullable=False)
    external_id = Column(String(255), nullable=False)
    user_local = Column(Boolean, nullable=False)
    homepage_type = Column(String(40))
    homepage_parameter = Column(String(40))
    last_connection_date = Column(BigInteger)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger, index=True)
    reset_password = Column(Boolean, nullable=False)
    last_sonarlint_connection = Column(BigInteger)


class WebhookDelivery(Base):
    __tablename__ = 'webhook_deliveries'
    __table_args__ = (
        Index('wd_webhook_uuid_created_at', 'webhook_uuid', 'created_at'),
        Index('wd_ce_task_uuid_created_at', 'ce_task_uuid', 'created_at'),
        Index('wd_project_uuid_created_at', 'project_uuid', 'created_at')
    )

    uuid = Column(String(40), primary_key=True)
    webhook_uuid = Column(String(40), nullable=False)
    project_uuid = Column(String(40), nullable=False)
    ce_task_uuid = Column(String(40))
    analysis_uuid = Column(String(40))
    name = Column(String(100), nullable=False)
    url = Column(String(2000), nullable=False)
    success = Column(Boolean, nullable=False)
    http_status = Column(Integer)
    duration_ms = Column(BigInteger, nullable=False)
    payload = Column(Text, nullable=False)
    error_stacktrace = Column(Text)
    created_at = Column(BigInteger, nullable=False, index=True)


class Webhook(Base):
    __tablename__ = 'webhooks'

    uuid = Column(String(40), primary_key=True)
    project_uuid = Column(String(40))
    name = Column(String(100), nullable=False)
    url = Column(String(2000), nullable=False)
    secret = Column(String(200))
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
