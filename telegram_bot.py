import requests


def send_message_to_telegram(token, chat_id, text):
    telegram_url = f'https://api.telegram.org/bot{token}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(telegram_url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")