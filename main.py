import logging
from maxapi import Bot, Dispatcher

TOKEN = "f9LHodD0cOLLWCc_Hvywa6caaHTk8fTLJ31WdQE-tBap9zd-6NUXQ7QA19xz5K8VrJcsMnbnNj8VNvxJJ6TH"

bot = Bot(TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

user_data = {}

@dp.bot_started()
async def on_start(event):
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
async def handle_message(event):
    uid = event.from_user.id
    text = event.message.text
    
    if text == "/start":
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
    
    # Обработка callback'ов
    if hasattr(event, 'callback_query'):
        callback = event.callback_query
        if callback.data == "book_car":
            user_data[callback.from_user.id] = {"step": "name"}
            await callback.message.edit_text("Введите ваше ФИО:")
        return
    
    # Обычные сообщения
    if uid in user_data:
        step = user_data[uid].get("step")
        if step == "name":
            user_data[uid]["name"] = text
            user_data[uid]["step"] = "phone"
            await event.message.answer("Введите номер телефона:")
        elif step == "phone":
            user_data[uid]["phone"] = text
            await event.message.answer("✅ Заявка принята! Менеджер свяжется с вами.")
            del user_data[uid]

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
