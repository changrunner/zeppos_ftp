import ftplib
import os
import time
from zeppos_logging.app_logger import AppLogger
from datetime import datetime


class Ftp:
    @staticmethod
    def download_files(FTP_HOST, FTP_PORT, FTP_DIRECTORY, FTP_USER, FTP_PASS, DESTINATION_FILE_DIR,
                       add_time_stamp=True, delete_files_on_ftp=False, max_attempts=5,
                       attempt_wait_period_in_minutes=5):
        success_state = False
        AppLogger.logger.info("Downloading files from FTP")
        num_attempts = 0

        while not success_state:
            success_state = Ftp._pull_files(
                FTP_HOST, FTP_PORT, FTP_DIRECTORY, FTP_USER, FTP_PASS,
                DESTINATION_FILE_DIR, add_time_stamp, delete_files_on_ftp
            )

            if success_state:
                AppLogger.logger.info(f"Ftp download was successful.")
            elif num_attempts >= max_attempts:
                AppLogger.logger.info(
                    f"We are unable to get files from the ftp. Max Attempt of [{max_attempts}] has been reached")
                success_state = True
            else:
                num_attempts += 1
                AppLogger.logger.info(f'Could not get ftp files successfully. Attempt No: [{num_attempts}]. '
                                      f'Waiting {attempt_wait_period_in_minutes} minutes')
                time.sleep(60 * attempt_wait_period_in_minutes)

    @staticmethod
    def _pull_files(FTP_HOST, FTP_PORT, FTP_DIRECTORY, FTP_USER, FTP_PASS, DESTINATION_FILE_DIR,
                    add_time_stamp, delete_files_on_ftp):
        AppLogger.logger.info('Entering pull_files')

        success_state = False
        try:
            ftp = ftplib.FTP()
            ftp.connect(host=FTP_HOST, port=21)
            ftp.login(user=FTP_USER, passwd=FTP_PASS)

            file_list = ftp.nlst(FTP_DIRECTORY)

            AppLogger.logger.info(f"Ftp file list: {file_list}")
            AppLogger.logger.info(f'num ftp files: {len(file_list)}')

            for filename in file_list:

                if add_time_stamp:
                    file_name = f"{datetime.today().strftime('%Y_%m_%d_%H_%M_%S')}_{os.path.basename(filename)}"
                else:
                    file_name = os.path.basename(filename)
                full_file_name = os.path.join(os.path.join(DESTINATION_FILE_DIR), file_name)

                AppLogger.logger.info(f"Saving file [{os.path.basename(filename)}] to [{full_file_name}]")

                os.makedirs(DESTINATION_FILE_DIR, exist_ok=True)
                with open(full_file_name, 'wb') as f:
                    ftp.retrbinary("RETR " + filename, f.write)

                AppLogger.logger.info(f"Got ftp file {filename}")

                if delete_files_on_ftp:
                    AppLogger.logger.info(f"deleting file from ftp site: {filename}")
                    # ftp.delete(filename)

            ftp.close()

            success_state = True
        except Exception as error:
            AppLogger.logger.error(f"Error getting files from the ftp server: {error}")

        AppLogger.logger.info('Exiting pull_files')

        return success_state
