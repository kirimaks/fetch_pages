# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import MySQLdb


class FetchPagesPipeline(object):
    def open_spider(self, spider):
        logging.debug("Open mysql")
        self.mysql = MySQLdb.connect("localhost", "root",
                                     "1234", "parsed_data")
        self.cursor = self.mysql.cursor()
        search_string = spider.start_urls[0]
        self.search_id = self.get_search_id(search_string)
        if not self.search_id:
            self.search_id = self.new_search(search_string)
        assert(self.search_id)
        self.search_id = self.search_id[0]

    def close_spider(self, spider):
        logging.debug("Close mysql")
        self.mysql.close()

    def process_item(self, item, spider):
        logging.debug("*** Store page ***, sid = {}".format(self.search_id))

        query = """
            INSERT INTO search_space(search_id, url, content)
                VALUES(%s, %s, %s)
        """

        sid = self.search_id
        url = item['url']
        body = item['body']

        self.cursor.execute(query, (sid, url, body))

        self.mysql.commit()

    def get_search_id(self, search_string):
        query = """
            SELECT search_id
                FROM search WHERE search_string = '{}'
        """.format(search_string)

        self.cursor.execute(query)
        search_id = self.cursor.fetchone()
        return search_id

    def new_search(self, search_string):
        logging.debug("*** Create new pages query ***")
        query = """
            INSERT INTO search(search_string) VALUES('{}')
        """.format(search_string)
        self.cursor.execute(query)
        self.mysql.commit()

        query = """
            SELECT LAST_INSERT_ID()
        """
        self.cursor.execute(query)
        search_id = self.cursor.fetchone()

        return search_id
