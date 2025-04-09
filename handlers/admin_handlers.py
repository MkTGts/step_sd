import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXCON_ADMIN_HANDLERS
from services.db.services.admin_service import AdminServiceDB
from keyboards.kyboards_admins import admin_submenu_users_kb, admin_main_inline_kb
from filters.filter import CheckRoleAdmin




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



@router.callback_query(F.data.in_("admin_users"))
async def process_admin_submenu_users(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Пользователи</b>",
        reply_markup=admin_submenu_users_kb
    )
    await callback.answer()


@router.callback_query(F.data.in_("back_to_main_menu"))
async def process_admin_back_to_main_menu(callback: CallbackQuery):
    await callback.message.answer(
        text="<b>Основное меню</b>",
        reply_markup=admin_main_inline_kb
    )
    await callback.answer()






    

