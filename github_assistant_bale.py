from bale import Bot,Message,Update,MenuKeyboardButton,InputFile,MenuKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,LabeledPrice,CallbackQuery
from random import randint, choice
import sqlite3
from json import loads, dumps
import requests
import os
import time as t
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
# database

users = {}

with sqlite3.connect('UserInfoBale.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, chat_id INTEGER, name TEXT)''')
    conn.commit()


def add_user_to_db(chat_id, name):
    with sqlite3.connect('UserInfoBale.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE chat_id = ?''', (chat_id,))
        fetch = cursor.fetchone()
        if fetch is None:
            cursor.execute('''INSERT INTO users(chat_id, name) VALUES (?, ?)''', (chat_id, name))
            conn.commit()
            return True
        return False

def get_user_data(chat_id):
    with sqlite3.connect('UserInfoBale.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE chat_id = ?''', (chat_id,))
        fetch = cursor.fetchone()
        if fetch:
            return fetch
        
def get_all_users():
    with sqlite3.connect('UserInfoBale.db') as conn:
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
    with sqlite3.connect('UserInfoBale.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(DISTINCT chat_id) FROM users''')
        count = cursor.fetchone()[0]
        return count

def get_all_users_simple():
    with sqlite3.connect('UserInfoBale.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT chat_id , name  FROM users''')
        return cursor.fetchall()

# end database
bot = Bot(token="") 

@bot.event 
async def on_ready():
    print(bot.user.username,"is Ready")

@bot.event
async def on_message(message:Message):
    if message.content == "/start" :
        if add_user_to_db(message.chat.id,message.author.first_name) == True:
            pass

        button  = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="🇮🇷 PERSIAN 🇮🇷",callback_data="persian"),row=1)
        button.add(InlineKeyboardButton(text="🇬🇧 ENGLISH 🇬🇧",callback_data="english"),row=3)
        await message.reply("زبان مورد نظر خود را انتخاب کنید🌐 \n\n Choose your preferred language🌐",components=button)
##################     admiin       #################
@bot.event
async def on_message(message:Message):
    if message.content == "/admin" :
            if message.from_user.chat_id == "1212421567":
                button_admin = MenuKeyboardMarkup()
                button_admin.add(MenuKeyboardButton("📊آمار ربات📊"),row=1)
                button_admin.add(MenuKeyboardButton("📝پیام به همه📝"),row=3)
                button_admin.add(MenuKeyboardButton("📸عکس به همه📸"),row=5)
                button_admin.add(MenuKeyboardButton("👤پیام به کاربر👤"),row=9)
                await message.reply("شما ادمین هستید✅",components=button_admin)
            else:
                await message.reply("شما ادمین نیستید❌")


@bot.event 
async def on_message(message:Message):
    if message.content == "📊آمار ربات📊":
        if message.from_user.chat_id == "1212421567":
            button_back_ad = MenuKeyboardMarkup()
            button_back_ad.add(MenuKeyboardButton("🔙بازگشت به منوی ادمین🔙"))
            if message.content != "🔙بازگشت به منوی ادمین🔙":
                user_count = count_users()
                all_users = get_all_users_simple()
                await message.reply(f"📊تعداد کاربران: {user_count} نفر \n\n لیست کاربران : {all_users}",components=button_back_ad)
@bot.event 
async def on_message(message:Message):
    if message.content == "📝پیام به همه📝":
        if message.from_user.chat_id == "1212421567":
            button_back_ad = MenuKeyboardMarkup()
            button_back_ad.add(MenuKeyboardButton("🔙بازگشت به منوی ادمین🔙"))
            if message.content != "🔙بازگشت به منوی ادمین🔙":
                await message.reply("لطفا پیام خود را بنویسید ...📝")
                def answer_checker(m: Message):
                    return message.author == m.author and bool(message.text)
                answer_obj: Message = await bot.wait_for('message', check=answer_checker)
                if answer_obj.text != "🔙بازگشت به منوی ادمین🔙":
                    ans = answer_obj.text
                    await notify_all_users(ans)
                    await bot.send_message(chat_id="1212421567",text="پیام با موفقیت ارسال شد✅",components=button_back_ad)
