# Folder Synchronization Script

This Python script ensures that the contents of a source folder are replicated exactly in a destination folder. It performs one-way synchronization, meaning any changes in the source folder are mirrored in the destination folder at regular intervals.

## Features

- **One-way Synchronization**: Mirrors the source folder to the destination folder.
- **Regular Intervals**: Performs synchronization at user-defined intervals.
- **Logging**: Records all operations, including file additions, updates, and deletions.

## Prerequisites

- Python 3.x

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/folder-sync-script.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd folder-sync-script
   ```

3. **Install Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command-line arguments:

- `--source`: Path to the source folder.
- `--replica`: Path to the destination folder.
- `--interval`: Synchronization interval in seconds.
- `--log`: Path to the log file.

**Example**:


```bash
python sync_folders.py --source /path/to/source --replica /path/to/replica --interval 60 --log sync.log
```

This command synchronizes the source folder with the replica folder every 60 seconds and logs the operations to `sync.log`.

## References

This project was inspired by the following resources:

- [How to synchronize two folders using python script - Stack Overflow](https://stackoverflow.com/questions/54688687/how-to-synchronize-two-folders-using-python-script)
- [Syncing Folders With Python : 5 Steps - Instructables](https://www.instructables.com/Syncing-Folders-With-Python/)
- [Synchronizing Files Between Two Directories Using Python - Dev.to](https://dev.to/devasservice/synchronizing-files-between-two-directories-using-python-19li)
