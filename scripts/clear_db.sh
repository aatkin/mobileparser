#!/bin/bash
if [[ $1 ]]; then
    while true; do
        read -p "Are you sure you want to clear the database $1? (y/n)" yn
        case $yn in
            [Yy]* ) mongo "$1" --port 24730 --eval "db.dropDatabase();" > /dev/null 2>&1; echo "done"; break;;
            [Nn]* ) exit;;
            * ) echo "Please answer [y]es or [n]o";;
        esac
    done
else
    echo "Please provide name of the database to clear"
fi