#! /bin/bash

# Description
# This script executes a Python script that handles SerpApi queries for
# exact image matches in Google Image Search.
# Queries are run per link provided by reading a file with links.

# Parameters
# api_key: SerpApi key to access the API.
# file_name: File with image links.
# target_dir: Directory, in which, to store the result.

# EG
# bash snitch_on_links.sh ${api_key} ${file_name} ${target_dir}
# bash snitch_on_links.sh ${api_key} ${file_name}

file_name=$2
if [ -e "${file_name}" ]; then
    api_key=$1
    target_dir="./OUT"
    if [ $# -eq 3 ]; then
        target_dir="./$3"
        echo $#
    fi
    while read line; do
        [ ${#line} -gt 3 ] && python image_snitch.py -k ${api_key} -d ${target_dir} -s ${line}
    done < "${file_name}"
fi
