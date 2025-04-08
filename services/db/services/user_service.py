from .base_service import ServiceDB
from services.db.decorators import with_session
from sqlalchemy.orm import Session
from services.db.models import User, Ticket, Group
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



class UserServiceDB(ServiceDB):

    @with_session
    def user_registration(self, 
                          session: Session,
                          invite_token: int,  # пользователь вводит токен для регистрации и по токену распределяется в свою группу
                          tg_id: int,  # tg id пользователя
                          username: str,  # юзернами пользователя в телеграме
                          fullname: str, 
                          user_ip: str|None=None,  # ip пользователя, вводится админом и оператором
                          user_geo: str|None=None  # расположение рабочего места пользователя, вводится админом или оператором
                        ) -> bool:
        '''Метод регистрации нового пользователя.'''
        group_obj = session.query(Group).filter(Group.invite_token==invite_token).first()
        if group_obj is not None:
            new_user = User(
                tg_id = tg_id,
                username = username,
                fullname = fullname,
                group_id = group_obj.group_id
            )
            session.add(new_user)
            logger.info(f"Зарегистрировался пользователь с TG ID {tg_id}. Username: {username}. По инвайту: {invite_token}")
        else:
            logger.warning(f"Попытка зарегистрироваться с несуществущим инвайтом. Данные пользователя: TG ID: {tg_id}, username: {username}")



    @with_session
    def user_ticket_list(self,
                    session: Session,
                    user_id: str  # id пользователя для поиска по таблице тикетов
                    ) -> list:
        '''Метод возвращающий список всех созданных пользователем тикетов в формате списка'''
        return [
            {
                "ticket_id": ticket.ticket_id,
                "status": ticket.status,
                "created": ticket.created_at,
                "message": ticket.message
             }
            for ticket in session.query(Ticket).filter(Ticket.user_id).all()
        ]
