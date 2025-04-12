#!/bin/bash

ps -auxf | grep main_step_sd_bot.py | awk '{print $2}' | xargs kill -9 &> /dev/null

echo "Бот остановлен"
