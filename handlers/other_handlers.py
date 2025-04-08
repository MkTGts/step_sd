import logging
from aiogram import Router, F
from aiogram.types import Message
from handlers.base import base
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command
from filters.filter import IsRegistredUserInvite, IsRegistredUserName
from services.db.services.admin_service import AdminServiceDB
from services.db.services.operator_service import OperatorServiceDB
from services.db.services.user_service import UserServiceDB


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
    if not base._in_base(message.from_user.id):
        await message.answer(
            text=LEXICON_RU["not_reg"]
        )
        logger.info(f"Пришла команда старт от незарегистрированного пользователя с  TG ID {message.from_user.id}")
    else:
        await message.answer(
            text="Авторизация пройдена"
        )


# хэндлер на команду хелп
@router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(
        text=LEXICON_RU["/help"]
    )
    logger.info(f'Вызвана команда /help пользоваетелм с TG ID {message.from_user.id}')


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
    else:
        await message.answer(
            text=LEXICON_RU["registration_invite_not_ok"]
        )


@router.message(IsRegistredUserName())
async def process_registration_user_name(message: Message):
    base._set_fullname(tg_id=int(message.from_user.id), fullname=message.text)
    await message.answer(
        text=f"Имя {message.text} принято"
    )


# хэндлер для сообщений не подходящих ни под какую категорию
@router.message()
async def other_all_mess(message: Message):
    await message.answer(
        text=LEXICON_RU["other"]
    )
    logger.info(f'Other command user id - {message.from_user.id}')
