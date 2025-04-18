import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from services.db.services.admin_service import AdminServiceDB
from keyboards.kyboards_admins import admin_submenu_users_kb, admin_main_inline_kb, admin_submenu_operators_kb, admin_submenu_groups_kb, admin_submenu_tickets_kb, but_admin_back_to_main_menu
from keyboards.kyboards_users import user_inline_kb
from keyboards.kyboards_operators import operator_main_inline_kb
from keyboards.set_menu import ticket_status_inline_kb
from filters.filter import CheckRoleAdmin
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXCON_TICKETS_STATUS




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



admin = AdminServiceDB()
router = Router()


# класс для хранения состояния создания группы
class GroupCreation(StatesGroup):
    waiting_for_group_name = State()




@router.callback_query(F.data.in_("back_to_main_menu"))
async def process_admin_back_to_main_menu(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Основное меню</b>",
        reply_markup=admin_main_inline_kb
    )
    await callback.answer()


########################################################################################################

@router.callback_query(F.data.in_("admin_users"))
async def process_admin_submenu_users(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Пользователи</b>",
        reply_markup=admin_submenu_users_kb
    )
    await callback.answer()


###################
# при нажатии кнопки Все пользователи, запрашивается список организаций, по которым будет вывод пользователей
@router.callback_query(F.data.in_("admin_show_users"))
async def process_admin_submenu_users(callback: CallbackQuery):
    group_list = {group.group_id: group.group_name for group in admin._return_group_list()}
    await callback.message.answer(
        text="<b>Выберите организацию</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=group, callback_data=f"group_for_admin{str(id_)}")]
                             for id_, group in group_list.items()] + [[but_admin_back_to_main_menu]])
        )
    await callback.answer()


# при выборе функции список пользователей, выводит клавиатуру с оранизациями для отбора по нужной
#@router.callback_query(F.data.in_([f"group_for_admin{str(id_)}" for id_ in range(1, 10)]))
@router.callback_query(F.data.regexp(r"group_for_admin\d+$"))
async def process_admin_submenu_users_select_group(callback: CallbackQuery):
    group_id = callback.data[-1]

    await callback.message.answer(
        text="<b>Список пользователей:</b>\n" +
        "\n\n".join([
            f"<b>ID пользователя</b>: {user['user_id']}\n<b>TG ID</b>: {user['tg_id']}\n<b>Username</b>: {f"@{user['username']}"}\n<b>Полное имя</b>: {user['fullname']}\n<b>IP пользователя</b>: {user['user_ip']}\n<b>Расположение рабочего места пользователя</b>: {user['user_geo']}"
            for user in admin.show_user_list_by_group_id(groupd_id=group_id)
        ]),
        reply_markup=admin_main_inline_kb
    )
    #await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
##################################


# при нажатии кнопки удалить пользователz, запрашивается список организаций, по которым будет вывод пользователей и далее выбор кого удалить
@router.callback_query(F.data.in_("admin_drop_user"))
async def process_admin_submenu_drop_user_groups_list(callback: CallbackQuery):
    group_list = {group.group_id: group.group_name for group in admin._return_group_list()}
    await callback.message.answer(
        text="<b>Выберите организацию</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=group, callback_data=f"group_for_admin_drop_user{str(id_)}")]
                             for id_, group in group_list.items()] + [[but_admin_back_to_main_menu]])
        )
    await callback.answer()


# при выборе функции удалить пользователя, выбрана организация, выводится список пользователей для удаления
#@router.callback_query(F.data.in_([f"group_for_admin_drop_user{str(id_)}" for id_ in range(1, 10)]))
@router.callback_query(F.data.regexp(r"group_for_admin_drop_user\d+$"))
async def process_admin_submenu_users_select_group(callback: CallbackQuery):
    group_id = callback.data[-1]
    users = admin.show_groups_users(group_id=group_id)
    
    await callback.message.answer(
        text="<b>Выберите пользователя для удаления</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text=user['fullname'],
                callback_data=f"user_for_drop_{user["user_id"]}"
            )] for user in users
        ] + [[but_admin_back_to_main_menu]])
    )
   
    await callback.answer()


