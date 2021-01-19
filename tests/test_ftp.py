import unittest
from zeppos_ftp.ftp import Ftp
import os
import shutil

# Start the ftp_server before running test tests

class TestTheProjectMethods(unittest.TestCase):
    def test_download_files_methods(self):
        if os.path.exists(r"c:\data\ftpclient"):
            shutil.rmtree(r"c:\data\ftpclient")
        os.makedirs(r"c:\data\ftpclient", exist_ok=True)
        Ftp.download_files(
            FTP_HOST="127.0.0.1",
            FTP_PORT="21",
            FTP_DIRECTORY="/",
            FTP_USER="user",
            FTP_PASS="12345",
            DESTINATION_FILE_DIR=r"c:\data\ftpclient"
        )
        file_count = sum(len(files) for _, _, files in os.walk(r"c:\data\ftpclient"))
        self.assertEqual(1, file_count)
        shutil.rmtree(r"c:\data\ftpclient")


if __name__ == '__main__':
    unittest.main()
