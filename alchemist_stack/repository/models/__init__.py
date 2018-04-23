from sqlalchemy import Column, PrimaryKeyConstraint, Table
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.base import declared_attr

from typing import TypeVar

B = TypeVar('B', bound='Base')
Base = declarative_base()

def create_tables(engine: Engine):
    Base.metadata.create_all(engine)

# class AutoTable(object):
#     @classmethod
#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__
#
#     @classmethod
#     def __table_cls__(cls, *args, **kwargs):
#         for obj in args[1:]:
#             if (isinstance(obj, Column) and obj.primary_key) \
#                     or (isinstance(obj, PrimaryKeyConstraint)):
#                 return Table(*args, **kwargs)
#
#         return None