# Обучение модели и сохранение ее в файле .pkl

import sys
import logging
from pathlib import Path
import pickle
import pandas as pd
from numpy.linalg import LinAlgError
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier

# Получаем путь к лог-файлу из аргументов командной строки
log_file = sys.argv[1]

# Настройка логирования
logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(asctime)s][%(levelname)s][%(module)s]: %(message)s')

# Загружаем подготовленные данные
DATA_PATH = f'{Path(__file__).parent.parent}/results/clear_data.csv'
MODEL_PATH = f'{Path(__file__).parent.parent}/results/model.pkl'

def train_model(data_path):
    """
    Обучает модель логистической регрессии и сохраняет её.
    """
    try:
        # Загружаем данные
        df = pd.read_csv(data_path)
        logging.info(f"[TRAIN]: Данные для обучения загружены. Shape: {df.shape}")

        # Разделяем данные на признаки и целевую переменную
        X = df.drop(columns=['target'])
        y = df['target']

        # Обучение модели
        try:
            model = LogisticRegression(max_iter=1000)
            model.fit(X, y)
        except LinAlgError:
            logging.warning("Fallback to DummyClassifier")
            model = DummyClassifier(strategy="most_frequent")
            model.fit(X, y)
        logging.info("[TRAIN]: Модель обучена.")

        # Сохранение модели
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        logging.info(f"[TRAIN]: Модель сохранена в {MODEL_PATH}")

    except Exception as e:
        logging.error(f"[TRAIN]: Произошла ошибка при обучении модели: {e}")
        exit(1)

if __name__ == "__main__":
    train_model(DATA_PATH)
    print(log_file)