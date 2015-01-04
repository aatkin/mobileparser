#!/bin/bash
mongo --port 24730 --eval "db.stats()" > /dev/null 2>&1

RESULT=$?

if [ $RESULT -eq "0" ]; then
    DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
    python "$DIR"/mobileparser/main.py $1
else
    echo "[FAILURE] mongod instance is not up (expected port 24730)"
    echo "Have you run setup_mongo.sh?"
fi