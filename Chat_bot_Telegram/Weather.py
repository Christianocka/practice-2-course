from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location_button = KeyboardButton(text="Отправить локацию", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Нажмите кнопку ниже, чтобы отправить свою геолокацию:", reply_markup=reply_markup)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    api_key = "55d0ba5e428c74d598742f9304895cba"
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=ru"

    response = requests.get(url)
    data = response.json()

    if data.get("weather"):
        city = data.get("name", "неизвестно где")
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        await update.message.reply_text(f"🌍 Местоположение: {city}\n🌡 Температура: {temp}°C\n☁️ Погода: {description}")
    else:
        await update.message.reply_text("Не удалось получить данные о погоде.")

async def main():
    app = ApplicationBuilder().token("8191588127:AAFNL8Yvbowf0aMO4RYBHjmZPgJfGqnz5Xs").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    print("Бот запущен...")
    await app.run_polling()

import asyncio
import nest_asyncio
nest_asyncio.apply()
asyncio.get_event_loop().run_until_complete(main())
