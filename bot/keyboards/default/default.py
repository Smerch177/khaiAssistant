from aiogram.types import ReplyKeyboardRemove, KeyboardButton

from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_default_markup(user):
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=_('Help 🆘')), KeyboardButton(text=_('Settings 🛠')))

    if user.is_admin:
        builder.add(KeyboardButton(text=_('Chats list 📁')))
        builder.add(KeyboardButton(text=_('Call list 📞')))
        builder.add(KeyboardButton(text=_('Create post ✉️')))
        builder.add(KeyboardButton(text=_('View user scores 🧮')))

    builder.add(KeyboardButton(text=_('Ask a question 🙋')))
    builder.add(KeyboardButton(text=_('Order a call 📞')))
    builder.add(KeyboardButton(text=_('Calculate your score 🧮')))


    if len(builder._markup) < 1:
        return ReplyKeyboardRemove()

    builder.adjust(3)

    return builder.as_markup()