@bot.event
async def on_message(message: Message):
    if message.content == "📸عکس به همه📸":
        if message.from_user.id == 1212421567:  
            button_back_ad = MenuKeyboardMarkup()
            button_back_ad.add(MenuKeyboardButton("🔙بازگشت به منوی ادمین🔙"))
            
            if message.content != "🔙بازگشت به منوی ادمین🔙":
                await bot.send_message(message.chat.id, "ارسال کنید .....", delete_after=4)
                user_ids = get_all_users()
                
                class CopyMessage:
                    def __init__(self):
                        self.bot = bot
                            
                    async def copy_message(self, message: Message, chat_id):
                        try:
                            await self.bot.send_photo(chat_id, InputFile(message.photos[0].file_id), caption=message.caption)
                        except Exception as e:
                            print(f"Error sending message to {chat_id}: {e}")
                
                @bot.event
                async def on_message(message: Message):
                    copier = CopyMessage()
                    for user_id in user_ids:
                        await copier.copy_message(message, user_id)
                    await message.reply("پیام شما با موفقیت به همه ارسال شد✅", components=button_back_ad)


@bot.event 
async def on_message(message:Message):
    if message.content == "👤پیام به کاربر👤":
        if message.from_user.chat_id == "1212421567":
            button_back_ad = MenuKeyboardMarkup()
            button_back_ad.add(MenuKeyboardButton("🔙بازگشت به منوی ادمین🔙"))
            await message.reply("چت ایدی مد نظر رو وارد کن",components=button_back_ad)
            if message.content != "🔙بازگشت به منوی ادمین🔙":
                def answer_checker(m: Message):
                        return message.author == m.author and bool(message.text)
                answer_obj: Message = await bot.wait_for('message', check=answer_checker)
                if answer_obj.text  != "🔙بازگشت به منوی ادمین🔙":
                    chat_id_user = answer_obj.text
                    await message.reply("پیام خود را وارد کنید",components=button_back_ad)
                    def answer_checker2(m: Message):
                            return message.author == m.author and bool(message.text)
                    answer_obj2: Message = await bot.wait_for('message', check=answer_checker2)
                    if answer_obj2.text != "🔙بازگشت به منوی ادمین🔙":
                        mess = answer_obj2.text
                        await bot.send_message(chat_id=chat_id_user,text=f"پیام ارسال شده توسط پشتیبانی 👤\n\n{mess}")
                        await bot.send_message(1212421567,"پیام شما با موفقیت فرستاده شد✅",components=button_back_ad)
                
            

@bot.event 
async def on_message(message:Message):
    if message.content == "🔙بازگشت به منوی ادمین🔙":
        if message.from_user.chat_id == "1212421567":
            button_admin = MenuKeyboardMarkup()
            button_admin.add(MenuKeyboardButton("📊آمار ربات📊"),row=1)
            button_admin.add(MenuKeyboardButton("📝پیام به همه📝"),row=3)
            button_admin.add(MenuKeyboardButton("📸عکس به همه📸"),row=5)
            button_admin.add(MenuKeyboardButton("👤پیام به کاربر👤"),row=9)
            await message.reply("شما ادمین هستید✅",components=button_admin)
        else:
            await message.reply("شما ادمین نیستید❌")

@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "persian":
        return await callback.message.reply("you cannot interact with buttons while in github bot")
    if callback.data == "persian":
        button = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="⚡اطلاعات حساب⚡",callback_data="fa_api"),row=1)
        button.add(InlineKeyboardButton(text="📄ساخت Readme.md📄",callback_data="fa_read"),row=3)
        button.add(InlineKeyboardButton(text="🌐تعویض زبان🌐",callback_data="language_switch"),row=5)
        await callback.message.reply("لطفا یکی از گزینه های زیر را انتخاب کنید🌹",components=button)


@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "english":
        return await callback.message.reply("you cannot interact with buttons while in github bot")
    if callback.data == "english":
        button = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="⚡Account information⚡",callback_data="en_api"),row=1)
        button.add(InlineKeyboardButton(text="📄Creating Readme.md📄",callback_data="en_read"),row=3)
        button.add(InlineKeyboardButton(text="🌐Language switching🌐",callback_data="language_switch"),row=5)

        await callback.message.reply("Please choose one of the options below🌹",components=button)

@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "language_switch":
        return await callback.message.reply("you cannot interact with buttons while in github bot")
    if callback.data == "language_switch":
        button  = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="🇮🇷 PERSIAN 🇮🇷",callback_data="persian"),row=1)
        button.add(InlineKeyboardButton(text="🇬🇧 ENGLISH 🇬🇧",callback_data="english"),row=3)
        await callback.message.reply("زبان مورد نظر خود را انتخاب کنید🌐 \n\n Choose your preferred language🌐",components=button)

