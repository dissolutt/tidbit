#!/usr/bin/env python3
import logging
import os
import sys
import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

TOKEN = os.environ.get("8299162168:AAEeYddTVCQ6V3Dyn6vedSJGgXBFfeWDTK0")
if not TOKEN:
    log.error("TELEGRAM_BOT_TOKEN не установлен!")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)
started_users = set()

FILE_IDS_PATH = os.path.join(os.path.dirname(__file__), "file_ids.json")

if not os.path.exists(FILE_IDS_PATH):
    with open(FILE_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump({}, f)

DIRECTION_MAP = {
    "hiphop": "hiphop.mp4",
    "hip-hop": "hiphop.mp4",
    "хип-хоп": "hiphop.mp4",
    "dancehall": "dancehall.mp4",
    "дэнсхолл": "dancehall.mp4",
    "contemporary": "contemporary.mp4",
    "контемпорари": "contemporary.mp4",
    "jazzmodern": "jazzmodern.mp4",
    "jazz modern": "jazzmodern.mp4",
    "джаз модерн": "jazzmodern.mp4",
    "jazzfunk": "jazzfunk.mp4",
    "jazz-funk": "jazzfunk.mp4",
    "джаз-фанк": "jazzfunk.mp4",
    "kpop": "kpop.mp4",
    "k-pop": "kpop.mp4",
    "кпоп": "kpop.mp4",
    "rental": "rental.mp4",
    "аренда": "rental.mp4",
}

AERIAL_TEXT = (
    "воздушные направления:\n\n"
    "• stretching\n"
    "• stretching дети\n"
    "• jumping fitness\n"
    "• high heels\n"
    "• pole dance\n"
    "• pole dance дети\n"
    "• exotic pole dance\n"
    "• зумба\n"
    "• воздушная гимнастика\n"
    "• воздушная гимнастика (дети)\n"
    "• танец живота\n"
    "• танец живота (дети)"
)

DANCE_TEXT = (
    "танцевальные направления:\n\n"
    "• jazz-funk\n"
    "• contemporary\n"
    "• hip-hop\n"
    "• dancehall\n"
    "• jazz modern\n"
    "• k-pop\n"
    "• детский танец"
)

PRICE_TEXT = (
    "первое пробное занятие:\n"
    "танцы - 350 руб.\n"
    "пилон, полотно - 400 руб.\n\n"
    "разовое занятие:\n"
    "танцы - 500 руб.\n"
    "пилон, полотно - 550 руб.\n\n"
    "абонемент на 8 занятий/месяц:\n"
    "танцы - 2900 руб.\n"
    "пилон - 3300 руб.\n"
    "полотно - 3500 руб."
)

RENTAL_TEXT = (
    "в наличии нашей студии:\n\n"
    "• 4 комфортных зала с зеркалами и удобным покрытием\n"
    "• качественная музыкальная аппаратура\n"
    "• системы кондиционирования\n"
    "• спортивный инвентарь\n"
    "• 2 раздевалки (мужская/женская)\n"
    "• зона ожидания с удобными диванами\n\n"
    "1 час - 700 / 750 ₽ (танцы / пилон)\n"
    "(300 ₽ - предоплата, 400 ₽ - доплачивать по факту)"
)

HELLO_TEXT = "чем могу помочь? :3"

def load_file_ids():
    try:
        with open(FILE_IDS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_file_ids(file_ids):
    with open(FILE_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(file_ids, f, ensure_ascii=False, indent=2)

def send_video_smart(chat_id, filename, caption, reply_markup=None):
    file_ids = load_file_ids()

    if filename in file_ids:
        try:
            msg = bot.send_video(chat_id, file_ids[filename], caption=caption, reply_markup=reply_markup)
            return msg
        except Exception as e:
            log.warning(f"Неверный file_id: {e}")
            bot.send_message(chat_id, "⚠️ Видео недоступно", reply_markup=reply_markup)
            return None

    bot.send_message(chat_id, "⚠️ Сначала отправь видео боту с подписью", reply_markup=reply_markup)
    return None

def start_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("начать"))
    return markup

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("о нас"), KeyboardButton("направления"))
    markup.add(KeyboardButton("педагоги"), KeyboardButton("расписание"))
    markup.add(KeyboardButton("прайс"), KeyboardButton("абонементы"))
    markup.add(KeyboardButton("аренда залов"))
    return markup

def directions_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("воздушные"), KeyboardButton("танцевальные"))
    markup.add(KeyboardButton("главное меню"))
    return markup

def aerial_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("танцевальные"))
    markup.add(KeyboardButton("главное меню"))
    return markup

