#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import MySQLdb


def connect_to_db():
    db = MySQLdb.connect("localhost", "root", "1234", "parsed_data")
    return db


def get_num_of_candidates_info():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM search")
    num_of_results = cursor.fetchone()[0]
    db.close()
    return num_of_results


def get_num_of_wiki_pages():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM search_space WHERE url LIKE '%wikipedia%'")
    num_of_results = cursor.fetchone()[0]
    db.close()
    return num_of_results


class BaseTest(unittest.TestCase):
    def test_wiki_pages(self):
        num_of_infos = get_num_of_candidates_info()
        num_of_wiki_pages = get_num_of_wiki_pages()
        self.assertTrue(num_of_wiki_pages >= num_of_infos)

if __name__ == "__main__":
    unittest.main()