@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "en_api":
        return await callback.message.reply("you cannot interact with buttons while in github bot")
    if callback.data == "en_api":
        button = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="🔙back🔙",callback_data="back_en"),row=1)
        await callback.message.reply("Please enter your GitHub username🌹\n\n example : *Phoenix-110-135*",components=button)
        if callback.data != "back_en" and callback.data != "back_fa":
            def answer_checker(m: Message):
                return callback.user == m.author and bool(m.text)
            answer_obj: Message = await bot.wait_for('message', check=answer_checker)
            url_acc_git = f"https://github.com/{answer_obj.text}"            
            response = requests.get(url_acc_git)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.find_all(class_='text-bold color-fg-default')
                name_element = soup.find(class_='p-name vcard-fullname d-block overflow-hidden')
                bio = soup.find(class_='p-note user-profile-bio mb-3 js-user-profile-bio f4')
                image_element = soup.find(class_="position-relative d-inline-block col-2 col-md-12 mr-3 mr-md-0 flex-shrink-0")
                if image_element and image_element.find('img'):
                    image_url = image_element.find('img')['src']
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image = Image.open(BytesIO(image_response.content))
                        image.save("image.png")
                if bio:
                    description = bio.get_text(strip=True)
                counter_element = soup.find(class_='Counter')
                if name_element:
                    name = name_element.text.strip()
                if counter_element:
                    Counter = counter_element.text.strip()
                numbers_found = []
                for item in content:
                    text = item.text.strip()
                    numbers_found.append(text)
                followers = numbers_found[0]
                following = numbers_found[1]
                file = open("image.png","rb").read()
                input_file = InputFile(file)
                url = f"https://profile-summary-for-github.com/user/{answer_obj.text}"
                await callback.message.reply_photo(photo=input_file,caption=f"name : *🌪️{name}🌪️* \n followers : *💧{followers}💧*  \n following : *❄️{following}❄️* \n number of repositories : *🔥{Counter}🔥* \n Analysis : *🌙{url} 🌙*  \n description: *⭐{description}⭐*\n\n 🆔@github_assistant_bot",components=button)
                os.remove("image.png")

            else:
                await callback.message.reply("Username does not exist❌",components=button)

@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "fa_api":
        return await callback.message.reply("you cannot interact with buttons while in github bot")
    if callback.data == "fa_api":
        button = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="🔙بازگشت🔙",callback_data="back_fa"),row=1)
        await callback.message.reply("لطفا نام کاربری GitHub خود را وارد کنید 🌹\n\n مثال : *Phoenix-110-135*",components=button)
        if callback.data != "back_en" and callback.data != "back_fa":
            def answer_checker(m: Message):
                return callback.user == m.author and bool(m.text)
            answer_obj: Message = await bot.wait_for('message', check=answer_checker)
            url_acc_git = f"https://github.com/{answer_obj.text}"
            response = requests.get(url_acc_git)
            if response.status_code == 200:

                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.find_all(class_='text-bold color-fg-default')
                name_element = soup.find(class_='p-name vcard-fullname d-block overflow-hidden')
                bio = soup.find(class_='p-note user-profile-bio mb-3 js-user-profile-bio f4')
                image_element = soup.find(class_="position-relative d-inline-block col-2 col-md-12 mr-3 mr-md-0 flex-shrink-0")
                if image_element and image_element.find('img'):
                    image_url = image_element.find('img')['src']
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image = Image.open(BytesIO(image_response.content))
                        image.save("image.png")
                if bio:
                    description = bio.get_text(strip=True)
                counter_element = soup.find(class_='Counter')
                if name_element:
                    name = name_element.text.strip()
                if counter_element:
                    Counter = counter_element.text.strip()
                numbers_found = []
                for item in content:
                    text = item.text.strip()
                    numbers_found.append(text)
                followers = numbers_found[0]
                following = numbers_found[1]
                file = open("image.png","rb").read()
                input_file = InputFile(file)
                url = f"https://profile-summary-for-github.com/user/{answer_obj.text}"

                await callback.message.reply_photo(photo=input_file,caption=f"نام : *🌪️{name}🌪️* \n دنبال کنندگان : *💧{followers}💧*  \n دنبال شوندگان : *❄️{following}❄️* \n  تعداد مخازن : *🔥{Counter}🔥* \n تحلیل : *🌙{url} 🌙* \n توضیحات : *⭐{description}⭐*\n\n 🆔@github_assistant_bot",components=button)
                os.remove("image.png")

            else:
                await callback.message.reply("نام کاربری وجود ندارد❌",components=button)

