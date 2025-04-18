from aiogram.utils.markdown import hlink


LEXICON_RU: dict[str, str] = {
    "/start": 'Привет.',
    "/help": "Еще заполняется",
    "not_reg": f"Вы не зарегистрированы.\nПродалжая, вы принимаете {hlink('условия обработки персональных данных', 'https://www.consultant.ru/document/cons_doc_LAW_61801/315f051396c88f1e4f827ba3f2ae313d999a1873/')}\n",
    "other": "Other",
    "registration_invite_ok": "Запущен процесс регистрации.\nВведите ваше имя.",
    "registration_invite_not_ok": "Неверный инвайт. По ИНН компания не определна.",
    
}

LEXCON_TICKETS_STATUS: dict[str, str] = {
    "open": "Открыт",
    "in_work": "В работе",
    "closed": "Закрыт"
}


LEXCON_USER_KEYBOARDS: dict[str, str] = {
    "tickets_list": "Список моих тикетов",
    "create_ticket": "Создать тикет"
}


LEXCON_USER_HANDLERS: dict[str, str] = {
    "is_tickets_none": "У вас нет тикетов",
    "created_ticket": "Тикет создан",
    "select_creat_ticket": "Введите текст тикета"
}


LEXCON_ADMIN_KEYBOARDS: dict[str, str] = {
    "users": "Пользователи",
    "tickets": "Тикеты",
    "operators": "Операторы",
    "groups": "Организации",
    "show_users": "Список пользователей",
    "create_user": "Добавить пользователя",
    "drop_user": "Удалить пользователя",
    "show_operators": "Все операторы",
    "create_operator": "Добавить оператора",
    "drop_operator": "Удалить оператора",
    "show_groups": "Все организации",
    "create_group": "Добавить организацию",
    "drop_group": "Удалить организацию",
    "show_invite_group": "Список организаций с ИНН",
    "show_tickets": "Все тикеты",
    "create_tickets": "Создать тикет",
    "edit_tickets": "Изменить статус тикета",
    "drop_tickets":"Удалить тикет",
    "back_to_main_menu": "<< В основное меню"
    
}

LEXCON_ADMIN_HANDLERS: dict[str, str] = {
    "start": "Старт администратора"
}


LEXICON_OPERATOR_KEYBOARDS: dict[str, str] = {
    "back_to_main_menu": "<< В основное меню",
    "users": "Пользователи",
    "show_tickets": "Список тикетов",
    "edit_status": "Изменить статус тикета"
}

LEXICON_OPERATOR_HANDLERS: dict[str, str] = {
    "users_is_none": "Похоже, что пользователей пока нет"
}



 

LEXICON_COMMANDS_RU: dict[str, str] = {
    "/start": "Команда запуска бота",
    "/help": "Команда вызова справки по работе бота"
}