#!/bin/bash

file=./main.py

source ./venv/bin/activate

python3 $file &> /dev/null &

echo "Бот запущен"

