from aiogram import Bot, Dispatcher, types, html
from config import BOT_API
import asyncio
import unicodedata
from pdf2image import convert_from_path
import logging
import random

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove , InlineKeyboardButton ,InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram import F
from aiogram.utils.formatting import Url
from aiogram.types import Animation
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart, chat_member_updated
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
import subprocess

logging.basicConfig(level=logging.INFO)
bot = Bot(BOT_API, parse_mode="HTML")
dp = Dispatcher()

Menu = """
/start - начнём
/help - информация
/fuck_you - попробуй
/compliment -сделать комплимент
/life - жизненный вопрос
/game - игра
/links - ..
/Valentinka - отправить ваентинку
"""
Menulst = ["/start", "/help", "/fuck_you", "/compliment", "/photo", "/life" ]
Guesslst = {}  

@dp.message(Command("links"))
async def cmd(message: Message):
    Startbtn = InlineKeyboardButton(text="GitHub", url="https://github.com")
    keyboard = [
        [Startbtn]
    ]

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    
    await message.answer(
        text="hjj",
        reply_markup=reply_markup,
        #disable_web_page_preview=True
    )

@dp.message(Command("fuck_you"))
async def poslat(message: types.Message):
    if message.text.startswith('/fuck_you'):
        name = message.from_user.first_name
        if name == 'Валерия':
             await message.reply(f"Булочка, не воняй!")
        else:
            await message.reply(f"{name} , иди нахуй")

user_data = {}

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Создать валентинку", callback_data="text"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@dp.message(Command("Valentinka"))
async def cmd_numbers(message: types.Message):
    
    await message.answer("Укажите текст валентинки: ")

    user_data[message.from_user.id] = {"waiting_for_text": True, "text": ""}

@dp.message(lambda message: user_data.get(message.from_user.id, {}).get("waiting_for_text", False))
async def save_text(message: Message):
    # Save the text provided by the user
    with open("val.txt", "w", encoding="utf-8") as file:
        file.write(message.text)

    subprocess.run(["python", "drownphoto.py"])

    

    await message.answer_photo(FSInputFile("output.jpg"))
    
    user_data[message.from_user.id]["text"] = message.text
    user_data[message.from_user.id]["waiting_for_text"] = False  # Update the state

    await message.answer("Текст валентинки сохранен.")

@dp.message(Command('send_message'))
async def send_message(message: types.Message):
    # Prompt the user to select a recipient from their contacts
    button = InlineKeyboardButton(text="Recipient 1", callback_data="recipient_1")
    keyboard = [
        [button]
        #InlineKeyboardButton("Recipient 2", callback_data="recipient_2"),
        #InlineKeyboardButton("Recipient 3", callback_data="recipient_3")]
    ]
    x = InlineKeyboardMarkup(inline_keyboard= keyboard)
    await message.answer("Please select a recipient from your contacts:", reply_markup=x)

# Handler for handling user selection from the inline keyboard
@dp.callback_query(lambda query: query.data.startswith('recipient_'))
async def handle_recipient_selection(query: types.CallbackQuery):
    recipient_id = query.data.split('_')[1]  # Extract recipient ID from the callback data
    message_text = "Hello, this is a test message."  # You can customize the message text here

    # Send the message to the selected recipient using the Telegram API
    try:
        await bot.send_message(chat_id=recipient_id, text=message_text)
        await query.message.answer("Message sent successfully.")
    except Exception as e:
        await query.message.answer(f"Failed to send message. Error: {e}")
#     await ValentinkaText.waiting_for_text.set()

# @dp.message_handler(state=ValentinkaText.waiting_for_text)
# async def save_text(message: types.Message, state: FSMContext):
#     # Save the received text into the user_data dictionary
#     user_data[message.from_user.id] = message.text
    
#     # Inform the user that the text is saved
#     await message.answer("Текст валентинки сохранен.")

#     # Finish the state
#     await state.finish()

    # user_data[message.from_user.id] = message.text
    # #await message.answer(user_data[message.from_user.id])
    # await message.answer("Текст валентинки сохранен.")

# @dp.message(lambda message: user_data.get(x = message.from_user., {}) == "waiting_for_text")
# async def cmd_numbers(message: types.Message):
#     user_data[message.from_user.id] = message.text
#     await message.answer("Текст валентинки сохранен.")



# @dp.callback_query(F.data.startswith("text"))
# async def callbacks_text(callback: types.CallbackQuery):


@dp.message(Command("help"))
async def help(message: types.Message):
    if message.text.startswith('/help'):
        await message.reply(text=Menu)

@dp.message(Command("compliment"))
async def help(message: types.Message):
    if message.text.startswith('/compliment'):
        name = message.from_user.first_name
        
        await message.reply(f"Ахуенно выгядишь {name}!")

# @dp.message(F.chat_)
# async def added(message: Message):
#     for user in new_chat_members:


@dp.message(F.animation)
async def echo_gif(message: Message):
    await message.reply_animation(message.animation.file_id)


