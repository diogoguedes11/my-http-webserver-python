#!/bin/sh
#
# Use this script to run your program LOCALLY.
#

set -e # Exit early if any commands fail

exec pipenv run python3 -m app.main "$@"

