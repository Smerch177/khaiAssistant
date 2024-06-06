import taskiq_aiogram
from aiogram.types import User

from bot.database.services import get_users, get_admins
from bot.keyboards.inline.answer import get_answer_inline_markup
from bot.keyboards.inline.post import get_post_inline_markup
from brok import broker
from taskiq import TaskiqDepends
from aiogram import Bot

from loader import i18n

_ = i18n.gettext

# This line is going to initialize everything.
taskiq_aiogram.init(
    broker,
    # This is path to the dispatcher.
    "loader:dp",
    # This is path to the bot instance.
    "loader:bot",
    # You can specify more bots here.
)


@broker.task(task_name="send_post")
async def send_post(data: dict, bot: Bot = TaskiqDepends()):
    get_all_users = await get_users()
    for user in get_all_users:
        await bot.send_photo(user.id, data["photo"], caption=data["text"],
                             reply_markup=get_post_inline_markup(locale=user.language))


@broker.task(task_name="send_question_to_admin")
async def send_question_to_admin(data: dict, user: User, bot: Bot = TaskiqDepends()):
    get_all_admins = await get_admins()
    for admin in get_all_admins:
        text = _("Question from {name}(@{username}):\n\n{text}", locale=admin.language).format(
            name=user.full_name,
            username=user.username,
            text=data['text'])
        await bot.send_message(admin.id, text, reply_markup=get_answer_inline_markup(user.id, locale=admin.language))
