from .context import Context

__author__ = 'H.D. "Chip" McCullough IV'

__settings__ = {
  'drivername': '',
  'host': '',
  'port': 0,
  'username': '',
  'password': '',
  'database': ''
}

def set_settings(drivername: str, host: str, port: int, username: str, password: str, database: str):
  __settings__.update({
    'drivername': drivername,
    'host': host,
    'port': port,
    'username': username,
    'password': password,
    'database': database
  })

def create_context(*args, **kwargs) -> Context:
  return Context(settings=__settings__, *args, **kwargs)