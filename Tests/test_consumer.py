import tempfile
import unittest

from unittest import mock
from unittest.mock import patch
from Common.Utils.Consts import CREATED, DELETED, MOVED, MODIFIED, FILE_PATH, EVENT_TYPE
from Common.Utils.DBUtils import Database
from Services.Consumer.HandleMessage import HandleMessage


class TestConsumer(unittest.TestCase):
    @patch('Services.Consumer.HandleMessage.HandleMessage._log')
    def setUp(self, mock_log):
        self.db_connection = mock.MagicMock(spec=Database)
        self.handle_message = HandleMessage(self.db_connection)

    @patch('os.rename')
    @patch('Services.Consumer.HandleMessage.HandleMessage._log')
    def test_dup_file_created_event(self, mock_os_rename, mock_log):
        message = {
            FILE_PATH: "/path/to/file.txt",
            EVENT_TYPE: CREATED
        }
        self.db_connection.is_file_exists_in_db.return_value = False
        self.db_connection.get_original_md5_file_from_db.return_value = ('test.txt', None)

        with mock.patch("Services.Consumer.HandleMessage.HandleMessage._calculate_hash") as md5_hash_func:
            md5_hash_func.return_value = '1234'
            self.handle_message.handle(message)

        self.db_connection.is_file_exists_in_db.assert_called_once_with("/path/to/file.txt")
        self.db_connection.get_original_md5_file_from_db.assert_called_once()
        mock_log.assert_called_once_with("/path/to/file.txt", 'test_DUP_1.txt')

    @patch('Services.Consumer.HandleMessage.HandleMessage._log')
    def test_new_file_created_event(self, mock_log):
        message = {
            FILE_PATH: "/path/to/file.txt",
            EVENT_TYPE: CREATED
        }
        self.db_connection.is_file_exists_in_db.return_value = False
        self.db_connection.get_original_md5_file_from_db.return_value = None

        with mock.patch("Services.Consumer.HandleMessage.HandleMessage._calculate_hash") as md5_hash_func:
            md5_hash_func.return_value = '1234'
            self.handle_message.handle(message)

        self.db_connection.is_file_exists_in_db.assert_called_once_with("/path/to/file.txt")
        self.db_connection.get_original_md5_file_from_db.assert_called_once()
        mock_log.assert_called_once_with("/path/to/file.txt", CREATED)

    @patch('Services.Consumer.HandleMessage.HandleMessage._log')
    def test_handle_created_event_file_exists(self, mock_log):
        message = {
            FILE_PATH: "/path/to/file.txt",
            EVENT_TYPE: CREATED
        }
        self.db_connection.get_original_md5_file_from_db.return_value = None

        with mock.patch("builtins.print") as mock_print:
            self.handle_message.handle(message)

        self.db_connection.is_file_exists_in_db.assert_called_once_with("/path/to/file.txt")
        self.db_connection.get_original_md5_file_from_db.assert_not_called()
        self.db_connection.insert_file.assert_not_called()
        self.db_connection.log_current_db_status.assert_not_called()
        mock_print.assert_called_once_with("This specific file already exists in db")
        mock_log.assert_not_called()

    @patch('Services.Consumer.HandleMessage.HandleMessage._log')
    def test_handle_deleted_event(self, mock_log):
        message = {
            FILE_PATH: "/path/to/file.txt",
            EVENT_TYPE: DELETED
        }
        self.db_connection.delete_file.return_value = None

        self.handle_message.handle(message)

        self.db_connection.delete_file.assert_called_once_with("/path/to/file.txt")
        mock_log.assert_called_once_with("/path/to/file.txt", DELETED)

    @patch('Services.Consumer.HandleMessage.HandleMessage._log')
    def test_handle_modified_event(self, mock_log):
        message = {
            FILE_PATH: "/path/to/file.txt",
            EVENT_TYPE: MODIFIED
        }

        self.handle_message.handle(message)

        self.db_connection.delete_file.assert_not_called()
        mock_log.assert_called_once_with("/path/to/file.txt", f"{MODIFIED}/{MOVED}")

    def test_md5_hash(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(b'test')
            temp_file.flush()
            result = HandleMessage(None)._calculate_hash(temp_file.name)
            assert result == '098f6bcd4621d373cade4e832627b4f6'
