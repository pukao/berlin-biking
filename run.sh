#!/bin/bash

echo "Starting the data feeder"

while true;
do
  echo "New round of parsing"
  python berlin_biking.py
  sleep $((24*60*60))
done

echo "Ahm, what happened?"
