from aiogram.types import BotCommandScopeChat, BotCommand

from loader import bot
from .default import get_default_commands
from aiogram.utils.i18n import gettext as _


def get_admin_commands(lang: str = 'en') -> list[BotCommand]:
    commands = get_default_commands(lang)

    commands.extend([
        BotCommand(command='/chats_list', description=_('get list of chats', locale=lang)),
        BotCommand(command='/call_list', description=_('get list of calls', locale=lang)),
        BotCommand(command='/create_post', description=_('create post', locale=lang)),
        BotCommand(command='/view_user_scores', description=_('view user scores', locale=lang)),
    ])

    return commands


async def set_admin_commands(user_id: int, commands_lang: str):
    await bot.set_my_commands(commands=get_admin_commands(commands_lang), scope=BotCommandScopeChat(chat_id=user_id))
