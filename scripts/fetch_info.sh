#!/bin/bash

# Fetching info for all candidates from database.

if [[ $1 == "" ]]; then
    python ../fetch_info/fetch_info.py
else
    python ../fetch_info/fetch_info.py -c $1
fi