def dance_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("воздушные"))
    markup.add(KeyboardButton("главное меню"))
    return markup

def subscriptions_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("продлить прошлый абонемент"))
    markup.add(KeyboardButton("приобрести новый абонемент"))
    markup.add(KeyboardButton("разовое занятие"), KeyboardButton("пробное занятие"))
    markup.add(KeyboardButton("главное меню"))
    return markup

def buy_directions_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("воздушные 🛒"), KeyboardButton("танцевальные 🛒"))
    markup.add(KeyboardButton("◀️ к абонементам"))
    return markup

def buy_aerial_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("танцевальные 🛒"))
    markup.add(KeyboardButton("◀️ к абонементам"))
    return markup

def buy_dance_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("воздушные 🛒"))
    markup.add(KeyboardButton("◀️ к абонементам"))
    return markup

def teachers_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("jazz-funk"), KeyboardButton("jazz modern"))
    markup.add(KeyboardButton("contemporary"), KeyboardButton("hip-hop"))
    markup.add(KeyboardButton("dancehall"), KeyboardButton("k-pop"))
    markup.add(KeyboardButton("в главное меню"))
    return markup

def after_dancehall_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("jazz-funk"), KeyboardButton("jazz modern"))
    markup.add(KeyboardButton("contemporary"), KeyboardButton("hip-hop"))
    markup.add(KeyboardButton("k-pop"))
    markup.add(KeyboardButton("в главное меню"))
    return markup

def after_hiphop_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("jazz-funk"), KeyboardButton("jazz modern"))
    markup.add(KeyboardButton("contemporary"), KeyboardButton("dancehall"))
    markup.add(KeyboardButton("k-pop"))
    markup.add(KeyboardButton("в главное меню"))
    return markup

def after_contemporary_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("jazz-funk"), KeyboardButton("jazz modern"))
    markup.add(KeyboardButton("hip-hop"), KeyboardButton("dancehall"))
    markup.add(KeyboardButton("k-pop"))
    markup.add(KeyboardButton("в главное меню"))
    return markup

def after_jazzmodern_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("jazz-funk"), KeyboardButton("contemporary"))
    markup.add(KeyboardButton("hip-hop"), KeyboardButton("dancehall"))
    markup.add(KeyboardButton("k-pop"))
    markup.add(KeyboardButton("в главное меню"))
    return markup

def after_jazzfunk_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("jazz modern"), KeyboardButton("contemporary"))
    markup.add(KeyboardButton("hip-hop"), KeyboardButton("dancehall"))
    markup.add(KeyboardButton("k-pop"))
    markup.add(KeyboardButton("в главное меню"))
    return markup

def after_kpop_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("jazz-funk"), KeyboardButton("jazz modern"))
    markup.add(KeyboardButton("contemporary"), KeyboardButton("hip-hop"))
    markup.add(KeyboardButton("dancehall"))
    markup.add(KeyboardButton("в главное меню"))
    return markup

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "добро пожаловать! нажми кнопку, чтобы начать 👇", reply_markup=start_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "начать")
def handle_begin(message):
    started_users.add(message.chat.id)
    bot.send_message(message.chat.id, "привет! чем могу помочь? :3", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() in ["главное меню", "в главное меню"])
def handle_main_menu(message):
    bot.send_message(message.chat.id, HELLO_TEXT, reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "о нас")
def handle_about(message):
    text = (
        "📍 наш адрес:\n"
        "ул. молодогвардейцев 53, 2 этаж (тк карнавал)\n\n"
        "📞 контакты для связи:\n"
        "+7 951 772 98 98\n"
        "e-motion74@bk.ru\n\n"
        "🌐 наш сайт:\n"
        "https://vk.com/away.php?to=https%3A%2F%2Fwww.st-on.ru&utf=1"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "направления")
def handle_directions(message):
    bot.send_message(message.chat.id, "выберите направление", reply_markup=directions_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "воздушные")
def handle_aerial(message):
    bot.send_message(message.chat.id, AERIAL_TEXT, reply_markup=aerial_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "танцевальные")
def handle_dance(message):
    bot.send_message(message.chat.id, DANCE_TEXT, reply_markup=dance_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "педагоги")
def handle_teachers(message):
    bot.send_message(message.chat.id, "выберите направление", reply_markup=teachers_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "dancehall")
def handle_dancehall(message):
    send_video_smart(message.chat.id, "dancehall.mp4", "направление: dancehall\nтренер: катя\nрасписание: пн, ср 18:00")
    bot.send_message(message.chat.id, "выберите направление", reply_markup=after_dancehall_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "hip-hop")
