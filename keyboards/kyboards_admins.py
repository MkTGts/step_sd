from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXCON_ADMIN_KEYBOARDS


# кнопка возврата в основное меню
but_admin_back_to_main_menu = InlineKeyboardButton(
    text=LEXCON_ADMIN_KEYBOARDS["back_to_main_menu"],
    callback_data="back_to_main_menu"
)

#########################################################################################
# создание инлайн клавиатуры основного меню админа
admin_main_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["users"],
                    callback_data="admin_users"
        )], 
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["operators"],
                    callback_data="admin_operators"
        )], 
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["groups"],
                    callback_data="admin_groups"
        )], 
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["tickets"],
                    callback_data="admin_tickets"
        )]
    ])

#######################################################################################################################################################


# создание инлайн клавиатуры админского подменю Пользователи
admin_submenu_users_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["show_users"],
                    callback_data="admin_show_users"
        )],
#            [InlineKeyboardButton(
#                    text=LEXCON_ADMIN_KEYBOARDS["create_user"],
#                    callback_data="admin_create_user"
#        )],
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["drop_user"],
                    callback_data="admin_drop_user"
        )],
            [but_admin_back_to_main_menu]
    ])

###################################################################################################################################################

# создание инлайн клавиатуры админского подменю Операторы
admin_submenu_operators_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["show_operators"],
                    callback_data="admin_show_operators"
        )],
#            [InlineKeyboardButton(
#                    text=LEXCON_ADMIN_KEYBOARDS["create_operator"],
#                    callback_data="admin_create_operator"
#        )],
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["drop_operator"],
                    callback_data="admin_drop_operator"
        )],
            [but_admin_back_to_main_menu]
    ])

######################################


# создание инлайн клавиатуры админского подменю Организации
admin_submenu_groups_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["show_invite_group"],
                    callback_data="admin_show_invite_group"
        )],
#            [InlineKeyboardButton(
#                    text=LEXCON_ADMIN_KEYBOARDS["show_groups"],
#                    callback_data="admin_show_groups"
#        )],
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["create_group"],
                    callback_data="admin_create_group"
        )],
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["drop_group"],
                    callback_data="admin_drop_group"
        )],
            [but_admin_back_to_main_menu]
    ])


######################################

# создание инлайн клавиатуры админского подменю Тикеты
admin_submenu_tickets_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["show_tickets"],
                    callback_data="admin_show_tickets"
        )],
#            [InlineKeyboardButton(
#                    text=LEXCON_ADMIN_KEYBOARDS["create_tickets"],
#                    callback_data="admin_create_tickets"
#        )],
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["edit_tickets"],
                    callback_data="admin_edit_tickets"
        )],
            [InlineKeyboardButton(
                    text=LEXCON_ADMIN_KEYBOARDS["drop_tickets"],
                    callback_data="admin_drop_tickets"
        )],
            [but_admin_back_to_main_menu]
    ])