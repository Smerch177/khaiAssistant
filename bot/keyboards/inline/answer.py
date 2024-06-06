from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.factory.callbacks import AnswerCallbackFactory
from loader import i18n

_ = i18n.gettext


def get_answer_inline_markup(user_id: int, locale: str = "en") -> InlineKeyboardBuilder.as_markup:
    builder = InlineKeyboardBuilder()
    builder.button(text=_("Answer the question", locale=locale), callback_data=AnswerCallbackFactory(user_id=user_id)),
    return builder.as_markup()
