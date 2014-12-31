#!/bin/bash
if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

dpkg -s mongodb-org > /dev/null 2>&1

PKG_EXISTS=$?

if [ $PKG_EXISTS -eq "0" ]; then
    DIR=$(readlink -m /data/mongod/mobileparser)
    if [ ! -d $DIR ]; then
        echo "creating directory $DIR ..."
        mkdir -p "$DIR"
    fi

    mongo --port 24730 --eval "db.stats()" > /dev/null 2>&1
    MONGO_RUNNING=$?
    if [ ! $MONGO_RUNNING -eq "0" ]; then
        mongod --config mongodb.conf
        SUCCESS=$?
        wait $!
        if [ $SUCCESS -eq "0" ]; then
            echo "running mongodb at localhost on port 24730"
        fi
    else
        echo "mongodb instance is already running"
    fi
else
    echo "[FAILURE] mongodb installation was not found"\
         "(expected package mongodb-org)"
fi