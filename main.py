import requests


BOT_TOKEN = '' # buraya bot tokeninizi girin


SAHIBIN_CHAT_ID = '' # buraya kendi id'nizi girin

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response.json()

def start(update):
    user_name = update['message']['from']['first_name']
    chat_id = update['message']['chat']['id']
    response = f"Merhaba {user_name}, Ben Sahibim İle İletişim Kurmanız İçin Yaratılmış Basit Bir Botun.\n\nSpamınız Var İse Burdan Mesajınızı Yazabilirsiniz Sahibime ileteceğim.\n\nYazacağınız Örnek Metin: Merhaba Benim Spamım Var, Bana Yazar Mısın?"
    send_message(chat_id, response)

def receive_message(update):
    user_id = update['message']['from']['id']
    user_name = update['message']['from']['first_name']
    message_text = update['message']['text']
    response = f"Yeni Mesaj!\nKullanıcı: {user_name}\nMesajı: {message_text}\nKullanıcı ID: {user_id}"
    send_message(SAHIBIN_CHAT_ID, response)
    send_message(user_id, "Mesajınız Gönderildi!")

def main():
    offset = None
    while True:
        response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}')
        updates = response.json().get('result')
        
        if updates:
            for update in updates:
                offset = update['update_id'] + 1
                
                if 'message' in update and 'text' in update['message']:
                    if update['message']['text'] == '/start':
                        start(update)
                    else:
                        receive_message(update)

if __name__ == '__main__':
    main()
