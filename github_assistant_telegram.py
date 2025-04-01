import telebot
from telebot import types
import sqlite3
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os

# Database setup
users = {}

with sqlite3.connect('UserInfoTelegram.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, chat_id INTEGER, name TEXT)''')
    conn.commit()


def add_user_to_db(chat_id, name):
    with sqlite3.connect('UserInfoTelegram.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE chat_id = ?''', (chat_id,))
        fetch = cursor.fetchone()
        if fetch is None:
            cursor.execute('''INSERT INTO users(chat_id, name) VALUES (?, ?)''', (chat_id, name))
            conn.commit()
            return True
        return False

def get_user_data(chat_id):
    with sqlite3.connect('UserInfoTelegram.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE chat_id = ?''', (chat_id,))
        fetch = cursor.fetchone()
        if fetch:
            return fetch
        
def get_all_users():
    with sqlite3.connect('UserInfoTelegram.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT chat_id FROM users''')
        users = cursor.fetchall()
        return [user[0] for user in users]
    
async def notify_all_users(message_text):
    user_ids = get_all_users()
    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=message_text)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")
        
def count_users():
    with sqlite3.connect('UserInfoTelegram.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(DISTINCT chat_id) FROM users''')
        count = cursor.fetchone()[0]
        return count

def get_all_users_simple():
    with sqlite3.connect('UserInfoTelegram.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT chat_id , name  FROM users''')
        return cursor.fetchall()

# Bot setup
bot = telebot.TeleBot("8029495212:AAF7JKNFp9aP0W-Krfk4_1rHewQbtK4KELE")

@bot.message_handler(commands=['start'])
def start(message):
    if add_user_to_db(message.chat.id, message.from_user.first_name):
        pass

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🇮🇷 PERSIAN 🇮🇷", callback_data="persian"))
    markup.add(types.InlineKeyboardButton(text="🇬🇧 ENGLISH 🇬🇧", callback_data="english"))
    bot.send_message(message.chat.id, "زبان مورد نظر خود را انتخاب کنید🌐 \n\n Choose your preferred language🌐", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "persian":
        handle_persian_options(call)
    elif call.data == "english":
        handle_english_options(call)

def handle_persian_options(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="⚡اطلاعات حساب⚡", callback_data="fa_api"))
    markup.add(types.InlineKeyboardButton(text="📄ساخت Readme.md📄", callback_data="fa_read"))
    markup.add(types.InlineKeyboardButton(text="🌐تعویض زبان🌐", callback_data="language_switch"))
    bot.send_message(call.message.chat.id, "لطفا یکی از گزینه های زیر را انتخاب کنید🌹", reply_markup=markup)

def handle_english_options(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="⚡Account information⚡", callback_data="en_api"))
    markup.add(types.InlineKeyboardButton(text="📄Creating Readme.md📄", callback_data="en_read"))
    markup.add(types.InlineKeyboardButton(text="🌐Language switching🌐", callback_data="language_switch"))
    bot.send_message(call.message.chat.id, "Please choose one of the options below🌹", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("fa_api"))
def handle_fa_api(call):
    bot.send_message(call.message.chat.id, "لطفا نام کاربری GitHub خود را وارد کنید 🌹")

@bot.callback_query_handler(func=lambda call: call.data.startswith("en_api"))
def handle_en_api(call):
    bot.send_message(call.message.chat.id, "Please enter your GitHub username🌹")

@bot.callback_query_handler(func=lambda call: call.data.startswith("fa_read"))
def handle_fa_read(call):
    bot.send_message(call.message.chat.id, "لطفا کد یا توضیحات پروژه خود را وارد کنید🌹")

@bot.callback_query_handler(func=lambda call: call.data.startswith("en_read"))
def handle_en_read(call):
    bot.send_message(call.message.chat.id, "Please enter your code or a description of your project🌹")

@bot.message_handler(commands=['admin'])
def admin_menu(message):
    if is_admin(message.from_user.id):
        show_admin_options(message.chat.id)
    else:
        notify_not_admin(message.chat.id)

def is_admin(user_id):
    return user_id == 6477459620  

