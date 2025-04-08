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
