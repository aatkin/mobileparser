#!/bin/bash
if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

PROCESSES=$(ps aux | grep '[m]ongod' | awk '{print $2}' | tr '\n' ' ')
if [[ $PROCESSES ]]; then
    echo "Killing processes [ $PROCESSES] ..."
    kill "$PROCESSES"
else
    echo "No processes to kill"
fi