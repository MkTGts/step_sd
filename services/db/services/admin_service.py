from .operator_service import OperatorServiceDB
from sqlalchemy.orm import Session, joinedload
from services.db.models import User, Group, Admin, Operator, Ticket
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
    def create_user(self, 
                    session: Session, 
                    tg_id: int,  # tg id пользователя
                    username: str,  # юзернэйм пользователя в телеграме
                    fullname: str,   # имя введенное пользователем
                    group_id: int,
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
    def create_operator(self, 
                    session: Session, 
                    tg_id: int,  # tg id пользователя
                    username: str,  # юзернэйм пользователя в телеграме
                    fullname: str,   # имя введенное пользователем
                    group_id: int,
                    ) -> list:
        '''Метод создания нового пользователя.
        Добавлен на случай если админу потребуется создать пользователя самому руками'''
        new_operator = Operator(
            tg_id = tg_id,
            username = username,
            fullname = fullname,
            group_id = group_id,
        )
        session.add(new_operator)


    @with_session
    def create_admin(self, 
                    session: Session, 
                    tg_id: int,  # tg id пользователя
                    username: str,  # юзернэйм пользователя в телеграме
                    fullname: str,   # имя введенное пользователем
                    ) -> list:
        '''Метод создания нового пользователя.
        Добавлен на случай если админу потребуется создать пользователя самому руками'''
        new_admin = Admin(
            tg_id = tg_id,
            username = username,
            fullname = fullname,
        )
        session.add(new_admin)


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
    def drop_operator(self, operator_id: int, session: Session):
        '''Метод удаления оператора'''
        operator = session.query(Operator).get(operator_id)
        if not operator:
            logger.warning(f"Попытка удалить группу с несуществующим ID: {operator_id}")
            return None
        
        session.delete(operator)
        logger.warning(f"Удален оператор c ID {operator_id}")



    @with_session
    def show_ticket_list_for_admin(self, session: Session, group_id: int):
        '''Методы воводящий список тикетов по group_id'''
        try:
            users = session.query(User)
            operators = session.query(Operator)
            
            return [
                {
                "ticket_id": ticket.ticket_id,
                "ticket_status": ticket.status,
                "user_name": users.get(ticket.user_id).fullname,
                "user_tg": f"@{users.get(ticket.user_id).username}",
                "operator_name": operators.get(ticket.operator_id).fullname,
                "operator_tg": f"@{operators.get(ticket.operator_id).username}",
                "ticket_create_date": ticket.created_at,
                "ticket_message": ticket.message
                }
                for ticket in session.query(Ticket).filter(Ticket.group_id==group_id).all()
            ]
        except Exception as err:
            logger.critical(f"Ошибка в show_tickets. {err}")
            

    @with_session
    def show_group_list(self, session: Session):
        '''Метод выводит список всех групп'''
        return [{"group_id": group.group_id,
                 "group_name": group.group_name,
                 "invite_token": group.invite_token} 
                for group in session.query(Group).all()]