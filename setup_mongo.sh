#!/bin/bash
dpkg -s mongodb-org > /dev/null 2>&1

PKG_EXISTS=$?

if [ $PKG_EXISTS -eq "0" ]; then
    DIR=$(readlink -f "mongod")
    if [ ! -d $DIR ]; then
        echo "creating directory $DIR ..."
        mkdir "$DIR"
    fi

    mongo --port 24730 --eval "db.stats()" > /dev/null 2>&1
    MONGO_RUNNING=$?
    if [ ! $MONGO_RUNNING -eq "0" ]; then
        mongod --config mongodb.conf
        SUCCESS=$?
        wait $!
        if [ $SUCCESS -eq "0" ]; then
            echo "running mongodb at localhost on port 24730"
        else
            echo "[FAILURE] could not start mongodb instance, are you running sudo?"
        fi
    else
        echo "mongodb instance is already running"
    fi
else
    echo "[FAILURE] mongodb was not found!"
fi