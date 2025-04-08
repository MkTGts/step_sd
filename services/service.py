import random
#from lexicon.lexicon import LEXICON_RU
import logging
import random
from datetime import datetime


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


def invite_token_generator() -> int:
    '''Функция генерирует инвайт токены для групп.'''
    return int(''.join((str(random.randint(1, 9)) for _ in range(6))))


def now_time():
    '''Функция возвращает дату и время на данный момент'''
    return str(datetime.now())


