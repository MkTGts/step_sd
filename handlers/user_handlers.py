import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_RU, LEXCON_USER_HANDLERS
from services.db.services.user_service import UserServiceDB
from keyboards.kyboards_users import user_inline_kb
from filters.filter import IsRegistredUserName, CheckRoleUser




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


user = UserServiceDB()
router = Router()  # инициализация роутера


# класс для хранения состояния
class TicketCreation(StatesGroup):
    waiting_for_text = State()




@router.message(IsRegistredUserName())
async def process_registration_user_name(message: Message):
    user._set_fullname(tg_id=int(message.from_user.id), fullname=message.text)
    await message.answer(
        text=f"Имя {message.text} принято",
        reply_markup=user_inline_kb
    )



@router.callback_query(F.data.in_("user_tickets_list"))
async def process_tickets_list_user(callback: CallbackQuery):
    tickets_list = user.user_ticket_list(user_id=user._return_user_id(callback.from_user.id))
    if tickets_list:
        await callback.message.answer(
            text='\n\n'.join([
                f"ID: {ticket["ticket_id"]}\nСтатус: {ticket["status"]}\nДата создания: {ticket["created"]}\nОписание: {ticket["message"]}"
                for ticket in tickets_list
            ]),
            reply_markup=user_inline_kb
        )
    else:
        await callback.message.answer(
            text=LEXCON_USER_HANDLERS["is_tickets_none"],
            reply_markup=user_inline_kb
        )
    await callback.answer()


@router.callback_query(F.data.in_("user_create_ticket"))
async def process_select_creat_ticket_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=LEXCON_USER_HANDLERS["select_creat_ticket"]
    )
    await state.set_state(TicketCreation.waiting_for_text)
    await callback.answer()


@router.message(TicketCreation.waiting_for_text)
async def process_creating_ticket_user(message: Message, state: FSMContext):
    user.create_ticket(
        user_id=user._return_user_id(message.from_user.id),
        message=message.text
    )
    await message.answer(
        text=LEXCON_USER_HANDLERS["created_ticket"],
        reply_markup=user_inline_kb
    )
    await state.clear()






    

