import random
from aiogram import Bot, Dispatcher, types, executor
from keyboarddd import KB_default, KB_cancel, IKB, IKB_like, IKB_dislike
from sqlite import DataBase_start, edit_profile, create_profile, delete_profile
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import sqlite3 as sq
from jokesfromusers import DataBase_User_Jokes, add_user_joke, delAllJokes, get_joke_from_user
from jokesfrombot import get_joke

API = '6816973281:AAHfQuHR8M5iYjAwiLD2fpnRAUVQzf79_vA'
WasCreated = False
User_joke = True

# задает функции которые выполняются при старте


async def on_start(_):
    await DataBase_start()
    await DataBase_User_Jokes()

storage = MemoryStorage()
bot = Bot(API)
dp = Dispatcher(bot=bot, storage=storage)

# обновление лайков в бд


def update_vote(Likes, Dislikes, idd):
    global User_joke
    if (User_joke):
        dbb = sq.connect('JokesFromUsers.db')
    else:
        dbb = sq.connect('JokesFromBot.db')
    curr = dbb.cursor()
    curr.execute("UPDATE Jokes SET likes = '{}', dislikes = '{}' WHERE id == '{}'".format(
        Likes, Dislikes, idd))
    dbb.commit()

# для создания профиля


class ProfileState(StatesGroup):
    delete = State()
    photo = State()
    name = State()
    age = State()
    description = State()

# для добавления добавления и удаления шуток


class JokeState(StatesGroup):
    add = State()
    delAll = State()

# команда старта бота


@dp.message_handler(commands=['start'])
async def Start(message: types.Message) -> None:
    global WasCreated
    WasCreated = await create_profile(message.from_user.id)
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAJYiGVTSHB-SuhptBTryUYnCpC1FiWjAAKmGAACbjORSfydxNIpDtJoMwQ", reply_markup=KB_default())
    await message.delete()

# показывает все команды


@dp.message_handler(commands=['help'])
async def Help(message: types.Message) -> None:
    message_help = '''Its all commands that you can use:
    /start - start the bot
    /joke - get joke from bot
    /create - create a profile
    /delete - delete your profile
    /usersJoke - get joke from other user
    /addJoke - add joke
'''
    await bot.send_message(message.from_user.id, message_help, reply_markup=KB_default())

# создание профиля


@dp.message_handler(commands=['create'])
async def Create_profile(message: types.Message) -> None:
    global WasCreated
    if not WasCreated:
        await message.reply("Lets create your profile. Send photo for profile picture.", reply_markup=KB_cancel())
        await ProfileState.photo.set()
    else:
        await message.reply("U have created profile.")

# отмена какой-либо операции


