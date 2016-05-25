# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from scrapy.http import Request
from urlparse import urlparse


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

        # Link pattern.
        self.link_pattern = re.compile(r'(^\/\w+)|(^\w.+)')

    def check_link(self, link):
        # Here can check if the link is valid.

        link = link.rstrip('/')
        if self.link_pattern.match(link):
            return True

        return False

    def parse(self, response):
        link_list = set()

        # Prepare links (get unique links, and skip some links).
        for link in response.xpath('//a/@href'):

            link = link.extract()   # Get the link as text.

            if self.check_link(link):
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
        logging.debug(u"Processing [{}]".format(response.url))

        # RETURN url and body to the pipeline.
        return dict(url=response.url, body=response.body)
