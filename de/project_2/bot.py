#!/usr/bin/env python

import logging
import requests
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os

from pg_logger import db

load_dotenv()
CSV_LOG_PATH = os.getenv('CSV_LOG_PATH')
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
FOLDER_ID = os.getenv('FOLDER_ID')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_iam_token():
    try:
        response = requests.post(
            'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            json={'yandexPassportOauthToken': OAUTH_TOKEN}
        )

        response.raise_for_status()
        return response.json()['iamToken']
    except Exception as err:
        write_log(None, 'error', str(err)[:50])
        logger.error(f'Ошибка получения токена: {err}')
        raise


def write_log(user_id, action, additional_info=None):
    """Запись логов в БД"""
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                        INSERT INTO bot_logs (user_id, action, additional_info)
                        VALUES (%s, %s, %s)
                        """, (user_id, action, additional_info))
    except Exception as err:
        logger.error(f'Ошибка записи логов: {err}')

def read_log(lines=1):
    """Выводим записи из PG-лога"""
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT user_id, action, additional_info, created_at::timestamp(0) FROM bot_logs ORDER BY id DESC LIMIT (%s)', (lines,))
            lines = cursor.fetchall()
            formatted_values = []
            for line in lines:
                formatted_values.append(f'UserId: {line[0]} Action: {line[1]}, Info: {line[2]}, CreatedAt: {line[3]}')
            
            return "\n".join(formatted_values)

    except Exception as err:
        logger.error(f'Ошибка чтения логов: {err}')
        return str(err)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    write_log(update.message.from_user.id, 'start')
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот с Yandex-GPT",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выведем последние три записи лога"""
    write_log(update.message.from_user.id, 'help')
    await update.message.reply_text(read_log(lines=3))


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отвечает пользователю с использованием YandexGPT"""
    user_text = update.message.text
    write_log(update.message.from_user.id, 'request', user_text[:50])

    # Получаем IAM токен
    iam_token = get_iam_token()

    # Собираем запрос
    data = {}
    # Указываем тип модели
    data["modelUri"] = f"gpt://{FOLDER_ID}/yandexgpt"
    # Настраиваем опции
    data["completionOptions"] = {"temperature": 0.3, "maxTokens": 1000}
    # Указываем контекст для модели
    data["messages"] = [{"role": "user", "text": f"{user_text}"}]

    URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    try:
        # Отправляем запрос
        response = requests.post(
            URL,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {iam_token}"
            },
            json=data,
        ).json()

        answer = response.get('result', {})\
                         .get('alternatives', [{}])[0]\
                         .get('message', {})\
                         .get('text', {})
        write_log(update.message.from_user.id, 'answer', answer[:50])

        await update.message.reply_text(answer)
    except Exception as err:
        logger.error(f'Ошибка обработки запроса: {err}')


def main() -> None:
    """Запуск бота"""
    try:
        # Создаём соединение с базой
        db.connect(
            dbname=os.getenv('PG_DB_NAME'),
            user=os.getenv('PG_DB_USER'),
            password=os.getenv('PG_DB_PASS'),
            host=os.getenv('PG_HOST'),
            port=os.getenv('PG_PORT')
            )

        application = Application.builder().token(os.getenv("BOT_ID")).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        db.close()


if __name__ == "__main__":
    main()
