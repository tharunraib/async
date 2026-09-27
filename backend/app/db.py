import os
from contextlib import contextmanager
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rootcause:rootcause@localhost:5432/rootcause")

@contextmanager
def connection():
    with psycopg.connect(DATABASE_URL) as conn:
        yield conn
