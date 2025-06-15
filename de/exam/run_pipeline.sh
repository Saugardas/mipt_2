#!/bin/bash

LOG_FILE=$(python3 ./etl/data_loader.py) # Запускаем первый этап пайплайна (создание лог-файла)

# Проверяем, что лог-файл успешно создан
if [[ ! -z "$LOG_FILE" ]]; then
    echo "Лог-файл создан: $LOG_FILE"
else
    echo "Ошибка: лог-файл не создан."
    exit 1
fi

# Запускаем следующие этапы пайплайна с передачей лог-файла
echo "Запускаем Transform..."
python3 ./etl/transform.py "$LOG_FILE"

echo "Запускаем Train..."
python3 ./etl/train.py "$LOG_FILE"

echo "Запускаем Evaluate..."
python3 ./etl/evaluate.py "$LOG_FILE"

echo "Пайплайн выполнен успешно!"
exit 0