@dp.message_handler(commands=['cancel'], state='*')
async def Cancel(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    await message.reply('You canceled your operation', reply_markup=KB_default())

# удаление профиля


@dp.message_handler(commands=['delete'])
async def Del_profile(message: types.Message) -> None:
    global WasCreated
    if WasCreated:
        await message.reply("Are u sure that u want to delete your profile?\n Say 'YES', if u wanna delete your profile.")
        await ProfileState.delete.set()
    else:
        await message.reply("You dont have profile")

# продтверждение удаления


@dp.message_handler(state=ProfileState.delete)
async def CheckerDel(message: types.Message, state: FSMContext):
    global WasCreated
    if str(message.text) == "YES":
        WasCreated = False
        await delete_profile(user_id=message.from_user.id)
        await delAllJokes(user_id=message.from_user.id)
        await message.reply("Ok, your profile delete")
        await state.finish()
    else:
        await message.reply("Ok, your profile not delete")
        await state.finish()

# проверка на то, что боту отправили фото


@dp.message_handler(lambda message: not message.photo, state=ProfileState.photo)
async def CheckerPhoto(message: types.Message):
    await message.reply('This is not photo, try again')

# добавление фото для профиля


@dp.message_handler(content_types=['photo'], state=ProfileState.photo)
async def SetPhoto(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.reply("Now, send me your name.")
    await ProfileState.next()

# проверка на текст


@dp.message_handler(lambda message: not message.text, state=ProfileState.name)
async def CheckerText(message: types.Message):
    await message.reply('This is not text, try again')

# добавление имени к профилю


@dp.message_handler(state=ProfileState.name)
async def SetName(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply("How old are you?")
    await ProfileState.next()

# проверка на число


@dp.message_handler(lambda message: not message.text.isdigit(), state=ProfileState.age)
async def CheckerPhoto(message: types.Message):
    await message.reply('This is not age, try again')

# добавление возраста


@dp.message_handler(state=ProfileState.age)
async def SetAge(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply("Tell something about yourself.")
    await ProfileState.next()

# проверка на текст


@dp.message_handler(lambda message: not message.text, state=ProfileState.description)
async def CheckerTextDesc(message: types.Message):
    await message.reply('This is not text, try again')

# добавление описания к профилю


@dp.message_handler(state=ProfileState.description)
async def SetDescription(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_photo(chat_id=message.from_user.id, photo=data['photo'], caption=f"{data['name']}, {data['age']}\n{data['description']}")
    await edit_profile(state, user_id=message.from_user.id)
    await state.finish()
    await message.reply('All good', reply_markup=KB_default())


# @dp.message_handler(commands=['cancel'], state='*')
# async def Cancel(message: types.Message, state: FSMContext) -> None:
#     await state.finish()
#     await message.reply('You canceled your operation', reply_markup=KB_default())

# добавление шутки
@dp.message_handler(commands=['addJoke'])
async def AddUsersJoke(message: types.Message) -> None:
    global WasCreated
    print(f"{WasCreated}" + " v add ")
    if not WasCreated:
        await message.reply("You need to create profile for post joke.")
    else:
        await message.reply("Write a joke here", reply_markup=KB_cancel())
        await JokeState.add.set()

# проверка на текст


@dp.message_handler(lambda message: not message.text, state=JokeState.add)
async def CheckerTextJoke(message: types.Message):
    await message.reply('This is not text, try again')

# добавление


@dp.message_handler(content_types=['text'], state=JokeState.add)
async def AddUsersJoke(message: types.Message, state: FSMContext) -> None:
    await add_user_joke(message.from_user.id, message.text)
    await message.reply('You have added the joke', reply_markup=KB_default())
    await state.finish()

# подтверждение удаления шуток


@dp.message_handler(commands=['deleteJokes'])
async def DelJokes(message: types.Message) -> None:
    await message.reply("Are u sure that u want to delete your jokes?\n Say 'YES', if u wanna delete your jokes.")
    await JokeState.delAll.set()

# удаление шуток


@dp.message_handler(state=JokeState.delAll)
async def CheckerDelJokes(message: types.Message, state: FSMContext):
    if str(message.text) == "YES":
        await delAllJokes(user_id=message.from_user.id)
        await message.reply("Ok, your jokes delete")
        await state.finish()
    else:
        await message.reply("Ok, your profile not delete")
        await state.finish()


# @dp.message_handler(commands=['clear'])
# async def clear(message: types.Message) -> None:
#     for i in range(message.message_id, 0, -1):
#         try:
#             await bot.delete_message(message.from_user.id, i)
#         except:
#             print('no')
#     await message.delete()

# получение шуток от бота
@dp.message_handler(commands=['joke'])
async def Joke(message: types.Message):
    global User_joke
    global id_jokee
    global Likes, Dislikes
    User_joke = False
    anecdot, id_jokee, Likes, Dislikes = await get_joke()
    anecdot = anecdot[2:-3]
    await bot.send_message(chat_id=message.from_user.id, text=f'{anecdot}', reply_markup=IKB())
    print('nooo1')
    await message.delete()

# получение шуток от юзеров


@dp.message_handler(commands=['usersJoke'])
async def JokeFromUser(message: types.Message):
    global User_joke
    global id_jokee
    global Likes, Dislikes
    User_joke = True
    anec, id_jokee, Likes, Dislikes = await get_joke_from_user()
    print(anec)
    await bot.send_message(chat_id=message.from_user.id, text=f'{anec}', reply_markup=IKB())
    print('nooo2')
    await message.delete()

# проверка на оценку шутки


@dp.callback_query_handler(text="voted")
async def vote_callback(call: types.CallbackQuery):
    await call.answer('You have voted')

# оценка шутки


@dp.callback_query_handler()
async def vote_callback(call: types.CallbackQuery):
    global Likes, Dislikes
    print('dadadad')
    if call.data == 'like':
        await call.answer('You liked this joke')
        Likes = int(Likes) + 1
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=IKB_like(Likes, Dislikes))
        update_vote(Likes, Dislikes, id_jokee)
    elif call.data == 'dislike':
        Dislikes = int(Dislikes) + 1
        await call.answer(text='You disliked this joke')
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=IKB_dislike(Likes, Dislikes))
        update_vote(Likes, Dislikes, id_jokee)

# если пользователь не хочет шуток)


@dp.message_handler()
async def RandomWord(message: types.Message):
    await message.answer(message.text + '🤡')

# старт мейна
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
