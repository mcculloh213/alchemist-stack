from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base

from typing import TypeVar

B = TypeVar('B', bound='Base')
Base = declarative_base()

def create_tables(engine: Engine):
    Base.metadata.create_all(engine)
