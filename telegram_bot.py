import requests


def send_message_to_telegram(token, chat_id, text):
    """
    Отправляет сообщение в Telegram.

    :param token: Токен вашего бота.
    :param chat_id: ID чата, куда будет отправлено сообщение.
    :param text: Текст сообщения.
    """
    telegram_url = f'https://api.telegram.org/bot{token}/sendMessage'

    # Формируем данные для запроса
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }

    # Отправляем сообщение в Telegram
    try:
        response = requests.post(telegram_url, json=payload)
        response.raise_for_status()  # Проверка на ошибки
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")