"""Utility script for running PhotoRec with session backups and recovery monitoring."""

import glob
import os
import shutil
import signal
import time
from typing import Tuple

import pexpect


def backup_ses_file(photorec_ses_path: str) -> None:
    """Back up ``photorec.ses`` keeping the last five versions.

    Parameters
    ----------
    photorec_ses_path:
        Path to the ``photorec.ses`` file used by PhotoRec.
    """
    backup_dir = os.path.join(os.path.dirname(photorec_ses_path), "ses_backups")
    os.makedirs(backup_dir, exist_ok=True)

    existing_backups = sorted(glob.glob(os.path.join(backup_dir, "photorec.ses.bak*")))

    while len(existing_backups) >= 5:
        os.remove(existing_backups.pop(0))

    if existing_backups:
        last_backup = existing_backups[-1]
        next_num = int(last_backup.split(".bak")[-1]) + 1
    else:
        next_num = 1

    new_backup_path = os.path.join(backup_dir, f"photorec.ses.bak{next_num}")
    shutil.copy(photorec_ses_path, new_backup_path)
    print(f"Backup created: {new_backup_path}")


def filter_and_delete_files(directory: str, size_threshold_mb: float) -> None:
    """Delete files smaller than ``size_threshold_mb`` from ``directory``."""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            if size_mb < size_threshold_mb:
                os.remove(filepath)
                print(f"Deleted {filename}: Size below threshold")


def monitor_recovery_dir(
    recovery_directory: str,
    file_threshold: int,
    size_threshold_mb: float,
    child_process: pexpect.spawn,
) -> None:
    """Monitor ``recovery_directory`` and prune files while PhotoRec runs."""
    while True:
        try:
            files = [
                f
                for f in os.listdir(recovery_directory)
                if os.path.isfile(os.path.join(recovery_directory, f))
            ]
            if len(files) >= file_threshold:
                print(f"Threshold of {file_threshold} files reached. Pausing recovery to filter files.")
                os.kill(child_process.pid, signal.SIGSTOP)
                filter_and_delete_files(recovery_directory, size_threshold_mb)
                os.kill(child_process.pid, signal.SIGCONT)
                print("Resuming recovery process.")
            time.sleep(5)
        except Exception as exc:  # pragma: no cover - runtime safety
            print(f"Monitoring error: {exc}")
            break


def start_photorec(photorec_executable: str, photorec_ses_path: str) -> pexpect.spawn:
    """Spawn PhotoRec using ``pexpect``."""
    backup_ses_file(photorec_ses_path)
    cmd = f"{photorec_executable} /cmd {photorec_ses_path}"
    return pexpect.spawn(cmd, encoding="utf-8")


def get_user_input() -> Tuple[str, str, str, int, float]:
    """Prompt for required runtime parameters."""
    recovery_directory = input("Recovery directory: ")
    photorec_executable = input("Path to photorec executable: ")
    photorec_ses_path = input("Path to photorec.ses: ")
    file_threshold = int(input("File threshold before filtering: "))
    size_threshold_mb = float(input("Minimum file size to keep (MB): "))
    return (
        recovery_directory,
        photorec_executable,
        photorec_ses_path,
        file_threshold,
        size_threshold_mb,
    )


def main() -> None:
    args = get_user_input()
    recovery_directory, photorec_executable, photorec_ses_path, file_threshold, size_threshold_mb = args
    child = start_photorec(photorec_executable, photorec_ses_path)
    print(f"PhotoRec process started with PID: {child.pid}")
    monitor_recovery_dir(recovery_directory, file_threshold, size_threshold_mb, child)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - runtime wrapper
        print(f"Error: {exc}")
