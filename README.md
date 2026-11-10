# File Integrity Monitor
A lightweight CLI tool written in Python that tracks and detects unauthorized modifications to files in a given directory using MD5 cryptographic hashing.

## Features

- **Memory Efficient:** Processes files in 64KB chunks to maintain a minimal RAM footprint, allowing safe hashing of large files.
- **Recursive Directory Scanning:** Monitors all files and nested subdirectories using relative paths.
- **Mutually Exclusive CLI:** Uses Python's `argparse` to enforce clear execution modes (`--save` vs. `--check`).
- **Tkinter Integration:** Opens a native GUI directory selector when saving a new baseline.

## Prerequisites

- Python 3.8+ (uses the walrus operator `:=` for chunked reads)
- Standard library modules only (`os`, `hashlib`, `json`, `argparse`, `pathlib`, `tkinter`)

## Usage

### 1. Save a Baseline
Select a directory to hash and save its baseline state by running:

python3 fim.py --save
(A folder selection window will open. Select the directory you want to monitor. The file hashes and selected path will be saved to data.json and path.json.)

2. Check Integrity
Compare the current state of the directory against the saved baseline by running:

python3 fim.py --check
Output Meanings:

Files Remain Unchanged: Returned if all monitored files match the baseline.

Files Have Been Altered: Returned if one or more files have been modified, deleted, or added.

Missing JSON file, please run with --save first: Returned if --check is executed before running --save.

File hashes have been saved, validate file integrity with --check: Returned if files are sucessfully saved as hashes

File hashes have not been saved: Returned if the file selection GUI is closed without a file being selected.

How It Works
Initialization: Automatically creates data.json and path.json if they do not exist.

Chunked Hashing: Opens each file in binary mode ('rb') and reads 64KB blocks via a while loop to feed the hashlib.md5() digest incrementally.

State Comparison: Maps file paths to their respective hash strings in a dictionary, comparing the dictionary against the saved baseline JSON data.
