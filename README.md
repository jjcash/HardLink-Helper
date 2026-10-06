# HardLink Helper

A modern desktop utility built with Python and CustomTkinter to batch-create hard links from a source folder (Folder A) to a destination folder (Folder B).

---

## Features

- **Modern Responsive UI**: Built with CustomTkinter supporting system dark/light modes.
- **Directory Pickers**: Intuitive browsing for source and destination directories.
- **File System Safeguards**:
  - **Directory Exclusion**: Only files are linked; sub-directories are excluded by default.
  - **Cross-Drive Prevention**: Verifies that Source and Destination share the same drive/filesystem.
  - **Conflict Handling**: Detects existing files in Folder B, skips them, and prevents overwriting (`[SKIPPED] <filename> already exists. Do not overwrite.`).
- **Advanced Features**:
  - **Dry Run Toggle**: Simulate the batch process without modifying or creating any files.
  - **Extension Filter**: Filter which files get linked (e.g., `*.mp4, *.jpg` or `.txt`).
  - **Recursive Mirroring**: Check "Include Subfolders" to recursively scan Folder A, recreate the directory tree inside Folder B, and link nested files.
  - **Symlink Fallback**: If the cross-drive check fails, a dialog prompts to create soft links (symlinks) instead.
- **Real-Time Logging**: Scrollable console with timestamped status messages (`INFO`, `WARN`, `ERROR`, `SKIPPED`, `SUCCESS`).

---

## Installation & Requirements

Ensure you have Python 3.10+ installed.

```bash
pip install -r requirements.txt
```

---

## Running the Application

Launch the desktop application:

```bash
python main.py
```
