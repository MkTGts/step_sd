from services.db.services.base_service import ServiceDB
from aiogram.filters import BaseFilter
from aiogram.types import Message



base = ServiceDB()


class IsRegistredUserInvite(BaseFilter):
    '''Фильтр проверяющий зарегистрирован ли пользователь и введен ли инвайт.
    Использоваться будет в команде /start (для незарегистрированных пользователей)'''
    async def __call__(self, message: Message):
        return (base._check_role(tg_id=message.from_user.id) is None) and message.text.isdigit() and len(message.text) == 6


class IsRegistredUserName(BaseFilter):
    '''Фильтр проверяющий зарегистрирован ли пользовател и введено ли имя.
    Будет использоваться после ввода инвайта (для незарегистрированных пользователей)'''
    async def __call__(self, message: Message):
        return base._check_role(tg_id=message.from_user.id)=="user" and not base._have_fullname(message.from_user.id) and message.text.isalnum() 
    

class CheckRoleAdmin(BaseFilter):
    '''Фильтр проверяющий явлиется ли пользователь администратором'''
    async def __call__(self, message: Message):
        return base._check_role(tg_id=message.from_user.id)=="admin"


class CheckRoleOperator(BaseFilter):
    '''Фильтр проверяющий является пользователь оператором'''
    async def __call__(self, message: Message):
        return base._check_role(tg_id=message.from_user.id)=="operator"
    

class CheckRoleUser(BaseFilter):
    '''Фильтр проверяющий явлиется ли пользователь обычным пользователем'''
    async def __call__(self, message: Message):
        return base._check_role(tg_id=message.from_user.id)=="user"
