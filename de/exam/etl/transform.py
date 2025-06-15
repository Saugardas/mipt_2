# Очистка и предобработка данных (raw_data.csv -> clear_data.csv)

import sys
import logging
import pandas as pd
from pathlib import Path

# Получаем путь к лог-файлу из аргументов командной строки
log_file = sys.argv[1]

logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(asctime)s][%(levelname)s][%(module)s]: %(message)s')

RAW_DATA_PATH = f'{Path(__file__).parent.parent}/results/raw_data.csv'  # загруженные необработанные данные
CLEAR_DATA_PATH = f'{Path(__file__).parent.parent}/results/clear_data.csv' # обработанные данные для модели

def transform_data(raw_data_path):
    """
    Выполняет очистку и предобработку данных, возвращает преобразованный DataFrame.
    """
    try:
        # Загружаем данные
        df = pd.read_csv(raw_data_path, header=None)
        logging.info(f"[TRANSFORM]: Данные успешно загружены. Shape: {df.shape}")

        # Названия колонок (ID, Target, features)
        col_names = ['id'] + ['target'] + [f'column_{i}' for i in range(1, len(df.columns)-1)]
        df.columns = col_names

        # Проверяем значения в колонке 'target' на корректность
        if not set(df['target'].unique()).issubset({'B', 'M'}):
            logging.error("[TRANSFORM]: невалидные данные в target")
            exit(1)

        df['target'] = df['target'].map({'B': 0, 'M': 1}) # Преобразование target'а B/M в 0/1

        df = df.drop(columns=['id']) # стобец ID не нужен для обучения модели
        df = df.dropna(axis=0)  # Удаляем строки с любыми NaN

        logging.info(f"[TRANSFORM]: Преобразование завершено. Shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"[TRANSFORM]: Произошла ошибка при преобразовании: {e}")
        exit(1)

def save_transformed_data(transformed_df, clear_data_path):
    """Сохраняет преобразованный dataset в файл"""
    try:
        transformed_df.to_csv(clear_data_path, index=False)
        logging.info(f"[TRANSFORM]: Преобразованные данные сохранены в {clear_data_path}")
    except Exception as e:
        logging.error(f"[TRANSFORM]: Произошла ошибка при сохранении преобразованных данных: {e}")
        exit(1)

if __name__ == "__main__":
    df = transform_data(RAW_DATA_PATH)
    save_transformed_data(df, CLEAR_DATA_PATH)
    print(log_file)
