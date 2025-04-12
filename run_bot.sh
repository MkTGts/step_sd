#!/bin/bash

file=./main_step_sd_bot.py

source ./venv/bin/activate

python3 $file &> /dev/null &

echo "Бот запущен"

