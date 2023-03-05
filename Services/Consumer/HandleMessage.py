import hashlib
import os
import time

from dotenv import load_dotenv

from Common.Utils.Consts import (CREATED, DELETED, EVENT_TYPE, FILE_PATH, FILES_FOLDER, MODIFIED, MOVED, LOGS)
from Common.Utils.DBUtils import Database
from Common.Utils.Decorators import retry
from Common.Utils.Logger import log

load_dotenv()


class HandleMessage:
    def __init__(self, db_connection: Database):
        self.db_connection = db_connection
        self.logger_path = os.path.join(os.getenv(FILES_FOLDER), LOGS)
        print(f'watch folder: {self.logger_path}')

    def handle(self, message: dict):
        filepath = message[FILE_PATH]
        time.sleep(1)

        # Handle the message according to the event type
        if message[EVENT_TYPE] == CREATED:
            if not self.db_connection.is_file_exists_in_db(filepath):
                self.handle_new_file(filepath)
            else:
                # Handle cases that modified file fire create event
                print('This specific file already exists in db')

        elif message[EVENT_TYPE] == DELETED:
            self._delete_file(filepath)
            self._log(filepath, DELETED)

        elif message[EVENT_TYPE] in (MOVED, MODIFIED):
            # TODO check case that the md5 changed to exists file
            self._log(filepath, f"{MODIFIED}/{MOVED}")

    def _add_file(self, filepath: str, md5_hash: str):
        # Check if a file with the same hash exists in the database
        original_file = self.db_connection.get_original_md5_file_from_db(md5_hash)

        if original_file is not None:
            new_file_name = self._handle_duplicate_file(original_file, filepath)
            self._log(filepath, f'Changed to {new_file_name} dou to duplicate hash')
        else:
            # Insert the file details into the database
            self.db_connection.insert_file(filepath, md5_hash)
            self._log(filepath, CREATED)

    def _delete_file(self,  filepath: str):
        # Delete the record from the database
        self.db_connection.delete_file(filepath)

    def _log(self, filepath, message):
        log(filepath, message, self.logger_path)
        self.db_connection.log_current_db_status(self.logger_path)

    @retry
    def _calculate_hash(self, filepath: str):
        block_size = 65536
        hasher = hashlib.md5()

        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                buf = f.read(block_size)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(block_size)
            return hasher.hexdigest()
        else:
            print(f"file not found {filepath}")
        return None

    def handle_new_file(self, filepath):
        try:
            # Generate MD5 hash for the file
            md5_hash = self._calculate_hash(filepath)
            if md5_hash:
                self._add_file(filepath, md5_hash)
        except IsADirectoryError:
            # Handle some cases that new dir creating event
            return

    def _handle_duplicate_file(self, original_file: tuple, filepath: str) -> str:
        original_name, dup_num = original_file
        dup_num = 1 if dup_num is None else dup_num + 1

        # A file with the same hash exists in the database, so rename the file
        self.db_connection.update_original_file_with_new_dup_num(original_name, dup_num)
        new_filepath = f"{os.path.splitext(original_name)[0]}_DUP_{dup_num}{os.path.splitext(filepath)[1]}"

        os.rename(filepath, new_filepath)
        print(f'File {filepath} renamed to {new_filepath} due to duplicate content.')
        return new_filepath
