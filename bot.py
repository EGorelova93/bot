from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# 🔧 Логирование
logging.basicConfig(level=logging.INFO)

# 🔑 Твои данные
BOT_TOKEN = "8051090104:AAF04qthIzcCeEMyM8saN6S2hV-l2z4C1w4"
CHANNEL_USERNAME = "@ernigood_dvizh"
CHANNEL_URL = "https://t.me/ernigood_dvizh"
GUIDE_URL = "https://disk.yandex.ru/d/KadUn1GMfOSLFA"

# 🔹 /start
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📲 Подписаться", url=CHANNEL_URL)],
        [InlineKeyboardButton("✅ Я подписался", callback_data="subscribed")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "👋 Привет!\n\n"
        "Мы подготовили гайд для риелторов: как уверенно стартовать в соцсетях и привлекать клиентов из Instagram и Telegram.\n\n"
        "🛎 Чтобы получить гайд — подпишитесь на наш канал:\n👉 Эрнигуд Недвижка\n\n"
        "В нём мы делимся:\n"
        "— фишками продвижения для риелторов\n"
        "— полезными материалами\n"
        "— готовыми шаблонами и гайды"
    )

    update.message.reply_text(text, reply_markup=reply_markup)

# 🔹 Обработка кнопки "Я подписался" + проверка
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    bot = context.bot

    try:
        # Проверка подписки через Telegram API
        member = bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

        if member.status in ['member', 'administrator', 'creator']:
            # Подписан
            keyboard = [[InlineKeyboardButton("📘 Получить гайд", url=GUIDE_URL)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            text = (
                "✅ Спасибо, что с нами!\n\n"
                "📘 Ниже твой гайд — готовый план, как риелтору уверенно стартовать в соцсетях и не терять клиентов:"
            )
        else:
            # Не подписан
            keyboard = [[InlineKeyboardButton("📲 Подписаться", url=CHANNEL_URL)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            text = (
                "❌ Похоже, вы ещё не подписаны на канал.\n"
                "Пожалуйста, подпишитесь и вернитесь — это обязательное условие, чтобы получить гайд 😊"
            )

        query.answer()
        query.edit_message_text(text=text, reply_markup=reply_markup)

    except Exception as e:
        query.answer()
        query.edit_message_text(text=f"⚠️ Ошибка проверки подписки: {e}")

# 🔹 Запуск бота
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    print("Бот запущен...")
    updater.idle()

if __name__ == "__main__":
    main()
