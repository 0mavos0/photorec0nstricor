# photorec0nstricor

This repository provides a simple utility script for running PhotoRec while
backing up the `photorec.ses` session file and monitoring the recovery
folder. The script creates up to five backups of the session file and can
optionally prune recovered files below a size threshold while PhotoRec runs.

## Usage

1. Ensure [`pexpect`](https://pypi.org/project/pexpect/) is installed.
2. Run `python recovery.py` and provide the requested paths and settings.

The script will start PhotoRec using the supplied session file, periodically
check the recovery directory, and delete small files when necessary.
