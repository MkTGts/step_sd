from .operator_service import OperatorServiceDB
from sqlalchemy.orm import Session
from services.db.models import User, Group
from services.db.decorators import with_session
from services.service import invite_token_generator
import logging



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


class AdminServiceDB(OperatorServiceDB):
    @with_session
    def create_group(self,
                        session: Session,
                        group_name: str,  # название группы 
                    ):
        '''Метод создания новой группы'''
        new_group = Group(
            group_name=group_name,
            invite_token=invite_token_generator()
        )
        session.add(new_group)



    @with_session
    def create_user(self, 
                    session: Session, 
                    tg_id: int,  # tg id пользователя
                    username: str,  # юзернэйм пользователя в телеграме
                    fullname: str,   # имя введенное пользователем
                    group_id: int,
                    user_type: int = 3,  
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
            user_type = user_type,
            user_ip = user_ip,
            user_geo = user_geo
        )
        session.add(new_user)


    @with_session    
    def drop_user(self, user_id: int, session: Session):
        '''Метод удаления пользователя'''
        user = session.query(User).get(user_id)
        if not user:
            logger.warning(f"Попытка удалить пользователя с несуществующим ID  {user_id}")
            return None
        
        session.delete(user)
        logger.warning(f"Удален пользователь с TGID {user.tg_id}, Username: {user.fullname}")


    @with_session
    def drop_group(self, group_id: int, session: Session):
        '''Метод удаления группы'''
        group = session.query(Group).get(group_id)
        if not group:
            logger.warning(f"Попытка удалить группу с несуществующим ID: {group_id}")
            return None
        
        session.delete(group)
        logger.warning(f"Удален удалена группа с ID {group.group_id}, Groupname: {group.group_name}")


    @with_session
    def show_user_list(self, session: Session):
        '''Метод выводит список всех пользователей'''
        return [{"user_id": user.user_id,
                 "tg_id": user.tg_id,
                 "username": user.username,
                 "fullname": user.fullname,
                 "user_type": user.user_type,
                 "group_name": session.query(Group).get(user.group_id).group_name,
                 "user_ip": user.user_ip,
                 "user_geo": user.user_geo} 
                for user in session.query(User).all()]
        


    @with_session
    def show_group_list(self, session: Session):
        '''Метод выводит список всех групп'''
        return [{"group_id": group.group_id,
                 "group_name": group.group_name,
                 "invite_token": group.invite_token} 
                for group in session.query(Group).all()]