# удалние, выбранного через инлайн кнопку, пользователя
#@router.callback_query(F.data.in_([f"user_for_drop_{str(id_)}" for id_ in range(0, 100)]))
@router.callback_query(F.data.regexp(r"user_for_drop_\d+$"))
async def process_admin_submenu_users_select_group_drop_user(callback: CallbackQuery):
    user_id: int = int(''.join([s for s in callback.data if s.isdigit()]))
    admin.drop_user(user_id=user_id)
    await callback.message.answer(
        text=f"<b>Пользователь с ID {user_id} удален.</b>"
    )
    await callback.answer()



#################################################################################################
# отбирает пользователей по выбранной в прошлом апдейте-хэндлере организации
@router.callback_query(F.data.in_("admin_operators"))
async def process_admin_submenu_users(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Операторы</b>",
        reply_markup=admin_submenu_operators_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("admin_show_operators"))
async def process_admin_submenu_operators_show(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Список операторов:</b>\n" +
        "\n\n".join([
            f"<b>ID оператора</b>: {operator['operator_id']}\n<b>TG ID</b>: {operator['tg_id']}\n<b>Username</b>: {f"{operator['username']}"}\n<b>Полное имя</b>: {operator['fullname']}\n<b>Организация оператора</b>: {operator['group']}"
            for operator in admin.show_operators_list()
        ]),
        reply_markup=admin_main_inline_kb
    )
    #await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()



@router.callback_query(F.data.in_("admin_drop_operator"))
async def process_admin_submenu_operator_select_operator(callback: CallbackQuery):
    operator_dict = {operator["operator_id"]: operator["fullname"] for operator in admin.show_operators_list()}
    
    await callback.message.answer(
        text="<b>Выберите оператора для удаления</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text=name,
                callback_data=f"operator_for_admin_drop_operator{id_}"
            )] for id_, name in operator_dict.items()
        ] + [[but_admin_back_to_main_menu]])
    )
   
    await callback.answer()
    


#@router.callback_query(F.data.in_([f"operator_for_admin_drop_operator{str(id_)}" for id_ in range(0, 100)]))
@router.callback_query(F.data.regexp(r"operator_for_admin_drop_operator\d+$"))
async def process_admin_submenu_operator_select_operator_drop_operator(callback: CallbackQuery):
    operator_id: int = int(''.join([s for s in callback.data if s.isdigit()]))
    admin.drop_operator(operator_id=operator_id)
    await callback.message.answer(
        text=f"<b>Оператор с ID {operator_id} удален.</b>"
    )
    await callback.answer()




######################################################################################################


@router.callback_query(F.data.in_("admin_groups"))
async def process_admin_submenu_users(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Организации</b>",
        reply_markup=admin_submenu_groups_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("admin_show_invite_group"))
async def process_admin_submenu_groups_show_invites(callback: CallbackQuery):
    groups = admin.show_group_list()
    await callback.message.answer(
        text="<b>Список организаций:</b>\n" +
        "\n\n".join(
            f"Организация: {group["group_name"]}\nИнвайт: {group["invite_token"]}"
            for group in groups
        ),
        reply_markup=admin_main_inline_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("admin_create_group"))
async def process_admin_submenu_groups_create_group(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите название организации и ее ИНН через запятую"
    )
    await state.set_state(GroupCreation.waiting_for_group_name)
    await callback.answer()


@router.message(GroupCreation.waiting_for_group_name)
async def process_admin_submenu_groups_create_group_create(message: Message, state: FSMContext):
    data = message.text.split(",")
    try:
        admin.create_group(group_name=data[0].strip(), inn=int(data[1].strip()))
        await message.answer(
            text=f"Создана группа {data[0]}",
            reply_markup=admin_main_inline_kb
        )
    except:
        await message.answer(
            text="Ошибка при создании группы. Данные введены некорректно.",
            reply_markup=admin_main_inline_kb
        )
    await state.clear()


# при выборе функции удалить организацию, выбираетс организация для удаления
@router.callback_query(F.data.in_("admin_drop_group"))
async def process_admin_submenu_group_select_group(callback: CallbackQuery):
    group_list = {group.group_id: group.group_name for group in admin._return_group_list()}
    
    await callback.message.answer(
        text="<b>Выберите организация для удаления</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text=name,
                callback_data=f"group_for_admin_drop_group{id_}"
            )] for id_, name in group_list.items()
        ] + [[but_admin_back_to_main_menu]])
    )
   
    await callback.answer()
    

