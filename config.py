"""
Configuration system.
"""


class WatcherConfig:
    def __init__(self, d):
        self.sendgrid_api = d['SENDGRID_KEY']
        self.cache_dir = d['CACHE_DIR']
        self.to_email = d['TO_EMAIL']
        self.from_email = d['FROM_EMAIL']
