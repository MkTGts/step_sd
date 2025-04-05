import logging
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.kyboards import main_kb
from lexicon.lexicon import LEXICON_RU
from services.services import pars_wb
from services.db_services import create_db, verification_user, insert_datas, set_pars_mode, verification_mode, set_wb_id



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


router = Router()  # инициализация роутера


# хэндрел на команду старт
@router.message(Command(commands="start"))
async def process_command_start(message: Message):
    pass


# хэндлер на команду хелп
@router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(
        text=LEXICON_RU["/help"],
        reply_markup=main_kb
    )
    logger.info(f'Help bot user id - {message.from_user.id}')
    

