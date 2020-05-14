"""
File for the actual entries we get.
"""
from typing import Dict, Tuple
from urllib import request
from difflib import HtmlDiff
import xml.dom.minidom as minidom

from config import WatcherConfig
from cache import WatcherCache

class Entries:
    """
    A collection of entries (key, url, formatted_content).

    Content formatted based on lxml prettifier for better diffs.
    """

    def __init__(self, config: WatcherConfig, cache: WatcherCache,
                 csvfile: str):
        """
        Initialize all entries.

        1. Read given CSV file and populates basic information
        2. Goes to the URLs and scrapes data into entries
        3. Goes to cache and puts data into entries

        Entries without cache data or have bad URL responses (404, 500, etc)
        will be `None`.
        """
        self.cache = cache
        # Internal entry representation: {url, current_content, cached_content}
        self.entries = {}

        # Read given CSV file
        try:
            with open(csvfile, 'r') as cf:
                for line in cf.readlines():
                    line = line.strip().split(',')
                    self.entries[line[0]] = {'url': line[1]}
        except FileNotFoundError:
            pass

        # Scrape URLs and grab cache
        for name, d in self.entries.items():
            content = Entries.get_content(d['url'])
            try:
                xml = minidom.parseString(content)
                content = xml.toprettyxml(indent='  ')
            except:
                # There's a small chance that the HTML isn't well formed. And
                # in that case, we sigh and be unhappy.
                pass
            self.entries[name]['current_content'] = content.strip()
            # We don't need to parse cache because by default it should have
            # been pretty beforehand
            self.entries[name]['cached_content'] = cache[name]

    @staticmethod
    def get_content(url: str):
        """Get the string content for a given URL, or None if error."""
        try:
            resp = request.urlopen(url)
            if resp.getcode() != 200:
                return None

            return resp.read().decode('utf-8')
        except:
            return None

    def get_comparison(self) -> Dict[str, str]:
        """
        Get a comparison object for use in sending emails.

        We have the name (key) -> HTML diff table (value).
        """
        diff = HtmlDiff(tabsize=4, wrapcolumn=80)
        return {name: (diff.make_table(v['cached_content'].split('\n'),
                                       v['current_content'].split('\n'),
                                       context=True),
                       v['url'])
                for name, v in self.entries.items()
                if v['cached_content'] is not None and
                v['current_content'] is not None and
                v['cached_content'] != v['current_content']}

    def write_to_cache(self):
        """Write current_content for all entries into cache."""
        for name, val in self.entries.items():
            self.cache[name] = val['current_content']
