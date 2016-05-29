#!/bin/bash

# ./fetch_pages.sh [url] [out_path]

if [[ $1 == '' ]]; then
    me=`basename "$0"`
    echo "Usage: ./$me [url]"
    echo "Example: ./$me http://google.com/search?q=panda"
    exit
fi

# Set environment (to use script not only from project's directory).
BASE_DIR=`dirname $(realpath $0)`
echo $BASE_DIR
cd $BASE_DIR
export PATH

scrapy crawl myspider -a url=$1
