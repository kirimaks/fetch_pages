#!/bin/bash

if [[ $1 == '' ]]; then
    echo "Search a query in google."
    echo "Usage: ./search.sh [query]"
    echo "Example: ./search.sh panda"
    exit
fi

# Set environment (to use script not only from project's directory).
BASE_DIR=`dirname $(realpath $0)`
echo $BASE_DIR
cd $BASE_DIR
export PATH

bash ./fetch_pages.sh https://google.com/search?q=$1
