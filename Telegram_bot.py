import requests

def telegram_send_message(message):
    bot_token = ""
    bot_chatID = ""
    send_text = "https://api.telegram.org/bot"+bot_token+"/sendMessage?chat_id="+bot_chatID+"&parse_mode=Markdown&text="+message
    response = requests.get(send_text)
    return response.json()
