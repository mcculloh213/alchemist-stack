from .context import Context

__author__ = 'H.D. "Chip" McCullough IV'

__settings__ = {
  'drivername': 'postgres',
  'host': 'localhost',
  'port': 5432,
  'username': 'postgres',
  'password': 'aG93OTNlbGw',
  'database': 'data'
}

def create_context(*args, **kwargs) -> Context:
  return Context(settings=__settings__, *args, **kwargs)