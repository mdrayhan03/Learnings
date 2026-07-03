#!/bin/bash

set -e

LOG_DIR="./logs"

echo "===Log Cleaner Start==="

echo "Enter your name"
read NAME

if [ ! -d "$LOG_DIR" ]; then
    echo "ERROR: Log dir ($LOG_DIR) doesn't exist...."
    exit 1
fi

for file in "$LOG_DIR"/*.log; do
    if [ ! -e "$file" ]; then
        echo "No .log files found"
        break
    fi

    echo "Removing: $file"
    rm "$file"
done

echo "Congratulation $NAME, Log cleanup complete!"
echo "[CLEANUP] by $NAME ($(date))" >> "$LOG_DIR"/cleanup_log.txt

echo "___Cleanup Log History___"
cat < "$LOG_DIR"/cleanup_log.txt
