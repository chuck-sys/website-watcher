"""
Read and write to the cache directory and get string back.
"""
import os
from config import WatcherConfig


class WatcherCache:
    """Handle calls to get and set data, as files on disk."""

    def __init__(self, config: WatcherConfig):
        """Create the directory if it doesn't already exist."""
        self.basedir = os.path.dirname(__file__)
        self.cachedir = os.path.join(self.basedir, config.cache_dir)

        if not os.path.exists(self.cachedir):
            os.makedirs(self.cachedir)

    def __getitem__(self, key: str) -> str:
        """
        Get file content associated with key.

        Raises KeyError if no key associated can be found.
        """
        filename = self.key_to_filename(key)

        try:
            with open(filename, 'r') as item:
                return item.read().strip()
        except FileNotFoundError:
            raise KeyError(f'File associated with key `{key}` not found')

    def __setitem__(self, key: str, contents: str):
        """Sets file content associated with key."""
        filename = self.key_to_filename(key)

        with open(filename, 'w') as item:
            item.write(contents.strip())

    def key_to_filename(self, key: str) -> str:
        """Converts the key into a filename."""
        filename = f'{key}.cache'
        return os.path.join(self.cachedir, filename)
