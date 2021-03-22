#!/usr/bin/env python3
import requests
from pathlib import Path
import yaml
from loguru import logger
from bs4 import BeautifulSoup


class SiteStalker:
    def __init__(self, config_file, content_dir=None):
        self.root_dir = Path(__file__).resolve().parent.parent
        if content_dir:
            self.content_dir = Path(content_dir)
        else:
            self.content_dir = self.root_dir.joinpath('content')
        self.config = yaml.safe_load(config_file.open())
        self.monitor_dict = {k: v for (k, v) in self.config['sites'].items()}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Pragma': 'no-cache', 'Cache-Control': 'no-cache'
        }

    def _log(self, _level, msg):
        static_info = 'audit=site_stalker '
        logger.log(_level.upper(), static_info + msg)

    def process_html(self, string):
        soup = BeautifulSoup(string, features="lxml")

        # make the html look good
        soup.prettify()

        # remove script tags
        for s in soup.select('script'):
            s.extract()

        # remove meta tags
        for s in soup.select('meta'):
            s.extract()

        # convert to a string, remove '\r', and return
        return str(soup).replace('\r', '')

    def get_website(self, _site):
        response = requests.get(_site, headers=self.headers)
        if response.status_code < 300:
            self._log('info', f'action=get_website event=website_retrieved website={_site}')
            return response.text
        self._log('error', f'action=get_website event=website_not_retrieved website={_site} '
                           f'http_code={response.status_code} http_text="{response.text}"')
        return ''

    def compare_websites(self):
        for _alias, _site in self.monitor_dict.items():
            yield self.compare_current_and_previous_sites(_alias, self.get_website(_site))

    def compare_current_and_previous_sites(self, site_alias, site_text):
        """Returns true if the webpage was changed, otherwise false."""
        site_content_file = self.content_dir.joinpath(f'{site_alias}.html')
        processed_site_html = self.process_html(site_text)
        # create the site_file if it doesn't exist, return False because page did not technically change
        if not site_content_file.exists():
            site_content_file.touch()
            with open(site_content_file, 'w') as site_file_writer:
                site_file_writer.write(processed_site_html)
            self._log('info', 'action=check_if_site_file_exists event=site_file_does_not_exist '
                              'action=creating_site_file_and_returning_false')
            return False

        with open(site_content_file) as site_file_reader:
            previous_response_html = site_file_reader.read()

        if processed_site_html == previous_response_html:
            self._log('info', f'action=compare_current_and_previous_sites event=sites_match site_alias={site_alias}')
            return False
        else:
            self._log('success', f'action=compare_current_and_previous_sites event=sites_do_not_match'
                              f' site_alias={site_alias}')
            with open(site_content_file, 'w') as site_file_writer:
                site_file_writer.write(processed_site_html)
            return True
