#!/bin/bash
echo "ARG01 is $1"
echo "ARG02 is $2"
source venv/bin/activate
python runme.py $1
