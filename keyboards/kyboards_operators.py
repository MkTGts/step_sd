from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_OPERATOR_KEYBOARDS


# кнопка возврата в основное меню
but_operator_back_to_main_menu = InlineKeyboardButton(
    text=LEXICON_OPERATOR_KEYBOARDS["back_to_main_menu"],
    callback_data="operator_back_to_main_menu"
)
#######################################################################

# создание инлайн клавиатуры основного меню оператора
operator_main_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(
                    text=LEXICON_OPERATOR_KEYBOARDS["users"],
                    callback_data="operator_users_list_show"
        )], 
            [InlineKeyboardButton(
                    text=LEXICON_OPERATOR_KEYBOARDS["show_tickets"],
                    callback_data="operator_tickets_show"
        )],
            [InlineKeyboardButton(
                    text=LEXICON_OPERATOR_KEYBOARDS["edit_status"],
                    callback_data="operator_edit_status_ticket"
        )], 
    ])

########################################################################








