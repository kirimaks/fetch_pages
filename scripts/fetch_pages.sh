#!/bin/bash

# ./fetch_pages.sh [url]

if [[ $1 == '' || $2 == '' ]]; then
    echo "Usage: $0 [url]"
    echo "Example: $0 http://google.com/search?q=panda"
    exit
fi

# Set environment (to use script not only from project's directory).
BASE_DIR=`dirname $(realpath $0)`
echo $BASE_DIR
cd $BASE_DIR
export PATH

scrapy crawl myspider -a url=$1 -a candidate_id=$2
