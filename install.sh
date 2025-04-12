#!/bin/bash


read -p "Введи токен бота: " BOT_STEP_SD

echo 'export BOT_STEP_SD="$BOT_STEP_SD"' >> ~/.bashrc
source ~/.bashrc


python3 -m venv venv

source ./venv/bin/activate
pip install -r ./requirements.txt

./init_db.sh