@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "en_read":
        return await callback.message.reply("you cannot interact with buttons while in github bot")
    if callback.data == "en_read":
        button = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="🔙back🔙",callback_data="back_en"),row=1)
        await callback.message.reply('''Please enter your code or a description of your project🌹\n\n Example:``` * 
        Project Title: The name of the project.
        Description: A brief overview of what the project does and its purpose.
        Table of Contents: A list of sections included in the README.
        Installation: Instructions on how to install the project, including any dependencies.
        Usage: Examples of how to use the project, including code snippets.
        Contributing: Guidelines for contributing to the project.
        License: Information about the project's license.```
        *''',components=button)
        if callback.data != "back_en" and callback.data != "back_fa":
            def message_checker(m: Message):
                return m.from_user.id == callback.user.id

            user_message: Message = await bot.wait_for('message', check=message_checker)
            await bot.send_message(callback.message.chat_id,"please wait ...😉")

            if user_message.document :
                document = user_message.document
            
                file_info = await bot.get_file(document.file_id)
            
            
                with open("test.txt", "wb") as f:
                    f.write(file_info)
                    
                with open("test.txt", "r", encoding='utf-8') as f:
                    text = f.read()
                os.remove("test.txt")

            else:
                text = user_message.text

            qu = ("create README.md for my github " , text)
            response = requests.get(f"https://api.daradege.ir/ai?text={qu}")
            if response.status_code == 200:
                js = response.json()
                await callback.message.reply(js['text'], components=button)
                
            else:
                await callback.message.reply("API HAS ERROR!")



@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "fa_read":
        return await callback.message.reply("you cannot interact with buttons while in github bot")
    if callback.data == "fa_read":
        button = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="🔙بازگشت🔙",callback_data="back_fa"),row=1)
        await callback.message.reply('''لطفا کد یا توضیحات پروژه خود را وارد کنید🌹\n\n مثال: ``` * 
        عنوان پروژه: نام پروژه.
        توضیحات: مروری کوتاه بر آنچه پروژه انجام می دهد و هدف آن.
        فهرست مطالب: فهرستی از بخش های موجود در README.
        نصب: دستورالعمل نحوه نصب پروژه، از جمله هر گونه وابستگی.
        استفاده: نمونه هایی از نحوه استفاده از پروژه، از جمله قطعه کد.
        مشارکت: رهنمودهایی برای مشارکت در پروژه.
        مجوز: اطلاعات مربوط به مجوز پروژه.
        *```''',components=button)
        if callback.data != "back_en" and callback.data != "back_fa":
            def message_checker(m: Message):
                return m.from_user.id == callback.user.id

            user_message: Message = await bot.wait_for('message', check=message_checker)
            await bot.send_message(callback.message.chat_id,"لطفا منتظر بمانید...😉")


            if user_message.document :
                document = user_message.document
            
                file_info = await bot.get_file(document.file_id)
            
            
                with open("test.txt", "wb") as f:
                    f.write(file_info)
                    
                with open("test.txt", "r", encoding='utf-8') as f:
                    text = f.read()
                os.remove("test.txt")
            else:
                text = user_message.text

            qu = ("برای گیتهابم یک readme.md درست کن با کد و مشخصات " , text)
            response = requests.get(f"https://api.daradege.ir/ai?text={qu}")
            if response.status_code == 200:
                js = response.json()
                await callback.message.reply(js['text'], components=button)
                
            else:
                await callback.message.reply("خطا در برقراری api!")
            

@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "back_en":
        return await callback.message.reply("you cannot interact with buttons while in github bot")
    if callback.data == "back_en":
        button = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="⚡Account information⚡",callback_data="en_api"),row=1)
        button.add(InlineKeyboardButton(text="📄Creating Readme.md📄",callback_data="en_read"),row=3)
        button.add(InlineKeyboardButton(text="🌐Language switching🌐",callback_data="language_switch"),row=5)

        await callback.message.reply("Please choose one of the options below🌹",components=button)

@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "back_fa":
        return await callback.message.reply("you cannot interact with buttons while in github bot")
    if callback.data == "back_fa":
        button = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="⚡اطلاعات حساب⚡",callback_data="fa_api"),row=1)
        button.add(InlineKeyboardButton(text="📄ساخت Readme.md📄",callback_data="fa_read"),row=3)
        button.add(InlineKeyboardButton(text="🌐تعویض زبان🌐",callback_data="language_switch"),row=5)
        await callback.message.reply("لطفا یکی از گزینه های زیر را انتخاب کنید🌹",components=button)
    
bot.run()
