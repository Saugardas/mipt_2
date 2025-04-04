#!/usr/bin/env python

import logging
import requests
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os

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
        logger.error(f'Ошибка получения токена: {err}')
        raise

def write_log(user_id, action):
    """Запись логов в log.csv"""
    written_info = f'{user_id},{datetime.now().strftime("%d.%m.%Y %H.%M.%S")},{action}\n'
    try:
        if not os.path.exists(CSV_LOG_PATH):
            with open(CSV_LOG_PATH, 'w') as file:
                file.write('id,datetime,action\n')

        with open(CSV_LOG_PATH, 'a') as file:
            file.write(written_info)
    except Exception as err:
        logger.error(f'Ошибка записи логов: {err}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    write_log(update.message.from_user.id, 'start')
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот с Yandex-GPT",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    write_log(update.message.from_user.id, 'help')
    await update.message.reply_text("Help!")


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отвечает пользователю с использованием YandexGPT"""
    write_log(update.message.from_user.id, 'answer')
    user_text = update.message.text

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

        await update.message.reply_text(answer)
    except Exception as err:
        logger.error(f'Ошибка обработки запроса: {err}')


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("BOT_ID")).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
