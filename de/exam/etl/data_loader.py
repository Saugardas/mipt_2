# Загрузка и сохранение данных в локальное хранилище

import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import logging
from pathlib import Path

load_dotenv() # загружаем .env файл

LOGS_DIR = f'{Path(__file__).parent.parent}/logs/'
RESULTS_DIR = f'{Path(__file__).parent.parent}/results/'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
log_file = os.path.join(LOGS_DIR, f"log_{current_time}.log")

# Формат логов
logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(asctime)s][%(levelname)s][%(module)s]: %(message)s')

DATA_URL = os.getenv('DATA_URL')

def load_and_save_data(path):
    """
    Загружает данные из DATA_URL и сохраняет их в results/raw_data.csv
    """
    try:
        df = pd.read_csv(path)
        logging.info(f"[LOADER]: Данные загружены. Размер данных: {df.shape}")
        
        # Сохраняем данные в файл raw_dataset.csv
        output_file = os.path.join(RESULTS_DIR, 'raw_data.csv')
        df.to_csv(output_file, index=False)
        logging.info(f"[LOADER]: Данные сохранены в {output_file}")
    except Exception as e:
        logging.error(f"[LOADER]: Произошла ошибка при чтении/сохранении данных: {e}")
        exit(1)

if __name__ == "__main__":
    load_and_save_data(DATA_URL)
    print(log_file)
