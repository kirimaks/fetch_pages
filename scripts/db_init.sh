#!/bin/bash

if [ $1 == "" ]; then
    echo "Create or recreate tables in database."
    echo "Usage: $0 file.sql"
    exit
fi

dbname="parsed_data"
db_user="root"
db_pass="1234"

mysql -v -u$db_user -p$db_pass $dbname < $1
