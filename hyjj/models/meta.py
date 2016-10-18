from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.readthedocs.org/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
# 数据库 schema
HYJJ_SCHEMA = 'public'

metadata = MetaData(schema=HYJJ_SCHEMA, naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)

other_metadata = MetaData(naming_convention=NAMING_CONVENTION)
Other = declarative_base(metadata=other_metadata)
