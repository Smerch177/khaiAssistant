import csv

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.database.services import count_users, get_users, get_user_ordered_call, get_users_with_score
from bot.filters.admin import AdminFilter, Post
from brok import redis_source
from loader import config
from tasks import send_post
from utils.helper import convert_datetime_from_local_to_utc, validate_datetime

router = Router()


@router.message(F.text == __('Chats list 📁'), AdminFilter())
@router.message(Command('chats_list'), AdminFilter())
async def _chats_list(message: Message):
    _list = _('Chats list 📁') + '\n\n'
    for user in await get_users():
        _list += f'{user.id} - {user.name} - @{user.username}\n'
    await message.answer(_list)


@router.message(F.text == __('Call list 📞'), AdminFilter())
@router.message(Command('call_list'), AdminFilter())
async def _call_list(message: Message):
    _list = _('Call list 📞') + '\n\n'
    for user in await get_user_ordered_call():
        _list += f'{user.id} - {user.name} - @{user.username} - {user.phone}\n'
    await message.answer(_list)


@router.message(F.text == __('View user scores 🧮'), AdminFilter())
@router.message(Command('view_user_scores'), AdminFilter())
async def _view_user_scores(message: Message):
    _list = _('User scores 🧮') + '\n\n'
    for user in await get_users_with_score():
        _list += f'{user.id} - {user.name} - @{user.username} - 126: {user.score_126} - 172: {user.score_172}\n'
    await message.answer(_list)


@router.message(F.text == __('Create post ✉️'), AdminFilter())
@router.message(Command('create_post'), AdminFilter())
async def _create_post(message: Message, state: FSMContext):
    await state.set_state(Post.message)
    await message.answer(_('Enter the text of the post'))


@router.message(Post.message)
async def _set_post_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Post.photo)
    await message.answer(_('Send a photo of the post'))


@router.message(Post.photo, F.photo)
async def _set_post_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id, photo_unique_id=message.photo[-1].file_unique_id)
    await state.set_state(Post.date)
    await message.answer(_('Send the date of the post, example: 2024-12-31 23:59:59'))


@router.message(Post.date)
async def _set_post_date(message: Message, state: FSMContext):
    try:
        date = convert_datetime_from_local_to_utc(validate_datetime(message.text))
    except ValueError:
        await message.answer(_('Invalid date format. Use YYYY-MM-DD HH:MM:SS'))
        return
    await state.update_data(date=str(date))
    await state.set_state(Post.date)
    await message.answer(_('Post created'))
    data = await state.get_data()
    await send_post.schedule_by_time(redis_source, validate_datetime(data['date']), data)
    await state.clear()
