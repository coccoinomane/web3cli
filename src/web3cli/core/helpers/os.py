import os


def create_folder(dir: str, mode: int = 0o777) -> None:
    """Create a folder and all its parent folders, if they do not
    exist"""
    expanded_dir = os.path.expanduser(dir)
    if not os.path.isdir(expanded_dir):
        os.makedirs(expanded_dir, mode)
        os.chmod(expanded_dir, mode)  # for good measure
