#!/bin/bash

# ./fetch_pages.sh [url] [out_path]

scrapy crawl myspider -a url=$1 -a out_path=$2
