#!/bin/bash

# Загрузка переменных окружения
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Запуск бота
cd "$(dirname "$0")"
source venv/bin/activate
python bot.py
