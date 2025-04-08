import logging
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from lexicon.lexicon import LEXICON_RU




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






    