def show_admin_options(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    markup.add("📊آمار ربات📊")
    markup.add("📝پیام به همه📝")
    markup.add("📸عکس به همه📸")
    markup.add("👤پیام به کاربر👤")
    
    bot.send_message(chat_id, "شما ادمین هستید✅", reply_markup=markup)

def notify_not_admin(chat_id):
    bot.send_message(chat_id, "شما ادمین نیستید❌")

@bot.message_handler(func=lambda message: message.text == "📊آمار ربات📊")
def stats(message):
    if message.from_user.id == 6477459620:
        user_count = count_users()
        all_users = get_all_users_simple()
        bot.send_message(message.chat.id, f"📊تعداد کاربران: {user_count} نفر \n\n لیست کاربران : {all_users}")

@bot.message_handler(func=lambda message: message.text == "📝پیام به همه📝")
def message_to_all(message):
    if message.from_user.id == 6477459620:
        bot.send_message(message.chat.id, "لطفا پیام خود را بنویسید ...📝")
        bot.register_next_step_handler(message, send_message_to_all)

def send_message_to_all(message):
    user_ids = get_all_users()
    for user_id in user_ids:
        try:
            bot.send_message(chat_id=user_id, text=message.text)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")
    bot.send_message(message.chat.id, "پیام با موفقیت ارسال شد✅")

@bot.message_handler(func=lambda message: message.text == "📸عکس به همه📸")
def photo_to_all(message):
    if message.from_user.id == 6477459620:  
        button_back_ad = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_back_ad.add("🔙بازگشت به منوی ادمین🔙")
        
        bot.send_message(message.chat.id, "لطفا عکس خود را ارسال کنید.", reply_markup=button_back_ad)
        bot.register_next_step_handler(message, send_photo_to_all)

def send_photo_to_all(message):
    user_ids = get_all_users()
    if message.content_type == 'photo':
        for user_id in user_ids:
            try:
                bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=message.caption)
            except Exception as e:
                print(f"Error sending message to {user_id}: {e}")
        
        bot.send_message(message.chat.id, "عکس با موفقیت به همه ارسال شد✅")
    else:
        bot.send_message(message.chat.id, "لطفا یک عکس ارسال کنید.")

    

@bot.message_handler(func=lambda message: message.text == "👤پیام به کاربر👤")
def message_to_user(message):
    if message.from_user.id == 6477459620:
        bot.send_message(message.chat.id, "چت ایدی مد نظر رو وارد کن")
        bot.register_next_step_handler(message, get_chat_id)

def get_chat_id(message):
    chat_id_user = message.text
    bot.send_message(message.chat.id, "پیام خود را وارد کنید")
    bot.register_next_step_handler(message, lambda msg: send_message_to_user(chat_id_user, msg))

def send_message_to_user(chat_id_user, message):
    bot.send_message(chat_id=chat_id_user, text=f"پیام ارسال شده توسط پشتیبانی 👤\n\n{message.text}")
    bot.send_message(6477459620, "پیام شما با موفقیت فرستاده شد✅")

@bot.message_handler(func=lambda message: True)
def on_message(message):
    if message.text == "🔙بازگشت به منوی ادمین🔙":
        if message.from_user.id == 6477459620: 
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("📊آمار ربات📊"))
            markup.add(types.KeyboardButton("📝پیام به همه📝"))
            markup.add(types.KeyboardButton("📸عکس به همه📸"))
            markup.add(types.KeyboardButton("👤پیام به کاربر👤"))
            bot.send_message(message.chat.id, "شما ادمین هستید✅", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "شما ادمین نیستید❌")

@bot.callback_query_handler(func=lambda call: call.data == "persian")
def handle_persian(call):
    global users
    user_id = str(call.from_user.id)

    if user_id in users.keys() and users[user_id] == "persian":
        bot.answer_callback_query(call.id, "شما نمی‌توانید در حال حاضر با دکمه‌ها تعامل داشته باشید.")
        return

    button = types.InlineKeyboardMarkup()
    button.add(types.InlineKeyboardButton(text="⚡اطلاعات حساب⚡", callback_data="fa_api"))
    button.add(types.InlineKeyboardButton(text="📄ساخت Readme.md📄", callback_data="fa_read"))
    button.add(types.InlineKeyboardButton(text="🌐تعویض زبان🌐", callback_data="language_switch"))
    bot.send_message(call.message.chat.id, "لطفاً یکی از گزینه‌های زیر را انتخاب کنید🌹", reply_markup=button)

@bot.callback_query_handler(func=lambda call: call.data == "english")
def handle_english(call):
    global users
    user_id = str(call.from_user.id)

    if user_id in users.keys() and users[user_id] == "english":
        bot.answer_callback_query(call.id, "You cannot interact with buttons while in GitHub bot.")
        return

    button = types.InlineKeyboardMarkup()
    button.add(types.InlineKeyboardButton(text="⚡Account information⚡", callback_data="en_api"))
    button.add(types.InlineKeyboardButton(text="📄Creating Readme.md📄", callback_data="en_read"))
    button.add(types.InlineKeyboardButton(text="🌐Language switching🌐", callback_data="language_switch"))
    bot.send_message(call.message.chat.id, "Please choose one of the options below🌹", reply_markup=button)

