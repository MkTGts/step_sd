from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXCON_ADMIN_KEYBOARDS


#кнопка для меню по пользователям
but_admin_users = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["users"],
    callback_data="admin_users"
)

#кнопка для меню по операторам
but_admin_operators = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["operators"],
    callback_data="admin_operators"
)

#кнопка для меню по операторам
but_admin_groups = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["groups"],
    callback_data="admin_groups"
)

#кнопка для тикетов
but_admin_tickets = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["tickets"],
    callback_data="admin_tickets"
)

# создание инлайн клавиатуры основного меню админа
admin_main_inline_kb =InlineKeyboardMarkup(
    inline_keyboard=[[but_admin_users], [but_admin_operators], [but_admin_groups], [but_admin_tickets]]
)







# кнопка для создания пользователя
but_admin_create_user = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["create_user"],
    callback_data="admin_create_user"
)

# кнопка для удаления пользователя
but_admin_drop_user = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["drop_user"],
    callback_data="admin_drop_user"
)

# кнопка для создания оператора
but_admin_create_operator = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["create_operator"],
    callback_data="admin_create_operator"
)

#кнопка для удаленяи оператора
but_admin_drop_operator = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["drop_operator"],
    callback_data="admin_drop_operator"
)

#кнопка для создания группы
but_admin_create_group = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["create_group"],
    callback_data="admin_create_group"
)

#кнопка для удаления группы
but_admin_drop_group = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["drop_group"],
    callback_data="admin_drop_group"
)



