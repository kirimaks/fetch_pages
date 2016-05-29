# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from scrapy.http import Request
from urlparse import urlparse

exclude_url = re.compile(r'(jpg|png|gif)$', flags=re.IGNORECASE)
include_url = re.compile(r'^[\w\/]{2,}')


def validate_url(link):
    """ Checking if the link is valid. """

    if not exclude_url.search(link):
        if include_url.match(link):
            return True

    return False


class SomeSpider(scrapy.Spider):
    name = "myspider"

    start_ruls = []

    def __init__(self, url=None, *kargs, **pargs):
        assert url, "Need to set a url."

        scrapy.Spider.__init__(self, *kargs, **pargs)

        self.start_urls.append(url)

        # Save netloc.
        parser = urlparse(url)
        self.netloc = "{}://{}/".format(parser.scheme, parser.netloc)

    def parse(self, response):
        link_list = set()

        # Prepare links (get unique links, and skip some links).
        for link in response.xpath('//a/@href'):

            link = link.extract()   # Get the link as text.

            if validate_url(link):
                if not link.startswith(u"http"):
                    link = self.netloc + link.lstrip('/')
                link_list.add(link)
            else:
                logging.debug(u"*** Skipping url [{}] ***".format(link))

        # Fetch pages.
        for link in link_list:
            logging.debug(u"Fetching {}".format(link))
            yield Request(link, callback=self.process_page)

    def process_page(self, response):
        logging.debug(u"Processing [{}], status = {}".format(response.url, response.status))

        # RETURN url and body to the pipeline.
        return dict(url=response.url, body=response.body)
