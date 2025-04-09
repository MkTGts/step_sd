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


@router.callback_query(F.data.in_("admin_users"))
async def process_admin_submenu_users(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Пользователи</b>",
        reply_markup=admin_submenu_users_kb
    )
    await callback.answer()

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


@router.callback_query(F.data.in_([f"group_for_admin{str(id_)}" for id_ in range(1, 10)]))
async def process_admin_submenu_users_select_group(callback: CallbackQuery):
    group_id = callback.data[-1]

    await callback.message.answer(
        text="<b>Список пользователей:</b>\n" +
        "\n\n".join([
            f"ID пользователя: {user['user_id']}\nTG ID: {user['tg_id']}\nusername: {user['username']}\nПолное имя: {user['fullname']}\nIP пользователя: {user['user_ip']}\nРасположение рабочего места пользователя: {user['user_geo']}"
            for user in admin.show_user_list_by_group_id(groupd_id=group_id)
        ])
    )
    await callback.answer()


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


@router.callback_query(F.data.in_("admin_tickets"))
async def process_admin_submenu_users(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Тикеты</b>",
        reply_markup=admin_submenu_tickets_kb
    )
    await callback.answer()











    

