from .user_service import UserServiceDB
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


class OperatorServiceDB(UserServiceDB):
    @with_session
    def show_groups_users(self,
                           session: Session
                           ):
        '''Метод просмотра пользователь состоящих в группе этого оператора.'''
        pass


    @with_session
    def edit_status(self):
        '''Метод изменения статуса тикета'''
        pass


    @with_session
    def drop_ticket(self,
                    session: Session,
                    ticket_id: int
                    ):
        '''Метод удаления тикета'''
        ticket = session.query(Ticket).get(ticket_id)
        if not ticket:
            logger.warning(f"Попытка удалить тикет с несуществующим ID: {ticket_id}")
            return None
        
        session.delete(ticket)
        logger.warning(f"Удален тикет с ID {ticket.ticket_id}")


    @with_session
    def edit_user_ip(self,
                    session: Session,
                    user_id: str, # id пользователя для таблицы users,
                    user_ip: str|None=None
                ):
        '''Метод добавления ip адреса пользователю в таблице users'''

        user = session.query(User).get(user_id)
        if not user:
            logger.error(f"Пользователь с ID  {user_id} не найден.")
            return None
        user.user_ip = user_ip
        logger.info(f"Обновлен IP адресс для пользоватлея с ID {user_id}")


    @with_session
    def edit_user_geo(self,
                    session: Session,
                    user_id: str,  # id пользователя для таблицы users
                    user_geo: str|None=None
                ):
        '''Метод добавлени  расположения рабочего места пользователя в таблице users'''
        
        user = session.query(User).get(user_id)
        if not user:
            logger.error(f"Пользователь с ID  {user_id} не найден.")
            return None
        user.user_geo = user_geo
        logger.info(f"Обновлено расположение рабочего места пользователя с ID {user_id}")

        
