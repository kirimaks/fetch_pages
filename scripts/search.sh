#!/bin/bash

if [[ $1 == '' ]]; then
    echo "Search a query in google."
    echo "Usage: $0 first_name last_name state"
    echo "Example: $0 Johnny Depp California"
    exit
fi

# Set environment (to use script not only from project's directory).
BASE_DIR=`dirname $(realpath $0)`
echo $BASE_DIR
cd $BASE_DIR
export PATH

bash ./fetch_pages.sh https://google.com/search?q=$1+$2+$3+politics
# bash ./fetch_pages.sh https://www.bing.com/search?q=$1+$2+$3+politics
