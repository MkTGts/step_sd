from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


# кнопка для вывода списка тикетов пользователя
but_user_tickets_list = InlineKeyboardButton(
    text="Список моих тикетов",
    callback_data="but2"
)

# кнопка для начала создания тикета пользоватеолем
but_user_create_ticket = InlineKeyboardButton(
    text="Создать тикет",
    callback_data="but1"
)

# создание инлайн клавиатуры пользователя
user_inline_kb =InlineKeyboardMarkup(
    inline_keyboard=[[but_user_create_ticket], [but_user_tickets_list]]
)














