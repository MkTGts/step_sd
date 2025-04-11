#!/bin/bash

ps -auxf | grep main.py | awk '{print $2}' | xargs kill -9 &> /dev/null

echo "Бот остановлен"