@dp.message(Command("start"))
@dp.message(CommandStart(
    deep_link=True, magic=F.args == "start"
))
async def start(message: types.Message):
        name = message.from_user.first_name
        name = name.capitalize()
        await message.answer(f"Здраствуйте <b>{name}</b>, вот что умеет этот бот:")
        await message.answer(text=Menu)
        await message.answer("Осторожно, на сревере замeчен <a href='tg://user?id=6306557886'>чушпан</a>!")
        
@dp.message(Command("game"))
async def game(message: Message):
    await message.answer("Попробуй угадать где монетка")

    Guesslst.clear()

    bldr = ReplyKeyboardBuilder()
    name = "?"
    for i in range(1, 4):
        Guesslst[i] = name
        bldr.add(types.KeyboardButton(text=name))
    
        bldr.adjust(3)
        name += "?"

        
    await message.answer(
            text="Выбери один вариант",
            reply_markup=bldr.as_markup(resize_keyboard=True)
                       
    )
    
    
    

@dp.message(Command("photo"))
async def upload_img(message: Message):
    file_ids = []

    image_from_pc = FSInputFile("buka1.png.jpg")
    result = await message.answer_photo(
        image_from_pc,
        caption="Изображение из файла на компьютере"
    )
    file_ids.append(result.photo[-1].file_id)
        
@dp.message(Command("life"))
async def life(message: Message):
    lst = [
        [
            types.KeyboardButton(text="Барби"),
            types.KeyboardButton(text="Оппенгеймер")
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard = lst,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Только честно"
    )

    await message.answer("Лучший фиьм прошшого года:", reply_markup=keyboard)


@dp.message(F.text.lower() == "барби")
async def mda(message: Message):
    await message.answer("Жаль!")
    lst = [
            [
                types.KeyboardButton(text="Грудь"),
                types.KeyboardButton(text="Жопа")
            ]
        ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard = lst,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Только честно"
    )

    await message.answer("Что важнее:", reply_markup=keyboard)

@dp.message(F.text.lower() == "оппенгеймер")
async def chad(message: Message):
    await message.answer("Отличный выбор!")
    lst = [
            [
                types.KeyboardButton(text="Грудь"),
                types.KeyboardButton(text="Жопа")
            ]
        ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard = lst,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Только честно"
    )

    await message.answer("Что важнее:", reply_markup=keyboard)

@dp.message(F.text.lower() == "грудь")
async def md(message: Message):
    await message.answer("Как скажешь!")

@dp.message(F.text.lower() == "жопа")
async def chd(message: Message):
    await message.answer("Как скажешь!)")

@dp.message(F.text, Command("test"))
async def any_message(message: Message):
    await message.answer(
        #"<b>h</b>",
        "Осторожно, на сревере замчен <a href='tg://user?id=6306557886'>чушпан</a>!", 
        parse_mode=ParseMode.HTML
    )

async def main():
    await dp.start_polling(bot)
# @dp.message()
# async def fuck(message: types.Message):
#     if message.text.startswith('/fuckyou'):
#         await poslat(message)

@dp.message(F.text, Command("parser_info"))
async def extract_data(message: Message):
    data = {
        "url": "<N/A>",
        "email": "<N/A>",
        "code": "<N/A>"
    }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            # Неправильно
            # data[item.type] = message.text[item.offset : item.offset+item.length]
            # Правильно
            data[item.type] = item.extract_from(message.text)
    await message.reply(
        "Вот что я нашёл:\n"
        f"URL: {html.quote(data['url'])}\n"
        f"E-mail: {html.quote(data['email'])}\n"
        f"Пароль: {html.quote(data['code'])}"
    )

@dp.message()
async def gameanswers(message: types.Message):
    if message.text in Guesslst.values():
        ans = random.randint(1,3)
        if Guesslst[ans] == message.text:
            await message.answer("Прaвильно!", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            
        else:
            await message.answer("Непрaвильно!")
            await message.answer("Перетасовали, попроуй ещё раз!")

    else:
        await message.answer("Выбери вариант, используя кнопки.")


@dp.message()
async def echo_capitalize(message: types.Message):
    if message.text not in Menulst:
        await message.answer(text=message.text.capitalize()+"!")
    else:
        return

if __name__ == '__main__':
    asyncio.run(main())

# n case
# from aiogram import F, Router, Bot
# from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
# from aiogram.types import ChatMemberUpdated


# new_member_router = Router()

# @new_member_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
# async def new_member(event: ChatMemberUpdated, bot: Bot):
        
#         await event.answer(f"<b>Hi, {event.new_chat_member.user.first_name}!</b>",
#                     parse_mode="HTML")
# from aiogram.utils.markdown import hide_link

# @dp.message(Command("hidden_link"))
# async def cmd_hidden_link(message: Message):
#     await message.answer(
#         f"{hide_link('https://telegra.ph/file/562a512448876923e28c3.png')}"


    

