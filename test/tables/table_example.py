from alchemist_stack.repository.models import Base
from sqlalchemy import Column, Integer, DateTime


class ExampleTable(Base):
    __tablename__ = 'example'

    primary_key = Column('id', Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return '<Example(timestamp={timestamp})>'.format(timestamp=self.timestamp)