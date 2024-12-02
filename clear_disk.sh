#!/bin/bash

DIR_TO_CLEAN="path/to/media"
MINUTES_OLD=1

find "$DIR_TO_CLEAN" -type f -mmin +$MINUTES_OLD -exec rm -f {} \;
echo "Cleanup completed at $(date)" >> .path/to/logs/clean_disk.log