# удалние, выбранной через инлайн кнопку, группы
#@router.callback_query(F.data.in_([f"group_for_admin_drop_group{str(id_)}" for id_ in range(0, 100)]))
@router.callback_query(F.data.regexp(r"group_for_admin_drop_group\d+$"))
async def process_admin_submenu_group_select_group_drop_group(callback: CallbackQuery):
    group_id: int = int(''.join([s for s in callback.data if s.isdigit()]))
    admin.drop_group(group_id=group_id)
    await callback.message.answer(
        text=f"<b>Оганизация с ID {group_id} удалена.</b>"
    )
    await callback.answer()


########################################################################################################################################

@router.callback_query(F.data.in_("admin_tickets"))
async def process_admin_submenu_tickets(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Тикеты</b>",
        reply_markup=admin_submenu_tickets_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("admin_show_tickets"))
async def process_admin_submenu_tickets_show_tickets(callback: CallbackQuery):
    group_list = {group.group_id: group.group_name for group in admin._return_group_list()}
    await callback.message.answer(
        text="<b>Выберите организацию</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=group, callback_data=f"group_for_admin_ticket{str(id_)}")]
                             for id_, group in group_list.items()] + [[but_admin_back_to_main_menu]])
        )
    await callback.answer()


# при выборе функции список тикетов, выводит клавиатуру с оранизациями для отбора по нужной
#@router.callback_query(F.data.in_([f"group_for_admin_ticket{str(id_)}" for id_ in range(1, 10)]))
@router.callback_query(F.data.regexp(r"group_for_admin_ticket\d+$"))
async def process_admin_submenu_ticket_select_group(callback: CallbackQuery):
    group_id = callback.data[-1]
    try:
        await callback.message.answer(
            text="<b>Список тикетов:</b>\n" +
            "\n\n".join([
                f"<b>ID тикета</b>: {ticket['ticket_id']}\n<b>Статус тикета</b>: {ticket['ticket_status']}\n<b>Дата создания</b>: {ticket['ticket_create_date']}\n<b>Имя пользователя</b>: {ticket['user_name']}\n<b>ТГ пользователя</b>: {ticket['user_tg']}\n<b>Имя оператора</b>: {ticket['operator_name']}\n<b>ТГ оператора</b>: {ticket['operator_tg']}\n<b>Сообщение</b>: {ticket['ticket_message']}"
                for ticket in admin.show_ticket_list_for_admin(group_id=group_id)
            ]),
            reply_markup=admin_main_inline_kb
        )
    except Exception as err:
        logger.critical(f'Ошикбка {err}; group_id={group_id}; data={admin.show_ticket_list_for_admin(groupd_id=group_id)}')
        await callback.message.answer(
            text="Похоже что тикетов нет..."
        )
    await callback.answer()


@router.callback_query(F.data.in_("admin_edit_tickets"))
async def process_admin_submenu_tickets_edit_tickets(callback: CallbackQuery):
    group_list = {group.group_id: group.group_name for group in admin._return_group_list()}
    await callback.message.answer(
        text="<b>Выберите организацию</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="По ID", callback_data="group_for_admin_edit_ticket_by_id")]] +
                [[InlineKeyboardButton(text=group, callback_data=f"group_for_admin_edit_ticket{str(id_)}")]
                             for id_, group in group_list.items()] + [[but_admin_back_to_main_menu]])
        )
    await callback.answer()



class SelectTicketByID(StatesGroup):
    waiting_for_group_id = State()


@router.callback_query(F.data.in_("group_for_admin_edit_ticket_by_id"))
async def process_admin_submenu_tickets_edit_tickets_by_id(callback: CallbackQuery, state:FSMContext):
    await callback.message.answer(
        text="Введите ID тикета"
    )
    await state.set_state(SelectTicketByID.waiting_for_group_id)
    await callback.answer()


@router.message(SelectTicketByID.waiting_for_group_id)
async def process_admin_submenu_groups_create_group_create(message: Message, state: FSMContext):
    if isinstance(message.text, int):
        ticket_id = int(message.text)

    await message.answer(
        text="<b>Выберите новый статус для тикета</b>",
        reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                        [InlineKeyboardButton(
                                text="Открыта",
                                callback_data=f"open:{ticket_id}"
                    )], 
                        [InlineKeyboardButton(
                                text="В работе",
                                callback_data=f"in_work:{ticket_id}"
                    )], 
                        [InlineKeyboardButton(
                                text="Закрыта",
                                callback_data=f"closed:{ticket_id}"
                    )]
    ])
        )
    await state.clear()



