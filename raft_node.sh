#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <config_path>"
    exit 1
fi

python3 node/main.py --config "$1"
