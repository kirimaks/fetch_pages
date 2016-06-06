# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from scrapy.http import Request
from urlparse import urlparse


link_pattern = re.compile(r'(^\/|#|jav)|(^http.?:\/\/[\w]+\.(google|blogger))')


def validate_url(link):

    # Check link and restrict urls from pattern.
    if link_pattern.match(link):
        return False

    # If the link have an anchor, delete it.
    if link.find('#') != -1:
        link = link[:link.index('#')]

    return link


class SomeSpider(scrapy.Spider):
    name = "myspider"

    start_ruls = []

    def __init__(self, url=None, candidate_id=None, *kargs, **pargs):
        assert url, "Need to set a url."
        assert candidate_id, "Need to set candidate_id."

        scrapy.Spider.__init__(self, *kargs, **pargs)

        self.start_urls.append(url)
        self.candidate_id = candidate_id

        # Save netloc.
        parser = urlparse(url)
        self.netloc = "{}://{}/".format(parser.scheme, parser.netloc)

    def parse(self, response):
        link_list = set()

        # Prepare links (get unique links, and skip some links).
        for link in response.xpath('//a/@href'):

            link = link.extract()               # Get the link as text.
            checked_link = validate_url(link)   # Validate and truncate anchor.

            if checked_link:
                link_list.add(checked_link)             # Add link.
            else:
                logging.debug(u"*** Skipping url [{}] ***".format(link))

        # Fetch pages.
        for link in link_list:
            logging.debug(u"Fetching {}".format(link))
            yield Request(link, callback=self.process_page)

    def process_page(self, response):
        logging.debug(u"Processing [{}], status = {}".format(response.url,
                                                             response.status))

        # RETURN url and body to the pipeline.
        return dict(url=response.url, body=response.body,
                    candidate_id=self.candidate_id)