#@router.callback_query(F.data.in_([f"group_for_admin_edit_ticket{str(id_)}" for id_ in range(1, 10)]))
@router.callback_query(F.data.regexp(r"group_for_admin_edit_ticket\d+$"))
async def process_admin_submenu_tickets_edit_tickets_select_group(callback: CallbackQuery):
    group_id = callback.data[-1]
    ticket_dict = {tic["ticket_id"]: f"{tic["ticket_message"][:45]}..." for tic in admin.show_ticket_list_for_admin(group_id=group_id)}
    await callback.message.answer(
        text="<b>Выберите тикет</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=ticket, callback_data=f"group_for_admin_edit_ticket_select_group_select_ticket{str(id_)}")]
                             for id_, ticket in ticket_dict.items()] + [[but_admin_back_to_main_menu]])
        )
    await callback.answer()


#@router.callback_query(F.data.in_([f"group_for_admin_edit_ticket_select_group_select_ticket{str(id_)}" for id_ in range(1, 100)]))
@router.callback_query(F.data.regexp(r"group_for_admin_edit_ticket_select_group_select_ticket\d+$"))
async def process_admin_submenu_tickets_edit_tickets_select_group_select_ticket(callback: CallbackQuery):
    ticket_id = callback.data[-1]
    await callback.message.answer(
        text="<b>Выберите новый статус для тикета</b>",
        reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                        [InlineKeyboardButton(
                                text="Открыта",
                                callback_data=f"open:{ticket_id}"
                    )], 
                        [InlineKeyboardButton(
                                text="В работе",
                                callback_data=f"in_work:{ticket_id}"
                    )], 
                        [InlineKeyboardButton(
                                text="Закрыта",
                                callback_data=f"closed:{ticket_id}"
                    )]
    ])
        )
    await callback.answer()


@router.callback_query(F.data.regexp(r"open:\d+$"))
@router.callback_query(F.data.regexp(r"in_work:\d+$"))
@router.callback_query(F.data.regexp(r"closed:\d+$"))
async def process_admin_submenu_tickets_edit_tickets_select_group_select_ticket_edit_status(callback: CallbackQuery):
    ticket_id = callback.data.split(":")
    admin.edit_status(ticket_id=ticket_id[-1], status=LEXCON_TICKETS_STATUS[ticket_id[0]])
    await callback.message.answer(
        text="<b>Новый статус установлен</b>",
        reply_markup=admin_main_inline_kb
        )
    await callback.answer()



@router.callback_query(F.data.in_("admin_drop_tickets"))
async def process_admin_submenu_tickets_drop_tickets(callback: CallbackQuery):
    group_list = {group.group_id: group.group_name for group in admin._return_group_list()}
    await callback.message.answer(
        text="<b>Выберите организацию</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=group, callback_data=f"group_for_admin_drop_ticket{str(id_)}")]
                             for id_, group in group_list.items()] + [[but_admin_back_to_main_menu]])
        )
    await callback.answer()


@router.callback_query(F.data.regexp(r"group_for_admin_drop_ticket\d+$"))
async def process_admin_submenu_tickets_drop_tickets_select_group(callback: CallbackQuery):
    group_id = callback.data[-1]
    ticket_dict = {tic["ticket_id"]: f"{tic["ticket_message"][:45]}..." for tic in admin.show_ticket_list_for_admin(group_id=group_id)}
    await callback.message.answer(
        text="<b>Выберите тикет</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=ticket, callback_data=f"group_for_admin_drop_ticket_select_group_select_ticket:{str(id_)}")]
                             for id_, ticket in ticket_dict.items()] + [[but_admin_back_to_main_menu]])
        )
    await callback.answer()


@router.callback_query(F.data.regexp(r"group_for_admin_drop_ticket_select_group_select_ticket:\d+$"))
async def process_admin_submenu_tickets_edit_tickets_select_group_select_ticket_edit_status(callback: CallbackQuery):
    ticket_id = callback.data.split(":")
    admin.drop_ticket(ticket_id=ticket_id[-1])
    await callback.message.answer(
        text="<b>Тикет удален</b>",
        reply_markup=admin_main_inline_kb
        )
    await callback.answer()




@router.callback_query(F.data.in_("show_users_menu"))
async def process_admin_show_users_menu(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Меню пользователя</b>",
        reply_markup=user_inline_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("show_operators_menu"))
async def process_admin_show_operators_menu(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Меню оператора</b>",
        reply_markup=operator_main_inline_kb
    )
    await callback.answer()
















    

