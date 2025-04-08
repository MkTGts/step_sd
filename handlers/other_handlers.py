import logging
from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command
from services.db.services.admin_service import AdminServiceDB
from services.db.services.base_service import ServiceDB
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
base = ServiceDB()

# хэндлер на команду старт
@router.message(Command(commands="start"))
async def process_command_start(message: Message):
    # проверка есть ли пользователь в базе 
    if not base._in_base(message.from_user.id):
        await message.answer(
            text=LEXICON_RU["not_reg"]
        )
        logger.info(f"Прищла команда старт от незарегистрированного пользователя с  TG ID {message.from_user.id}")
    else:
        pass


# хэндлер на команду хелп
@router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(
        text=LEXICON_RU["/help"]
    )
    logger.info(f'Help bot user id - {message.from_user.id}')



# хэндлер для сообщений не подходящих не под какую категорию
@router.message()
async def other_all_mess(message: Message):
    await message.answer(
        text=LEXICON_RU["other"]
    )
    logger.info(f'Other command user id - {message.from_user.id}')