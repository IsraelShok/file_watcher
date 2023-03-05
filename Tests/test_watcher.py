import tempfile
import threading
import time
import unittest
import os

from unittest.mock import patch

from Common.Utils.Consts import CREATED
from Services.Watcher.main import Watcher


class TestWatcher(unittest.TestCase):
    @patch('os.getenv')
    def setUp(self, mock_os_getenv):
        self.tempdir = tempfile.mkdtemp()
        mock_os_getenv.return_value = self.tempdir
        self.watcher = Watcher()

    @patch('Services.Watcher.HandleEvent.HandleEvent.send_message')
    def test_observer(self, mock_send_message):
        test_file_path = os.path.join(self.tempdir, "test_file.txt")
        stop_threads = False
        thread = threading.Thread(target=self.watcher.start, args=(lambda: stop_threads, ))
        thread.start()

        try:
            # Wait for a few seconds for the Watcher to start watching the folder
            time.sleep(3)

            # Create a test file in the watched folder
            with open(test_file_path, "w") as f:
                f.write("test")

            # Wait for a few seconds for the file to be processed by the Watcher
            time.sleep(3)

            # Assert that the file was created correctly
            # mock_send_message.assert_called_with(os.path.join(self.tempdir, "test_file.txt"), CREATED)
            assert self.tempdir in mock_send_message.call_args_list[0].args[0]
            assert mock_send_message.call_args_list[0].args[1] == CREATED

        finally:
            # Stop the Watcher and wait for the thread to exit
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
            stop_threads = True
            thread.join()
