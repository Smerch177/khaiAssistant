from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
from aiogram.utils.i18n import gettext as _


subjects = ['Математика(Math)', 'Фізика(Physics)', 'Хімія(Chemistry)', 'Біологія(Biology)', 'Іноземна мова(Foreign)',
            'Історія України(History)', 'Українська мова(Ukrainian)', 'Українська література(Ukrainian literature)',
            'Географія(Geography)']


def make_row_keyboard(data: dict):
    builder = ReplyKeyboardBuilder()
    subj = data.get('subjects', {})
    excluded = []
    if len(subj) > 0:
        for item in subj.values():
            excluded.append(item)
    for item in subjects:
        if item not in excluded:
            builder.add(KeyboardButton(text=item))
    builder.adjust(3)
    return builder.as_markup()


def make_ou_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=_('Yes')), KeyboardButton(text=_('No')))
    return builder.as_markup()
