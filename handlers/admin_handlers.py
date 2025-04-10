import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXCON_ADMIN_HANDLERS
from services.db.services.admin_service import AdminServiceDB
from keyboards.kyboards_admins import admin_submenu_users_kb, admin_main_inline_kb, admin_submenu_operators_kb, admin_submenu_groups_kb, admin_submenu_tickets_kb, but_admin_back_to_main_menu
from filters.filter import CheckRoleAdmin
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup




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
@router.callback_query(F.data.in_([f"group_for_admin{str(id_)}" for id_ in range(1, 10)]))
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
@router.callback_query(F.data.in_([f"group_for_admin_drop_user{str(id_)}" for id_ in range(1, 10)]))
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
@router.callback_query(F.data.in_([f"user_for_drop_{str(id_)}" for id_ in range(0, 100)]))
async def process_admin_submenu_users_select_group_drop_user(callback: CallbackQuery):
    user_id: int = int(''.join([s for s in callback.data if s.isdigit()]))
    admin.drop_user(user_id=user_id)
    await callback.message.answer(
        text=f"<b>Пользователь с ID {user_id} удален.</b>"
    )
    await callback.answer()



#################################################################################################
# отберает пользователей по выбранной в прошлом апдейте-хэндлере организации
@router.callback_query(F.data.in_("admin_operators"))
async def process_admin_submenu_users(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Операторы</b>",
        reply_markup=admin_submenu_operators_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("admin_groups"))
async def process_admin_submenu_users(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Организации</b>",
        reply_markup=admin_submenu_groups_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("admin_show_invite_group"))
async def procces_admin_submenu_groups_shwo_invites(callback: CallbackQuery):
    groups = admin.show_group_list()
    await callback.message.answer(
        text="<b>Список инвайтов:</b>\n" +
        "\n\n".join(
            f"Организация: {group["group_name"]}\nИнвайт: {group["invite_token"]}"
            for group in groups
        ),
        reply_markup=admin_main_inline_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("admin_tickets"))
async def process_admin_submenu_tickets(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Тикеты</b>",
        reply_markup=admin_submenu_tickets_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("admin_show_tickets"))
async def process_admin_submenu_tickets_show_tockets(callback: CallbackQuery):
    group_list = {group.group_id: group.group_name for group in admin._return_group_list()}
    await callback.message.answer(
        text="<b>Выберите организацию</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=group, callback_data=f"group_for_admin_ticket{str(id_)}")]
                             for id_, group in group_list.items()] + [[but_admin_back_to_main_menu]])
        )
    await callback.answer()


# при выборе функции список тикетов, выводит клавиатуру с оранизациями для отбора по нужной
@router.callback_query(F.data.in_([f"group_for_admin_ticket{str(id_)}" for id_ in range(1, 10)]))
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













    

