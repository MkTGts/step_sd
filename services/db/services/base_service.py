from sqlalchemy.orm import Session
from services.db.models import Base, User, Group, Ticket, Operator
from services.db.decorators import with_session
from services.service import now_time
import functools
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


class ServiceDB:
    '''Класс с методами для работы с базой данных, достпными дял всех пользователей.'''

    @with_session
    def _in_base(self, tg_id: int, session: Session):
        '''Метод проверяющий есть ли пользователь в базе'''
        return session.query(User.user_id).filter(User.tg_id==tg_id).first()
        
  
    @with_session
    def _return_group_id(self, user_id: int, session: Session) -> int:
        '''Метод возвращающий id группы в которой пользователь состоит'''
        return session.query(User.group_id).filter(User.user_id==user_id).first()[0]


    @with_session
    def create_ticket(self, 
                      session: Session,
                      user_id: int,  # id пользователя который создает заявку
                      
                      #operator_id: int,  # id оператора группы
                      message: str,  # текст заявки, подается пользователем
                      status: str = "open",  # изначально статус открыто 
                      closed_at: str|None=None,  # дата закрытия заявки. изначаль none
                      group_id: int|None = None,  #  id группы в которой пользователь состоит
                      ):
        '''Метод создания нового тикета.'''
        group_id = session.query(User).get(user_id).group_id

        new_ticket = Ticket(
            user_id = user_id,
            group_id = group_id,
            operator_id = session.query(Operator).filter(Group.group_id == group_id).first().operator_id,  #operator_id,
            message = message,
            status = status,
            created_at = now_time(),
            closed_at=closed_at
        )
        session.add(new_ticket)
        




    



















