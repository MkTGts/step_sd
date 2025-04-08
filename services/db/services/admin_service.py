from .operator_service import OperatorServiceDB
from sqlalchemy.orm import Session
from services.db.models import User
from services.db.decorators import with_session


class AdminServiceDB(OperatorServiceDB):
    @with_session
    def create_group(self,
                         group_name: str,  # название группы 
                         invite_token: int  # токен для приглашения пользователя в группу
                         ):
        '''Создание новое группы'''
        pass


    @with_session
    def create_user(self, 
                    session: Session, 
                    tg_id: int,  # tg id пользователя
                    username: str,  # юзернами пользователя в телеграме
                    fullname: str, group_id: int,  # имя введенное пользователем
                    user_ip: str="None",  # ip пользователя, вводится админом и оператором
                    user_geo: str="None"  # расположение рабочего места пользователя, вводится админом или оператором
                    ) -> list:
        '''Метод создания нового пользователя.
        Добавлен на случай если админу потребуется создать пользователя самому руками'''
        new_user = User(
            tg_id = tg_id,
            username = username,
            fullname = fullname,
            group_id = group_id,
            user_ip = user_ip,
            user_geo = user_geo
        )
        session.add(new_user)


    @with_session    
    def drop_user(self):
        '''Метод удаления пользователя'''
        pass


    @with_session
    def drop_group(self):
        '''Метод удаления группы'''
        pass


    @with_session
    def show_user_list(self):
        '''Метод выводит список всех пользователей'''
        pass


    @with_session
    def show_group_list(self):
        '''Метод выводит список всех групп'''
        pass