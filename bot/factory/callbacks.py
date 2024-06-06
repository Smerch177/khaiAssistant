from aiogram.filters.callback_data import CallbackData


class LanguageCallbackFactory(CallbackData, prefix="lang"):
    language_code: str


class AnswerCallbackFactory(CallbackData, prefix="answer"):
    user_id: int


class PostCallbackFactory(CallbackData, prefix="post"):
    action: str
