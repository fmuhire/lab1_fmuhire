#!/bin/bash

FILE="grades.csv"
ARCHIVE="archive"
LOG="organizer.log"

# Create archive folder if it doesn't exist
if [ ! -d "$ARCHIVE" ]; then
    mkdir "$ARCHIVE"
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# Archive grades.csv
if [ -f "$FILE" ]; then
    NEW_NAME="grades_$TIMESTAMP.csv"
    mv "$FILE" "$ARCHIVE/$NEW_NAME"
    touch "$FILE"
    echo "$TIMESTAMP - Moved $FILE to $ARCHIVE/$NEW_NAME" >> "$LOG"
    echo "Done archiving."
else
    echo "grades.csv not found."
fi
