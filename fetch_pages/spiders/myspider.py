# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from scrapy.http import Request
from urlparse import urlparse


def validate_url(link):

    # r'^http.?:\/\/[\w]*\.google.*'   # For all google subdomain.

    restricted_urls = (
        r'^\/',
        r'^http.?:\/\/www\.google.*',
        r'^http.?:\/\/translate\.google.*',
        r'^http.?:\/\/maps\.google.*',
        r'^http.?:\/\/accounts\.google.*',
        r'^http.?:\/\/plus\.google.*',
        r'^http.?:\/\/news\.google.*',
        r'^http.?:\/\/support\.google.*',
        r'^http.?:\/\/play\.google.*',
        r'^http.?:\/\/mail\.google.*',
        r'^http.?:\/\/photos\.google.*',
        r'^http.?:\/\/myaccount\.google.*',
        r'^http.?:\/\/docs\.google.*',
        r'^http.?:\/\/wallet\.google.*',
        r'^http.?:\/\/drive\.google.*',
        r'^http.?:\/\/webcache\.googleusercontent.*',
        r'^http.?:\/\/www\.blogger.com',
        r'^http.?:\/\/hangouts.google.com',
    )

    if not re.match("^http", link):     # If starts not from http, filter it.
        return False

    for pt in restricted_urls:
        if re.match(pt, link):
            return False

    return True


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
