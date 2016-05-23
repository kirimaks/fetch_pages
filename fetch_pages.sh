#!/bin/bash

# ./fetch_pages.sh [url] [out_path]

if [[ $1 == '' || $2 == '' ]]; then
    echo "Usage: ./fetch_pages.sh [url] [out_path]"
    echo "Example: ./fetch_pages.sh http://google.com/search?q=panda /tmp/panda_pages"
    exit
fi

# Set environment (to use script not only from project's directory).
BASE_DIR=`dirname $(realpath $0)`
echo $BASE_DIR
cd $BASE_DIR
export PATH

scrapy crawl myspider -a url=$1 -a out_path=$2
