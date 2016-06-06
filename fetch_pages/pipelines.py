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

    def close_spider(self, spider):
        logging.debug("Close mysql")
        self.mysql.close()

    def process_item(self, item, spider):

        query = """
            INSERT INTO search_space(url, content, candidate_id)
                VALUES(%s, %s, %s)
        """

        # sid = self.search_id
        url = item['url']
        body = item['body']
        candidate_id = item['candidate_id']

        logging.debug("*** Save page ***, size = {}".format(len(body)))

        self.cursor.execute(query, (url, body, candidate_id))

        self.mysql.commit()
