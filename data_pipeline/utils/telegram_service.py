import asyncio
from telegram import Bot 
from telegram.error import TelegramError # type: ignore
import os 
from dotenv import load_dotenv # type: ignore
load_dotenv(override=True)

telegram_token = os.getenv("CHAT_TOKEN")
telegram_group_id_success = os.getenv("CHAT_GROUP_ID_SUCCESS")

async def send_msg(token, chat_id, msg: str):
    try:
        bot = Bot(token)
        await bot.send_message(chat_id=chat_id, text=msg, parse_mode='HTML')
        print("**"*25)
        print("Message sent")
        print("**"*25)
        
    except TelegramError as error:
        print("**"*25)
        print(f'Telegram Bot Fails to Alert. Error:\n{error}')
        print("**"*25)

def send_telegram_message(text_message:str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(send_msg(telegram_token, telegram_group_id_success, text_message))
    except asyncio.TimeoutException:
        loop.close()
