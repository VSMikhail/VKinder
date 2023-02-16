import psycopg2
from Tokens import db_password


def conn():
    """Функция создает подключение к БД."""
    with psycopg2.connect(dbname='vkinder', user='postgres', password=db_password) as conn:
        pass
        return conn


class Database:
    def __init__(self, conn):
        self.conn = conn

    def delete_table(self):
        """Метод удаляет таблицу."""
        with self.conn.cursor() as cur:
            cur.execute("""
            DROP TABLE match;
            """)

            self.conn.commit()

    def create_table(self):
        """Метод создает таблицу."""
        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS match(
                id SERIAL PRIMARY KEY,
                user_id INT,
                match_id INT
            );
            """)
            self.conn.commit()

    def add_match(self, user_id: int, match_id: int):
        """Метод добавляет строку."""
        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO match (user_id, match_id)
            VALUES(%s, %s);
            """, (user_id, match_id))
            self.conn.commit()

    def select_match(self, user_id: int):
        """Метод выделяет все совпадения по ID."""
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT match_id FROM match
            WHERE user_id = %s;
            """, (user_id, ))
            response = cur.fetchall()
        match_select = []
        for _ in response:
            match_select.append(_[0])
        return match_select
