from .base_service import ServiceDB
from services.db.decorators import with_session
from sqlalchemy.orm import Session

class UserServiceDB(ServiceDB):
    @with_session
    def ticket_list(self,
                    user_id: str  # id пользователя для поиска по таблице тикетов
                    ) -> list:
        '''Метод возвращает список всех созданных пользователем тикетов в формате списка'''
        pass
