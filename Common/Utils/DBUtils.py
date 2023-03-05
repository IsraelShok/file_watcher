import os
import psycopg2
from dotenv import load_dotenv
from Common.Utils.Consts import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE, DB_PORT
from Common.Utils.Logger import log_table


class Database:
    def __init__(self, host: str = None, username: str = None, password: str = None, database: str = None):
        load_dotenv()

        self.conn = psycopg2.connect(
            port=os.getenv(DB_PORT),
            host=host or os.getenv(DB_HOST),
            user=username or os.getenv(DB_USERNAME),
            password=password or os.getenv(DB_PASSWORD),
            dbname=database or os.getenv(DB_DATABASE)
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            file_name VARCHAR(255),
            md5 VARCHAR(32),
            dup_num INT, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def drop_table(self):
        create_table_query = '''
        DROP TABLE files
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_file(self, file_name, md5_hash):
        insert_query = f"INSERT INTO files (file_name, md5) VALUES ('{file_name}', '{md5_hash}')"
        self.cursor.execute(insert_query)
        self.conn.commit()

    def delete_file(self, file_path):
        delete_query = f"DELETE FROM files WHERE file_name='{file_path}'"
        self.cursor.execute(delete_query)
        self.conn.commit()

    def delete_all_files(self):
        delete_query = f"DELETE FROM files"
        self.cursor.execute(delete_query)
        self.conn.commit()

    def get_original_md5_file_from_db(self, md5):
        query = f"SELECT file_name, dup_num FROM files WHERE md5='{md5}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def is_file_exists_in_db(self, file_name):
        query = f"SELECT * FROM files WHERE file_name='{file_name}'"
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None

    def close(self):
        self.cursor.close()
        self.conn.close()

    def update_original_file_with_new_dup_num(self, file_name, new_dup_number):
        query = f"UPDATE files SET dup_num = {new_dup_number} WHERE file_name='{file_name}'"
        self.cursor.execute(query)

    def log_current_db_status(self, logger_path):
        query = f"SELECT * from files"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        log_table(rows, logger_path)


if __name__ == '__main__':
    db = Database()
    db.close()
