import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from tarot_data import tarot_deck  # Убедитесь, что tarot_data.py лежит рядом

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["💖 Любовь", "💼 Карьера"],
            ["🌌 Путь души", "✨ Совет"],
            ["🛠️ Поддержка"]
        ],
        resize_keyboard=True
    )


def draw_card(topic):
    card = random.choice(tarot_deck)
    position = random.choice(["upright", "reversed"])
    card_data = card[position]

    if topic in card_data:
        meaning = card_data[topic]["meaning"]
        description = card_data[topic]["description"]
    else:
        meaning = card_data["meaning"]
        description = card_data["description"]

    return f"🃏 {card['name']} ({'прямая' if position == 'upright' else 'перевёрнутая'})\n\n{meaning}\n\nОписание: {description}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔮 Привет! Я Таро-бот. Выбирай тему расклада:",
        reply_markup=main_menu_keyboard()
    )


async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cards = [draw_card("love") for _ in range(3)]
    reply = "💖 Расклад на любовь:\n\n" + "\n\n".join(cards)
    await update.message.reply_text(reply)


async def career(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cards = [draw_card("career") for _ in range(3)]
    reply = "💼 Расклад на карьеру и финансы:\n\n" + "\n\n".join(cards)
    await update.message.reply_text(reply)


async def soul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cards = [draw_card("soul_path") for _ in range(3)]
    reply = "🌌 Путь души / самопознание:\n\n" + "\n\n".join(cards)
    await update.message.reply_text(reply)


async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card = draw_card("daily_card")
    reply = "✨ Совет от Таро:\n\n" + card
    await update.message.reply_text(reply)


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "💖 Любовь":
        await love(update, context)
    elif text == "💼 Карьера":
        await career(update, context)
    elif text == "🌌 Путь души":
        await soul(update, context)
    elif text == "✨ Совет":
        await advice(update, context)
    elif text == "🛠️ Поддержка":
        await update.message.reply_text("Пожалуйста, напишите в инстаграм taro.pulse, и я постараюсь помочь!")


def main():
    import os
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("love", love))
    app.add_handler(CommandHandler("career", career))
    app.add_handler(CommandHandler("soul", soul))
    app.add_handler(CommandHandler("advice", advice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))

    try:
        app.run_polling()
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    main()







