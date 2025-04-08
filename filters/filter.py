from services.db.services.base_service import ServiceDB
from aiogram.filters import BaseFilter
from aiogram.types import Message



base = ServiceDB()


class IsRegistredUserInvite(BaseFilter):
    '''Фильтр проверяющий зарегистрирован ли пользователь и введен ли инвайт.
    Использоваться будет в команде /start (для незарегистрированных пользователей)'''
    def __init__(self):
        self.users_tg_id = base._all_user_tg_id_list()  # список всех тг ид пользователей

    async def __call__(self, message: Message):
        return message.from_user.id not in self.users_tg_id and message.text.isdigit() and len(message.text) == 6


class IsRegistredUserName(BaseFilter):
    '''Фильтр проверяющий зарегистрирован ли пользовател и введено ли имя.
    Будет использоваться после ввода инвайта (для незарегистрированных пользователей)'''
    #def __init__(self):
    #    self.users_tg_id = base._all_user_tg_id_list()  # список всех тг ид пользователей

    async def __call__(self, message: Message):
        return not base._have_fullname(message.from_user.id) and message.text.isalnum() 
