from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def KB_default():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/help'))
    kb.add(KeyboardButton('/start'))
    kb.insert(KeyboardButton('/joke'))
    kb.add(KeyboardButton('/create'))
    kb.insert(KeyboardButton('/delete'))
    # kb.add(KeyboardButton('/clear'))
    kb.add(KeyboardButton('/usersJoke'))
    kb.insert(KeyboardButton('/addJoke'))
    kb.add(KeyboardButton('/deleteJokes'))

    return kb


def KB_cancel():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))

    return kb


def IKB():
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='❤️', callback_data="like")
    ib2 = InlineKeyboardButton(text='👎', callback_data="dislike")

    ikb.add(ib1, ib2)

    return ikb


def IKB_like(likes, dislikes):
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(
        text="❤️✅ - '{lik}'".format(lik=int(likes)), callback_data="voted")
    ib2 = InlineKeyboardButton(
        text="👎❌ - '{dislik}'".format(dislik=int(dislikes)), callback_data="voted")

    ikb.add(ib1, ib2)

    return ikb


def IKB_dislike(likes, dislikes):
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(
        text="❤️❌ - '{lik}'".format(lik=int(likes)), callback_data="voted")
    ib2 = InlineKeyboardButton(
        text="👎✅ - '{dislik}'".format(dislik=int(dislikes)), callback_data="voted")
    ikb.add(ib1, ib2)

    return ikb
