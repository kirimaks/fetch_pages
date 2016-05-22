# -*- coding: utf-8 -*-
import scrapy
import logging
import re
import os
import uuid
from scrapy.http import Request
from urlparse import urlparse


class ExampleSpider(scrapy.Spider):
    name = "myspider"

    start_ruls = []
    # out_path = None

    def __init__(self, url=None, out_path=None, *kargs, **pargs):
        assert url, "Need to set a url."
        assert out_path, "Need to set output path."

        scrapy.Spider.__init__(self, *kargs, **pargs)
        self.start_urls.append(url)
        self.out_path = out_path

        # Save netloc.
        parser = urlparse(url)
        self.netloc = "{}://{}/".format(parser.scheme, parser.netloc)

        # Create output directory.
        os.mkdir(self.out_path)

    def parse(self, response):
        self.save_page(response.body, "index.html")     # Save root page.

        link_list = set()

        # Prepare links.
        for link in response.xpath('//a/@href'):
            link = link.extract()
            if re.match(r'(^\/\w+)|(^\w.+)', link):
                # yield self.fetch_page(link)                   # Fetch a page.
                link_list.add(link)
            else:
                logging.debug(u"*** Skipping url [{}] ***".format(link))

        # Process links.
        for link in link_list:
            yield self.fetch_page(link)

    def save_page(self, body, name):
        logging.debug(u"Save page {} [{}] to ({})".format(name,
                                                          len(body),
                                                          self.out_path))

        path_to_file = os.path.join(self.out_path, name)
        with open(path_to_file, "w") as output:
            output.write(body)

    def fetch_page(self, url):
        if not url.startswith(u"http"):
            url = self.netloc + url.lstrip('/')

        logging.debug(u"Fetching {}".format(url))
        return Request(url, callback=self.process_page)

    def process_page(self, response):
        # Create name for a file, or generate random???

        name = u"{}.html".format(uuid.uuid4().hex)
        self.save_page(response.body, name)
