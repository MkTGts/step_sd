from .user_service import UserServiceDB
from services.db.decorators import with_session
from sqlalchemy.orm import Session
from services.db.models import User, Ticket, Group, Operator
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
                           session: Session,
                           tg_id: int|None = None,
                           group_id: int|None = None
                           ) -> list[dict]:
        '''Метод просмотра пользователей состоящих в группе. Поиск или по группе или по оператору.
        В приорите поиск по оператору и если подан на вход id оператора, то поиск будет по оператору в любом случае'''
        if tg_id:
            group_id = session.query(Operator).filter(Operator.tg_id==tg_id).first().group_id
            
        return [{
                "user_id": user.user_id,
                "username": user.username,
                "fullname": user.fullname,
                "user_ip": user.user_ip,
                "user_geo": user.user_geo
        }
            for user in session.query(User).filter(User.group_id == group_id).all()
        ]
    

    @with_session
    def show_ticket_list_for_operator(self, session: Session, tg_id: int):
        '''Методы воводящий список тикетов по tg_id оператора'''
        try:
            users = session.query(User)
            operators = session.query(Operator)
            operator_id = operators.filter(Operator.tg_id==tg_id).first().operator_id
            tickets = session.query(Ticket).filter(Ticket.operator_id==operator_id).all()

            return [
                {
                "ticket_id": ticket.ticket_id,
                "ticket_status": ticket.status,
                "user_name": users.get(ticket.user_id).fullname,
                "user_tg": f"@{users.get(ticket.user_id).username}",
                "ticket_create_date": ticket.created_at,
                "ticket_message": ticket.message
                }
                for ticket in tickets
            ]
        except Exception as err:
            logger.critical(f"Ошибка в show_tickets. {err}")

        


    @with_session
    def show_user_list_by_group_id(self, session: Session, groupd_id: int):
        '''Метод выводит список всех пользователей'''
        return [{"user_id": user.user_id,
                 "tg_id": user.tg_id,
                 "username": user.username,
                 "fullname": user.fullname,
                 "user_ip": user.user_ip,
                 "user_geo": user.user_geo} 
                for user in session.query(User).filter(User.group_id==groupd_id).all()]
    


    @with_session
    def edit_status(self,
                    session: Session,
                    ticket_id: int,
                    status: str
                ):
        '''Метод изменения статуса тикета'''
        ticket = session.query(Ticket).get(ticket_id)
        if not ticket:
            logger.error(f"Тикет с ID  {ticket_id} не найден.")
            return None
        ticket.status = status
        logger.info(f"Обновлен статус тикета с ID {ticket_id}")


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


    @with_session
    def show_operators_list(self, session: Session):
        '''Метод возвращающий список операторов'''
        return [
            {
                "operator_id": operator.operator_id,
                "username": f'@{operator.username}',
                "tg_id": operator.tg_id,
                "fullname":operator.fullname,
                "group": session.query(Group).filter(Operator.operator_id==operator.operator_id).first().group_name,
            }
            for operator in session.query(Operator).all()
        ]

        
