from .database import Database

__author__ = 'H.D. "Chip" McCullough IV'

__database__ = {
  'drivername': 'postgres',
  'host': 'localhost',
  'port': 5432,
  'username': 'postgres',
  'password': 'aG93OTNlbGw',
  'database': 'data'
}

def create_database(*args, **kwargs) -> Database:
  return Database(settings=__database__, *args, **kwargs)