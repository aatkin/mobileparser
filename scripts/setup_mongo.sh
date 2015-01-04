#!/bin/bash
if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

dpkg -s mongodb-org > /dev/null 2>&1

PORT=$1
if [ -z $PORT ]; then PORT=24730; fi

PKG_EXISTS=$?

if [ $PKG_EXISTS -eq "0" ]; then
    DIR=$(readlink -m /data/mongod/mobileparser)
    if [ ! -d $DIR ]; then
        echo "creating directory $DIR ..."
        mkdir -p "$DIR"
    fi

    mongo --port "$PORT" --eval "db.stats()" > /dev/null 2>&1
    MONGO_RUNNING=$?
    if [ ! $MONGO_RUNNING -eq "0" ]; then
        CONF=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../mongodb.conf
        mongod --config "$CONF" --port "$PORT"
        SUCCESS=$?
        wait $!
        if [ $SUCCESS -eq "0" ]; then
            echo "running mongodb at localhost on port $PORT"
        fi
    else
        echo "mongodb instance is already running"
    fi
else
    echo "[FAILURE] mongodb installation was not found"\
         "(expected package mongodb-org)"
fi