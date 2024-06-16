import random
import os

from pyrogram import Client
from pyrogram.types import Message
from datetime import datetime, time
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv('APP_ID'))
api_hash = os.getenv('APP_HASH')
app_name = os.getenv('APP_NAME')

phone = os.getenv('PHONE')
passwd = os.getenv('PASSWD')
session = os.getenv('SESSION')

restricted_users = os.getenv('RESTRICTED_USERS').split(',')
buffer_chat = os.getenv('BUFFER_CHAT')
limit = int(os.getenv('LIMIT'))

recieved_messages = {
    '2024-01-01': {
        'username': 0
    }
}
available_reactions = ['🤷‍♀️', '👎', '🙈', '🏆','🤓','🥱','😱']


app = Client(app_name, api_id, api_hash, phone_number=phone, password=passwd, session_string=session)

@app.on_message()
async def my_handler(client: Client, message: Message):
    current_chat = message.chat.username
    if current_chat in restricted_users:
        await client.read_chat_history(message.chat.id)
        date_send = datetime.combine(datetime.today(), time(23, 00))
        await message.forward(buffer_chat, disable_notification=True, schedule_date=date_send)

        if not current_chat in recieved_messages:
            recieved_messages[current_chat] = 1
            await message.reply(f"Ваше сообщение принято. Оно отправится пользователю в {date_send}.\n"
                                f"Лимит сообщений на день: {limit}. Осталось {limit - 1} \n")
            return

        recieved_messages[current_chat] += 1
        if recieved_messages[current_chat] < limit:
            await message.reply(f"Ваше сообщение принято. Осталось {limit - recieved_messages[current_chat]} сообщений")
            return

        if recieved_messages[current_chat] == limit:
            await message.reply('Вы отправили последнее сообщение. Следующие сообщения не будут отправлены')
            return

        if recieved_messages[current_chat] > limit:
            await message.react(random.choice(available_reactions))
            return


app.run()
