from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXCON_USER_KEYBOARS


# кнопка для вывода списка тикетов пользователя
but_user_tickets_list = InlineKeyboardButton(
    text=LEXCON_USER_KEYBOARS["tickets_list"],
    callback_data="user_tickets_list"
)

# кнопка для начала создания тикета пользоватеолем
but_user_create_ticket = InlineKeyboardButton(
    text=LEXCON_USER_KEYBOARS["create_ticket"],
    callback_data="user_create_ticket"
)

# создание инлайн клавиатуры пользователя
user_inline_kb =InlineKeyboardMarkup(
    inline_keyboard=[[but_user_create_ticket], [but_user_tickets_list]]
)