@bot.callback_query_handler(func=lambda call: call.data == "language_switch")
def handle_language_switch(call):
    button = types.InlineKeyboardMarkup()
    button.add(types.InlineKeyboardButton(text="🇮🇷 PERSIAN 🇮🇷", callback_data="persian"))
    button.add(types.InlineKeyboardButton(text="🇬🇧 ENGLISH 🇬🇧", callback_data="english"))
    bot.send_message(call.message.chat.id, "زبان مورد نظر خود را انتخاب کنید🌐 \n\n Choose your preferred language🌐", reply_markup=button)

@bot.callback_query_handler(func=lambda call: call.data == "en_api")
def handle_en_api(call):
    button = types.InlineKeyboardMarkup()
    button.add(types.InlineKeyboardButton(text="🔙back🔙", callback_data="back_en"))
    bot.send_message(call.message.chat.id, "Please enter your GitHub username🌹\n\n example: *Phoenix-110-135*", reply_markup=button)

    @bot.message_handler(func=lambda message: True)
    def handle_github_username(answer_obj):
        if answer_obj.from_user.id == call.from_user.id:
            url_acc_git = f"https://github.com/{answer_obj.text}"
            response = requests.get(url_acc_git)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                name_element = soup.find(class_='p-name vcard-fullname d-block overflow-hidden')
                bio = soup.find(class_='p-note user-profile-bio mb-3 js-user-profile-bio f4')
                image_element = soup.find(class_="position-relative d-inline-block col-2 col-md-12 mr-3 mr-md-0 flex-shrink-0")

                if image_element and image_element.find('img'):
                    image_url = image_element.find('img')['src']
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image = Image.open(BytesIO(image_response.content))
                        image.save("image.png")

                description = bio.get_text(strip=True) if bio else "No description"
                name = name_element.text.strip() if name_element else "Unknown"
                followers, following, Counter = extract_github_data(soup)

                input_file = open("image.png", "rb")
                bot.send_photo(call.message.chat.id, photo=input_file,
                               caption=f"name: *🌪️{name}🌪️* \n followers: *💧{followers}💧*  \n following: *❄️{following}❄️* \n number of repositories: *🔥{Counter}🔥* \n Analysis: *🌙{url} 🌙*  \n description: *⭐{description}⭐*\n\n 🆔@github_assistant_bot")
                input_file.close()
                os.remove("image.png")
            else:
                bot.send_message(call.message.chat.id, "Username does not exist❌")

@bot.callback_query_handler(func=lambda call: call.data == "fa_api")
def handle_fa_api(call):
    button = types.InlineKeyboardMarkup()
    button.add(types.InlineKeyboardButton(text="🔙بازگشت🔙", callback_data="back_fa"))
    bot.send_message(call.message.chat.id, "لطفا نام کاربری GitHub خود را وارد کنید 🌹\n\n مثال: *Phoenix-110-135*", reply_markup=button)

    @bot.message_handler(func=lambda message: True)
    def handle_github_username_fa(answer_obj):
        if answer_obj.from_user.id == call.from_user.id:
            url_acc_git = f"https://github.com/{answer_obj.text}"
            response = requests.get(url_acc_git)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                name_element = soup.find(class_='p-name vcard-fullname d-block overflow-hidden')
                bio = soup.find(class_='p-note user-profile-bio mb-3 js-user-profile-bio f4')
                image_element = soup.find(class_="position-relative d-inline-block col-2 col-md-12 mr-3 mr-md-0 flex-shrink-0")

                if image_element and image_element.find('img'):
                    image_url = image_element.find('img')['src']
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image = Image.open(BytesIO(image_response.content))
                        image.save("image.png")

                description = bio.get_text(strip=True) if bio else "No description"
                name = name_element.text.strip() if name_element else "Unknown"
                followers, following, Counter = extract_github_data(soup)

                input_file = open("image.png", "rb")
                bot.send_photo(call.message.chat.id, photo=input_file,
                               caption=f"نام: *🌪️{name}🌪️* \n دنبال کنندگان: *💧{followers}💧*  \n دنبال شوندگان: *❄️{following}❄️* \n تعداد مخازن: *🔥{Counter}🔥* \n تحلیل: *🌙{url} 🌙* \n توضیحات: *⭐{description}⭐*\n\n 🆔@github_assistant_bot")
                input_file.close()
                os.remove("image.png")
            else:
                bot.send_message(call.message.chat.id, "نام کاربری وجود ندارد❌")

def extract_github_data(soup):
    content = soup.find_all(class_='text-bold color-fg-default')
    counter_element = soup.find(class_='Counter')
    followers = content[0].text.strip() if len(content) > 0 else "0"
    following = content[1].text.strip() if len(content) > 1 else "0"
    Counter = counter_element.text.strip() if counter_element else "0"
    return followers, following, Counter

if __name__ == "__main__":
    bot.polling(none_stop=True)
