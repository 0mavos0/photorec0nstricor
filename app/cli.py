#!/usr/bin/env python3
import logging
import signal
import sys

from app.recovery import load_settings, start_recovery_process, RecoverySettings
from app.utils import validate_path, validate_numeric_input

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def display_menu() -> None:
    print("\nPhotoRec Automation Settings")
    print("1. Set Recovery Directory")
    print("2. Set PhotoRec Executable Path")
    print("3. Set Session File Path")
    print("4. Set File Count Threshold")
    print("5. Set Size Threshold (in bytes)")
    print("6. Set Minimum File Size (in bytes)")
    print("7. Start PhotoRec")
    print("8. Exit")


def handle_user_choice(settings: RecoverySettings) -> bool:
    while True:
        display_menu()
        choice = input("Please choose an option: ")
        if choice == '1':
            path = input("Enter the path to the recovery directory: ")
            valid, sanitized = validate_path(path, 'directory')
            if valid:
                settings.recovery_directory = sanitized
            else:
                logging.error("Invalid directory path")
        elif choice == '2':
            path = input("Enter the full path to the PhotoRec executable: ")
            valid, sanitized = validate_path(path, 'file')
            if valid:
                settings.photorec_executable = sanitized
            else:
                logging.error("Invalid executable path")
        elif choice == '3':
            path = input("Enter the full path to the PhotoRec session file (photorec.ses): ")
            valid, sanitized = validate_path(path, 'file')
            if valid:
                settings.session_file = sanitized
            else:
                logging.error("Invalid session file path")
        elif choice == '4':
            val = input("Enter the file count threshold for pausing recovery: ")
            valid, num = validate_numeric_input(val)
            if valid:
                settings.file_count_threshold = num
            else:
                logging.error("Invalid number")
        elif choice == '5':
            val = input("Enter the size threshold (in bytes) for pausing recovery: ")
            valid, num = validate_numeric_input(val)
            if valid:
                settings.size_threshold_bytes = num
            else:
                logging.error("Invalid number")
        elif choice == '6':
            val = input("Enter the minimum file size (in bytes) for file retention: ")
            valid, num = validate_numeric_input(val)
            if valid:
                settings.minimum_file_size_bytes = num
            else:
                logging.error("Invalid number")
        elif choice == '7':
            return True
        elif choice == '8':
            return False
        else:
            logging.error("Invalid choice. Please select a valid option.")


def graceful_exit(signum, frame) -> None:
    logging.info("Signal received, exiting.")
    sys.exit(0)


def main() -> None:
    settings = load_settings()
    if handle_user_choice(settings):
        start_recovery_process(settings)
        # Keep main thread alive while recovery runs
        try:
            while True:
                signal.pause()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)
    main()
