import sys
import json
import logging
import pickle
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Получаем путь к лог-файлу из аргументов командной строки
log_file = sys.argv[1]

# Настройка логирования
logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(asctime)s][%(levelname)s][%(module)s]: %(message)s')

# Определим пути к необходимым ресурсам
ROOT_DIR = Path(__file__).parent.parent
DATA_PATH = f'{Path(__file__).parent.parent}/results/clear_data.csv'
MODEL_PATH = f'{Path(__file__).parent.parent}/results/model.pkl'
EVALUATION_PATH = f'{Path(__file__).parent.parent}/results/evaluation.json'
PREDICTIONS_PATH = f'{Path(__file__).parent.parent}/results/predictions.csv'

def evaluate_model(data_path, model_path, evaluation_path):
    """
    Оценивает модель и сохраняет результаты в JSON.
    Возвращает истинные и предсказанные значения.
    """
    try:
        # Загружаем данные
        df = pd.read_csv(data_path)
        logging.info(f"[EVALUATE]: Данные загружены. Shape: {df.shape}")

        # Загружаем модель
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logging.info(f"[EVALUATE]: Модель загружена")

        # Разделяем данные на признаки и целевую переменную
        X = df.drop(columns=['target'])  # Признаки
        y_true = df['target']  # Истинные значения

        # Прогнозируем с помощью модели
        y_pred = model.predict(X)

        # Расчет метрик
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1_score': f1_score(y_true, y_pred)
        }

        # Сохраняем результаты оценки в JSON
        with open(evaluation_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        logging.info(f"[EVALUATE]: Результаты оценки сохранены в {EVALUATION_PATH}")

        return y_true, y_pred
    except Exception as e:
        logging.error(f"[EVALUATE]: Произошла ошибка при оценке модели: {e}")
        exit(1)

def save_predictions(predictions_path, y_true, y_pred):
    """
    Сохраняет предсказанные значения в CSV.
    """
    try:
        # Сохраняем предсказанные значения
        df_predictions = pd.DataFrame({'true': y_true, 'predicted': y_pred})
        df_predictions.to_csv(predictions_path, index=False)
        logging.info(f"[EVALUATE]: Предсказания сохранены в {predictions_path}")
    except Exception as e:
        logging.error(f"[EVALUATE]: Произошла ошибка при сохранении предсказаний: {e}")
        exit(1)

if __name__ == "__main__":
    try:
        y_true, y_pred = evaluate_model(DATA_PATH, MODEL_PATH, EVALUATION_PATH)
        save_predictions(PREDICTIONS_PATH, y_true, y_pred)
    except Exception as e:
        logging.error(f"[EVALUATE]: Произошла ошибка запуска evaluation: {e}")
        exit(1)
        
