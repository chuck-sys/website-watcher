"""
Configuration system.
"""


class WatcherConfig:
    def __init__(self, d):
        self.sendgrid_api = d['SENDGRID_KEY']
        self.cache_dir = d['CACHE_DIR']
