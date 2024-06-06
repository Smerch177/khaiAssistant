from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.factory.callbacks import PostCallbackFactory

from loader import i18n

_ = i18n.gettext


def get_post_inline_markup(locale="en") -> InlineKeyboardBuilder.as_markup:
    builder = InlineKeyboardBuilder()
    builder.button(text=_("Ask a question 🙋", locale=locale), callback_data=PostCallbackFactory(action="ask_question"))
    builder.button(text=_("Order a call 📞", locale=locale), callback_data=PostCallbackFactory(action="order_call"))
    return builder.as_markup()
