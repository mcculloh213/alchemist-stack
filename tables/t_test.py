from sqlalchemy import Column, Integer, DateTime
from alchemist_stack.repository.models import Base

__author__ = 'H.D. "Chip" McCullough IV'

class TestTable(Base):
    __tablename__ = 'test'

    primary_key = Column('id', Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return '<Test(timestamp={timestamp})>'.format(timestamp=self.timestamp)