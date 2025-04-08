from sqlalchemy.orm import Session
from services.db.models import Base, User, Group, Ticket
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
    def _return_group_id(self, user_id: int, session: Session) -> int:
        '''Метод возвращающий id группы в которой пользователь состоит'''
        return session.query(User.group_id).filter(User.user_id==user_id).first()[0]
    

    @with_session
    def user_registration(self, 
                          session,
                          invite_token: int,  # пользователь вводит токен для регистрации и по токену распределяется в свою группу
                          tg_id: int,  # tg id пользователя
                          username: str,  # юзернами пользователя в телеграме
                          fullname: str, group_id: int,  # имя введенное пользователем
                          user_type: int = 3,  # тип пользователя, по дефолту обычный пользователь
                          user_ip: str="None",  # ip пользователя, вводится админом и оператором
                          user_geo: str="None"  # расположение рабочего места пользователя, вводится админом или оператором
                        ) -> list:
        '''Метод регистрации нового пользователя.'''
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
    def create_ticket(self, 
                      session: Session,
                      user_id: int,  # id пользователя который создает заявку
                      group_id: int,  #  id группы в которой пользователь состоит
                      operator_id: int,  # id оператора группы
                      message: str,  # текст заявки, подается пользователем
                      status: str = "open",  # изначально статус открыто 
                      closed_at: str|None=None  # дата закрытия заявки. изначаль none
                      ):
        '''Метод создания нового тикета.'''
        new_ticket = Ticket(
            user_id = user_id,
            group_id = group_id,
            operator_id = operator_id,
            message = message,
            status = status,
            created_at = now_time(),
            closed_at=closed_at
        )
        session.add(new_ticket)
        




    



















