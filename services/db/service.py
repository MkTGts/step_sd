from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Group
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


engine = create_engine("sqlite:///data/db/app.db", echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)



class ServiceDB:
    '''Класс с методами для работы с базой данных, достпными дял всех пользователей.'''

    # декоратор для начала, закртыия сессии и принятия изменений в ней
    def with_session(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            with Session() as session:
                try:
                    if 'session' in func.__code__.co_varnames:
                        kwargs['session'] = session 

                    logger.info("Сессия запущена.")
                    res = func(self, *args, **kwargs)

                    if res is None:
                        session.commit()
                    logger.info("Сессия успешно завершилась.")
                    return res
                except Exception as err:
                    session.rollback()
                    logger.error(f"Во время сесси возникла ошибка {err}.")
        return wrapper
    

    @with_session
    def _return_group_id(self, user_id: int, session) -> int:
        '''Метод возвращающий id группы в которой пользователь состоит'''
        return session.query(User.group_id).filter(User.user_id==user_id).first()[0]
    

    @with_session
    def user_registration(self, 
                          session,
                          invite_token: int,  # пользователь вводит токен для регистрации и по токену распределяется в свою группу
                          tg_id: int,  # tg id пользователя
                          username: str,  # юзернами пользователя в телеграме
                          fullname: str, group_id: int,  # имя введенное пользователем
                          user_ip: str="None",  # ip пользователя, вводится админом и оператором
                          user_geo: str="None"  # расположение рабочего места пользователя, вводится админом или оператором
                        ) -> list:
        '''Метод регистрации нового пользователя.'''
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
    def create_ticket(self, 
                      user_id: int,  # id пользователя который создает заявку
                      group_id: int,  #  id группы в которой пользователь состоит
                      operator_id: int,  # id оператора группы
                      message: str,  # текст заявки, подается пользователем
                      created_at: str,  # дата созданяи заявки
                      closed_ar: str|None=None  # дата закрытия заявки. изначаль none
                      ):
        '''Метод создания нового тикета.'''
        pass


class UserServiceDB(ServiceDB):
    @ServiceDB.with_session
    def ticket_list(self,
                    user_id: str  # id пользователя для поиска по таблице тикетов
                    ) -> list:
        '''Метод возвращает список всех созданных пользователем тикетов в формате списка'''
        pass



class OperatorServiceDB(UserServiceDB):
    @ServiceDB.with_session
    def edit_status(self):
        '''Метод изменения статуса тикета'''
        pass


    @ServiceDB.with_session
    def drop_ticket(self):
        '''Метод удаления тикета'''
        pass


    @ServiceDB.with_session
    def add_user_ip(self,
                    user_id: str  # id пользователя для таблицы users
                      ):
        '''Метод добавления ip адреса пользователю в таблице users'''
        pass


    @ServiceDB.with_session
    def add_user_geo(self,
                     user_id: str  # id пользователя для таблицы users
                     ):
        '''Метод добавлени  расположения рабочего места пользователя в таблице users'''
        pass
        


class AdminServiceDB(OperatorServiceDB):
    @ServiceDB.with_session
    def create_group(self,
                         group_name: str,  # название группы 
                         invite_token: int  # токен для приглашения пользователя в группу
                         ):
        '''Создание новое группы'''
        pass


    @ServiceDB.with_session
    def create_user(self, 
                    session: Session, # type: ignore
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


    @ServiceDB.with_session    
    def drop_user(self):
        '''Метод удаления пользователя'''
        pass


    @ServiceDB.with_session
    def drop_group(self):
        '''Метод удаления группы'''
        pass


    @ServiceDB.with_session
    def show_user_list(self):
        '''Метод выводит список всех пользователей'''
        pass


    @ServiceDB.with_session
    def show_group_list(self):
        '''Метод выводит список всех групп'''
        pass

    


#admin = AdminServiceDB()

#admin.create_user(tg_id=23, username="qstepashka", fullname="qstepan", group_id=1)
#print(admin._return_group_id(user_id=2))


















