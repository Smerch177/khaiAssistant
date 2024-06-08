from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from bot.keyboards.default import get_default_markup
from models import User
from aiogram.utils.i18n import gettext as _


router = Router()


@router.message(StateFilter('*'))
async def _default_menu(message: Message, user: User):
    text = _('Choose an action from the menu 👇')
    text = text + '\n\n' + 'Developed by @Smerch_vlad'
    await message.answer(text, reply_markup=get_default_markup(user))
