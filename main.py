import os
import logging
from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, MessageCreated

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
bot = Bot(MAX_BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

user_data = {}

@dp.bot_started()
async def on_start(event: BotStarted):
    keyboard = {
        "inline_keyboard": [[{
            "text": "🚗 ЗАБРОНИРОВАТЬ АВТО",
            "callback_data": "book_car"
        }]]
    }
    await event.bot.send_message(
        chat_id=event.chat_id,
        text="Привет! Я бот для бронирования авто. Нажми кнопку.",
        extra={"attachments": [keyboard]}
    )

@dp.message_created()
async def handle_message(event: MessageCreated):
    uid = event.from_user.id
    
    # Обработка команды /start
    if event.message.text == "/start":
        keyboard = {
            "inline_keyboard": [[{
                "text": "🚗 ЗАБРОНИРОВАТЬ АВТО",
                "callback_data": "book_car"
            }]]
        }
        await event.message.answer(
            "Добро пожаловать! Нажмите кнопку для бронирования.",
            extra={"attachments": [keyboard]}
        )
        return
    
    # Если пользователь в процессе бронирования
    if uid in user_data:
        step = user_data[uid].get("step")
        if step == "name":
            user_data[uid]["name"] = event.message.text
            user_data[uid]["step"] = "phone"
            await event.message.answer("Введите номер телефона:")
        elif step == "phone":
            user_data[uid]["phone"] = event.message.text
            await event.message.answer("✅ Заявка принята! Менеджер свяжется с вами.")
            del user_data[uid]

# Обработка нажатий на кнопки
@dp.callback_query_handler()
async def handle_callback(callback):
    if callback.data == "book_car":
        user_data[callback.from_user.id] = {"step": "name"}
        await callback.message.edit_text("Введите ваше ФИО:")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
