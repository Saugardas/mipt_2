import psycopg2
from contextlib import contextmanager

class PgLogger:
    """
    Класс для работы с БД - запись/чтение
    """
    def __init__(self):
        self.conn = None

    def connect(self, **kwargs):
        self.conn = psycopg2.connect(**kwargs)
    
    # используем чтобы в остальном коде постоянно не делать явный .commit()/.close()
    @contextmanager
    def cursor(self):
        if not self.conn:
            raise RuntimeError("Нет соединения с БД")
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def close(self):
        if self.conn:
            self.conn.close()

db = PgLogger()