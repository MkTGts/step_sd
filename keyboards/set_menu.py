from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import LEXICON_COMMANDS_RU
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



# создание инлайн клавиатуры основного меню админа
ticket_status_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(
                    text="Открыта",
                    callback_data="open"
        )], 
            [InlineKeyboardButton(
                    text="В работе",
                    callback_data="in_work"
        )], 
            [InlineKeyboardButton(
                    text="Закрыта",
                    callback_data="closed"
        )]
    ])


# функция кнопок меню
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command=command, description=description
                   ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    await bot.set_my_commands(main_menu_commands)