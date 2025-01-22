import os
import datetime
import logging
import platform
import subprocess

class CloudZone:
    def __init__(self, log_file='system_events.log'):
        self.is_windows = platform.system() == 'Windows'
        if not self.is_windows:
            raise EnvironmentError('CloudZone is designed to run on Windows systems only.')
        self.log_file = log_file
        self.setup_logger()
        self.logger.info("CloudZone initialized.")

    def setup_logger(self):
        logging.basicConfig(filename=self.log_file,
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger('CloudZone')
        self.logger.info("Logger setup complete.")

    def track_event_logs(self):
        command = 'wevtutil qe System /f:text /c:10'
        self.logger.info("Running event log query with command: %s", command)
        try:
            event_logs = subprocess.check_output(command, shell=True, text=True)
            self.logger.info("Event logs retrieved successfully.")
            self.save_event_logs(event_logs)
        except subprocess.CalledProcessError as e:
            self.logger.error("Failed to retrieve event logs: %s", e)

    def save_event_logs(self, event_logs):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f'event_logs_{timestamp}.txt'
        with open(log_filename, 'w') as file:
            file.write(event_logs)
        self.logger.info("Event logs saved to %s", log_filename)

    def generate_report(self, output_file='system_report.txt'):
        self.logger.info("Generating system report.")
        try:
            with open(self.log_file, 'r') as file:
                logs = file.readlines()
            with open(output_file, 'w') as report:
                report.write("CloudZone System Event Report\n")
                report.write("Generated on: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
                report.writelines(logs)
            self.logger.info("System report generated and saved as %s", output_file)
        except Exception as e:
            self.logger.error("Failed to generate report: %s", e)

if __name__ == "__main__":
    cloud_zone = CloudZone()
    cloud_zone.track_event_logs()
    cloud_zone.generate_report()