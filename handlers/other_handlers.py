import logging
from aiogram import Router
from aiogram.types import Message
from handlers.base import base
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command
from filters.filter import IsRegistredUserInvite
from keyboards.kyboards_users import user_inline_kb
from keyboards.kyboards_admins import admin_main_inline_kb
from keyboards.kyboards_operators import operator_main_inline_kb


# инициализация логгера
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format= '[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)


router = Router()  # подключение роутера


# хэндлер на команду старт
@router.message(Command(commands="start"))
async def process_command_start(message: Message):
    # проверка есть ли пользователь в базе 
    if base._check_role(tg_id=message.from_user.id) is None:
        await message.answer(
            text=LEXICON_RU["not_reg"]
        )
        await message.answer(
            text="Для регистрации введите ИНН вашей организцаии."
        )
        logger.info(f"Пришла команда старт от незарегистрированного пользователя с  TG ID {message.from_user.id}")
    elif base._check_role(tg_id=message.from_user.id) == "user":
        await message.answer(
            text="Авторизация пользователя пройдена",
            reply_markup=user_inline_kb
        )
    elif base._check_role(tg_id=message.from_user.id) == "admin":
        await message.answer(
            text="Авторизация администратора пройдена",
            reply_markup=admin_main_inline_kb
        )
    elif base._check_role(tg_id=message.from_user.id) == "operator":
        await message.answer(
            text="Авторизация оператора пройдена",
            reply_markup=[operator_main_inline_kb.append(user_inline_kb)]
        )



@router.message(IsRegistredUserInvite())
async def process_registaration_user_invite(message: Message):
    if base._in_invite(invite_token=int(message.text)):
        base.user_registration(
            invite_token=int(message.text),
            tg_id=int(message.from_user.id),
            username=message.from_user.username
        )
        await message.answer(
            text=LEXICON_RU["registration_invite_ok"]
        )
    elif base._return_info_on_inn(inn=str(message.text)):
        org = base._return_info_on_inn(inn=str(message.text))
        base.create_group(group_name=org["suggestions"][0]["value"], inn=str(message.text))
        group_ = base._return_group_info(invite=message.text)
        base.user_registration(
            invite_token=group_.invite_token,
            tg_id=(message.from_user.id),
            username=message.from_user.username
        )
        await message.answer(
            text=f"Ваша организация определна как {org["suggestions"][0]["value"]}\nВведите ваше имя"
        )
        
    else:
        await message.answer(
            text=LEXICON_RU["registration_invite_not_ok"]
        )


# хэндлер на команду хелп
@router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(
        text=LEXICON_RU["/help"]
    )
    logger.info(f'Вызвана команда /help пользоваетелм с TG ID {message.from_user.id}')


# хэндлер для сообщений не подходящих ни под какую категорию
@router.message()
async def other_all_mess(message: Message):
    await message.answer(
        text="Не понимаю."
    )
    logger.info(f'Other command user id - {message.from_user.id}')
