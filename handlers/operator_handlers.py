import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_OPERATOR_HANDLERS, LEXCON_TICKETS_STATUS
from services.db.services.operator_service import OperatorServiceDB
from keyboards.kyboards_operators import operator_main_inline_kb, but_operator_back_to_main_menu
from filters.filter import IsRegistredUserName, CheckRoleUser
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




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


operator = OperatorServiceDB()
router = Router()  # инициализация роутера


# класс для хранения состояния
class TicketCreation(StatesGroup):
    waiting_for_text = State()



@router.callback_query(F.data.in_("operator_users_list_show"))
async def process_operators_list_user_show(callback: CallbackQuery):
    users_list = operator.show_groups_users(tg_id=int(callback.from_user.id))
    if users_list:
        await callback.message.answer(
            text='\n\n'.join([
                f"<b>ID</b>: {user["user_id"]}\n<b>Username</b>: {user["username"]}\n<b>Имя</b>: {user["fullname"]}\n<b>IP пользователя</b>: {user["user_ip"]}\n<b>Расположение рабочего места пользователя</b>: {user["user_geo"]}"
                for user in users_list
            ]),
            reply_markup=operator_main_inline_kb
        )
    else:
        await callback.message.answer(
            text=LEXICON_OPERATOR_HANDLERS["users_is_none"],
            reply_markup=operator_main_inline_kb
        )
    await callback.answer()


@router.callback_query(F.data.in_("operator_tickets_show"))
async def process_operator_submenu_tickets_tickets_list(callback: CallbackQuery):
    tickets_list = operator.show_ticket_list_for_operator(tg_id=callback.from_user.id)

    await callback.message.answer(
        text='\n\n'.join([
                f"<b>ID</b>: {ticket["ticket_id"]}\n<b>Статус</b>: {f"<u>{ticket["ticket_status"]}</u>"}\n<b>Имя пользователя</b>: {ticket["user_name"]}\n<b>ТГ пользователя</b>: {ticket["user_tg"]}\n<b>Дата создания тикета</b>: {ticket["ticket_create_date"]}\n<b>Тикет</b>:  {ticket["ticket_message"]}"
                for ticket in tickets_list
            ]),
        reply_markup=operator_main_inline_kb
    )

    await callback.answer()


#operator_edit_status_ticekt
@router.callback_query(F.data.in_("operator_edit_status_ticket"))
async def process_admin_submenu_tickets_edit_tickets_select_group(callback: CallbackQuery):
    #group_id = callback.data[-1]
    ticket_dict = {tic["ticket_id"]: f"{tic["ticket_message"][:45]}..." for tic in operator.show_ticket_list_for_operator(tg_id=callback.from_user.id)}
    await callback.message.answer(
        text="<b>Выберите тикет</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"{id_}: {ticket}", callback_data=f"operator_edit_status_select_ticket:{str(id_)}")]
                             for id_, ticket in ticket_dict.items()] + [[but_operator_back_to_main_menu]])
        )
    await callback.answer()


@router.callback_query(F.data.regexp(r"operator_edit_status_select_ticket:\d+$"))
async def process_admin_submenu_tickets_edit_tickets_select_group_select_ticket(callback: CallbackQuery):
    ticket_id = callback.data.split(":")[-1]
    await callback.message.answer(
        text="<b>Выберите новый статус для тикета</b>",
        reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                        [InlineKeyboardButton(
                                text="Открыта",
                                callback_data=f"operator_open:{ticket_id}"
                    )], 
                        [InlineKeyboardButton(
                                text="В работе",
                                callback_data=f"operator_in_work:{ticket_id}"
                    )], 
                        [InlineKeyboardButton(
                                text="Закрыта",
                                callback_data=f"operator_closed:{ticket_id}"
                    )]
    ])
        )
    await callback.answer()


@router.callback_query(F.data.regexp(r"operator_open:\d+$"))
@router.callback_query(F.data.regexp(r"operator_in_work:\d+$"))
@router.callback_query(F.data.regexp(r"operator_closed:\d+$"))
async def process_admin_submenu_tickets_edit_tickets_select_group_select_ticket_edit_status(callback: CallbackQuery):
    ticket_id = callback.data.split(":")
    operator.edit_status(ticket_id=ticket_id[-1], status=LEXCON_TICKETS_STATUS[ticket_id[0]])
    await callback.message.answer(
        text="<b>Новый статус установлен</b>",
        reply_markup=operator_main_inline_kb
        )
    await callback.answer()


    

