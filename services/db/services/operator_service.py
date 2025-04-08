from .user_service import UserServiceDB
from services.db.decorators import with_session
from sqlalchemy.orm import Session


class OperatorServiceDB(UserServiceDB):
    @with_session
    def edit_status(self):
        '''Метод изменения статуса тикета'''
        pass


    @with_session
    def drop_ticket(self):
        '''Метод удаления тикета'''
        pass


    @with_session
    def add_user_ip(self,
                    user_id: str  # id пользователя для таблицы users
                      ):
        '''Метод добавления ip адреса пользователю в таблице users'''
        pass


    @with_session
    def add_user_geo(self,
                     user_id: str  # id пользователя для таблицы users
                     ):
        '''Метод добавлени  расположения рабочего места пользователя в таблице users'''
        pass
        
