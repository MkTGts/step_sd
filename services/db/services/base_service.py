from sqlalchemy.orm import Session
from services.db.models import Base, User, Group, Ticket, Operator, Admin
from services.db.decorators import with_session
from services.service import now_time
import functools
import logging
import requests
from data.config import Config, load_config


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


config: Config = load_config()


class ServiceDB:
    '''Класс с методами для работы с базой данных, достпными дял всех пользователей.'''    

    @with_session
    def _return_user_info(self, session: Session, tg_id: int):
        '''Метод возвращающий информацию о пользователе как объект'''
        return session.query(User).filter(User.tg_id==tg_id).first()

    
    @with_session
    def _return_operator_info(self, session: Session, group_id: int):
        '''Метод возвращающий информацию об операторе как объект'''
        return session.query(Operator).filter(Operator.group_id==group_id).first()


    @with_session
    def _return_admins_id_list(self, session: Session):
        '''Метод возращает список tg идишнокв админов'''
        return session.query(Admin.tg_id).all()
    

    @with_session
    def _return_group_info(self, session: Session, group_id: int|None=None, invite: str|int|None=None):
        if group_id:
            return session.query(Group).filter(Group.group_id==group_id).first()
        elif invite:
            return session.query(Group).filter(Group.invite_token==invite).first()
    

    def _return_info_on_inn(self, inn: str|int):
        response = requests.post(
            url="http://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party",
            headers={"Authorization": config.tg_bot.token_inn},
            json={"query": str(inn)}
        )
        return response.json()
        #return response.json()["suggestions"][0]["value"]


    @with_session
    def _in_invite(self, invite_token: int, session: Session):
        '''Метод проверяющий есть ли такой инавайт'''
        return session.query(Group.invite_token).filter(Group.invite_token==invite_token).first()

    
    @with_session
    def _set_fullname(self, session: Session, tg_id: int, fullname: str):
        '''Устанавливает полное имя пользователя, им же введенное'''
        user = session.query(User).filter(User.tg_id==tg_id).first()
        user.fullname = fullname
    

    @with_session
    def _have_fullname(self, session: Session, tg_id: int):
        '''Метод проверяет записано ли полное имя пользователя в базе'''
        return session.query(User).filter(User.tg_id==tg_id).first().fullname
        
  
    @with_session
    def _return_group_id(self, user_id: int, session: Session) -> int:
        '''Метод возвращающий id группы в которой пользователь состоит'''
        return session.query(User.group_id).filter(User.user_id==user_id).first()[0]
    

    @with_session
    def _return_group_list(self, session: Session) -> list:
        '''Метод возвращающий список всех групп'''
        return session.query(Group).all()
    

    @with_session
    def _return_user_id(self, tg_id: int, session: Session) -> int:
        '''Метод возвращающий ID пользователя по TG ID'''
        return session.query(User).filter(User.tg_id==tg_id).first().user_id
    

    @with_session
    def _return_group_operator(self, session: Session, group_id: int) -> int:
        '''Метод возвращающий id оператора группы по id группы'''
        return session.query(Operator).filter(Operator.group_id==group_id).first().operator_id
    

    @with_session
    def _check_role(self, session: Session, tg_id: int):
        '''Метод определяющий роль пользователя по тг ид'''
        try:
            # Проверяем от высшей роли к низшей
            if session.query(Admin).filter(Admin.tg_id == tg_id).first():
                logger.debug(f"Найден администратор с tg_id={tg_id}")
                return "admin"
            
            if session.query(Operator).filter(Operator.tg_id == tg_id).first():
                logger.debug(f"Найден оператор с tg_id={tg_id}")
                return "operator"
            
            if session.query(User).filter(User.tg_id == tg_id).first():
                logger.debug(f"Найден пользователь с tg_id={tg_id}")
                return "user"
            
            logger.warning(f"Пользователь с tg_id={tg_id} не найден")
            return None
            
        except Exception as e:
            logger.error(f"Ошибка определения роли для tg_id={tg_id}: {str(e)}")
            raise 


    @with_session
    def create_group(self,
                        session: Session,
                        group_name: str,  # название группы 
                        inn: None
                    ):
        '''Метод создания новой группы'''
        try:
            new_group = Group(
                group_name=group_name,
                invite_token=inn,
            )
            session.add(new_group)
            logger.info(f"Группа {new_group.group_name} создана")
        except Exception as err:
            logger.warning(f'Во время создания группы возникла ошибка {err}')
    

    @with_session
    def user_registration(self, 
                          session: Session,
                          invite_token: int,  # пользователь вводит токен для регистрации и по токену распределяется в свою группу
                          tg_id: int,  # tg id пользователя
                          username: str,  # юзернами пользователя в телеграме
                          fullname: str|None=None, 
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
    def create_ticket(self, 
                      session: Session,
                      user_id: int,  # id пользователя который создает заявку
                      message: str,  # текст заявки, подается пользователем
                      status: str = "Открыт",  # изначально статус открыто 
                      closed_at: str|None=None,  # дата закрытия заявки. изначаль none
                      group_id: int|None = None,  #  id группы в которой пользователь состоит
                      ):
        '''Метод создания нового тикета.'''
        group_id = session.query(User).get(user_id).group_id
        try:
            operator_id = session.query(Operator).filter(Operator.group_id == group_id).first().operator_id
        except:
            operator_id = None

        new_ticket = Ticket(
            user_id = user_id,
            group_id = group_id,
            operator_id = operator_id,  #session.query(Operator).filter(Operator.group_id == group_id).first().operator_id,  #operator_id,
            message = message,
            status = status,
            created_at = now_time(),
            closed_at=closed_at
        )
        session.add(new_ticket)
        




    



















