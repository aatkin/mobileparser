#!/bin/bash
mongo --port 24730 --eval "db.stats()" > /dev/null 2>&1

RESULT=$?

if [ $RESULT -eq "0" ]; then
    python mobileparser/main.py $1
else
    echo "[FAILURE] mongod instance is not up (expected port 24730)"
fi