from pathlib import Path


def validate_file_path(file_path: Path):
    return file_path.exists() and file_path.is_file()
