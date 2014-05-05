# mobilefood-parser [![Build Status](https://travis-ci.org/Wiltzu/mobilefood-parser.png)](https://travis-ci.org/Wiltzu/mobilefood-parser) #

## HTML parser for Mobilefood exercise project ##

Creates JSON-output from certain restaurant foods.

### Usage ###

Run the run.sh shell script from the command line with proper rights (sudo and chmod +x). For timed parsing on the server side, add following cronjob to the crontab:
- `0 7 * * 1 cd /path/to/mobilefood-parser && /bin/echo "$(date)" > log && ./run.sh >> log 2>&1`