def handle_hiphop(message):
    text = "направление: hip-hop\nтренер: никита\nрасписание: вт, чт 20:00 (15+)\nвт, чт 18:00 (6-9 лет)\nпн 19:00, вт 20:00 (9-14 лет)"
    send_video_smart(message.chat.id, "hiphop.mp4", text)
    bot.send_message(message.chat.id, "выберите направление", reply_markup=after_hiphop_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "contemporary")
def handle_contemporary(message):
    text = "направление: contemporary\nтренер: даша\nрасписание: вт, чт 19:00 (9-13 лет)\nвт, чт 20:00 (17+)"
    send_video_smart(message.chat.id, "contemporary.mp4", text)
    bot.send_message(message.chat.id, "выберите направление", reply_markup=after_contemporary_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "jazz modern")
def handle_jazzmodern(message):
    send_video_smart(message.chat.id, "jazzmodern.mp4", "направление: jazz modern\nтренер: даша\nрасписание: пн, ср 19:00 (17+)")
    bot.send_message(message.chat.id, "выберите направление", reply_markup=after_jazzmodern_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "jazz-funk")
def handle_jazzfunk(message):
    text = "направление: jazz-funk\nтренер: настя\nрасписание: пн, ср 18:00/19:00 (набор закрыт)\nпн, пт 17:00/19:00 (набор закрыт)\nср, пт 18:00 (11+)"
    send_video_smart(message.chat.id, "jazzfunk.mp4", text)
    bot.send_message(message.chat.id, "выберите направление", reply_markup=after_jazzfunk_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "k-pop")
def handle_kpop(message):
    text = "направление: k-pop\nтренер: алёна\nрасписание: сб, вс 12:00 (9-16 лет)\nсб, вс 14:00 (10-16 лет)\nсб, вс 13:00 (группа для родителей 20+)"
    send_video_smart(message.chat.id, "kpop.mp4", text)
    bot.send_message(message.chat.id, "выберите направление", reply_markup=after_kpop_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "расписание")
def handle_schedule(message):
    bot.send_message(message.chat.id, "📅 Расписание доступно у администратора", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "прайс")
def handle_price(message):
    bot.send_message(message.chat.id, PRICE_TEXT, reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "аренда залов")
def handle_rental(message):
    send_video_smart(message.chat.id, "rental.mp4", RENTAL_TEXT)
    bot.send_message(message.chat.id, "выбери раздел 👇", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "абонементы")
def handle_subscriptions(message):
    bot.send_message(message.chat.id, "у вас нет активных абонементов", reply_markup=subscriptions_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "продлить прошлый абонемент")
def handle_renew(message):
    bot.send_message(message.chat.id, "свяжитесь с нами: +7 951 772 98 98", reply_markup=subscriptions_menu())

@bot.message_handler(func=lambda m: m.text and m.text.lower() in ["приобрести новый абонемент", "разовое занятие", "пробное занятие"])
def handle_buy(message):
    bot.send_message(message.chat.id, "выберите направление", reply_markup=buy_directions_menu())

@bot.message_handler(func=lambda m: m.text.lower() == "воздушные 🛒")
def handle_aerial_buy(message):
    bot.send_message(message.chat.id, AERIAL_TEXT, reply_markup=buy_aerial_menu())

@bot.message_handler(func=lambda m: m.text.lower() == "танцевальные 🛒")
def handle_dance_buy(message):
    bot.send_message(message.chat.id, DANCE_TEXT, reply_markup=buy_dance_menu())

@bot.message_handler(func=lambda m: m.text == "◀️ к абонементам")
def handle_back_to_subscriptions(message):
    bot.send_message(message.chat.id, "у вас нет активных абонементов", reply_markup=subscriptions_menu())

@bot.message_handler(content_types=["video"])
def handle_video_message(message):
    if not message.video:
        return
    fid = message.video.file_id
    cap = (message.caption or "").strip().lower()
    if cap in DIRECTION_MAP:
        fname = DIRECTION_MAP[cap]
        fids = load_file_ids()
        fids[fname] = fid
        save_file_ids(fids)
        bot.send_message(message.chat.id, f"✅ Видео для {cap} сохранено!")
    else:
        bot.send_message(message.chat.id, f"📹 file_id:\n{fid}")

@bot.message_handler(func=lambda m: True)
def handle_any(message):
    bot.send_message(message.chat.id, "выбери раздел 👇", reply_markup=main_menu())

if __name__ == "__main__":
    log.info("Бот запущен")
    bot.remove_webhook()
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=True)
        except Exception as e:
            log.error(f"Перезапуск: {e}")
            continue
