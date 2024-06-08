from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.database.services import edit_user_phone, update_user_score
from bot.factory.callbacks import AnswerCallbackFactory, PostCallbackFactory
from bot.filters.user import AskQuestion, OrderCall, AnswerQuestion, CalculateNMTscore
from bot.keyboards.default import get_default_markup
from bot.keyboards.default.calculate_score import make_row_keyboard, subjects, make_ou_keyboard
from data.config import MINSCOREFORBUDGET172, MINSCOREFORBUDGET126
from loader import bot
from models import User
from tasks import send_question_to_admin

router = Router()


@router.callback_query(AnswerCallbackFactory.filter())
async def _answer_on_question(callback: types.CallbackQuery, callback_data: AnswerCallbackFactory, state: FSMContext):
    await state.update_data(user_id=callback_data.user_id)
    await state.set_state(AnswerQuestion.answer)
    await callback.message.answer(_('Enter answer'))


@router.message(AnswerQuestion.answer, F.text.len() < 4096)
async def _set_answer(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await bot.send_message(data['user_id'], _('Answer: {text}').format(text=data['text']))
    await state.clear()
    await message.answer(_('Your answer has been sent'))


@router.callback_query(PostCallbackFactory.filter(F.action == 'ask_question'))
@router.message(F.text == __('Ask a question 🙋'))
@router.message(Command('ask_question'))
async def _ask_question(message: Message, state: FSMContext):
    await state.set_state(AskQuestion.message)
    await message.answer(_('Enter your question'))


@router.message(AskQuestion.message, F.text.len() < 4096)
async def _set_question_message(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await send_question_to_admin.kiq(data, message.from_user)
    await state.clear()
    await message.answer(_('Your question has been sent'))


@router.callback_query(PostCallbackFactory.filter(F.action == 'order_call'))
@router.message(F.text == __('Order a call 📞'))
@router.message(Command('order_call'))
async def _order_call(message: Message, state: FSMContext):
    await state.set_state(OrderCall.phone_number)
    await message.answer(_('Enter your phone number'))


@router.message(OrderCall.phone_number, F.text.regexp(r'^\+?\d{11,15}$'))
async def _set_phone(message: Message, state: FSMContext, user: User):
    await state.update_data(phone_number=message.text)
    await state.clear()
    await message.answer(_('Your call has been ordered'))
    await edit_user_phone(user, message.text)


@router.message(F.text == __('Calculate your score 🧮'))
@router.message(Command('calculate_score'))
async def _calculate_score(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(CalculateNMTscore.subjects)
    data = await state.get_data()
    await message.answer(_('Choose the science'), reply_markup=make_row_keyboard(data))


@router.message(CalculateNMTscore.subjects, F.text.in_(subjects))
async def _set_subjects(message: Message, state: FSMContext):
    data = await state.get_data()
    iteration = data.get('iteration', 0) + 1
    await state.update_data(iteration=iteration, subjects={**data.get('subjects', {}), iteration: message.text})
    await state.set_state(CalculateNMTscore.scores)
    await message.answer(_('Enter the score'))


@router.message(CalculateNMTscore.scores, F.text.func(lambda text: 0 <= int(text) <= 200))
async def _set_scores(message: Message, state: FSMContext):
    data = await state.get_data()
    iteration = data.get('iteration', 1)
    await state.update_data(scores={**data.get('scores', {}), iteration: int(message.text)})
    if iteration == 4:
        await state.set_state(CalculateNMTscore.OU)
        await message.answer(
            _('Do you have a KHAI certificate of successful completion of preparatory courses?'
              '(It is considered only for the specialty 172)'),
            reply_markup=make_ou_keyboard()
        )
        return
    await state.set_state(CalculateNMTscore.subjects)
    await message.answer(_('Choose the science'), reply_markup=make_row_keyboard(data))


@router.message(CalculateNMTscore.OU, F.text.in_([__('Yes'), __('No')]))
async def _set_ou(message: Message, user: User, state: FSMContext):
    if message.text == __('Yes'):
        await state.update_data(OU=10)
    else:
        await state.update_data(OU=0)
    data = await state.get_data()
    score_126, score_172 = CalculateNMTscore.calculate_score(data)
    await update_user_score(user, score_126, score_172)
    answer_126 = _('Your score for 126 - Information systems and technologies is:\n{score_126}').format(score_126=score_126)
    answer_172 = _(
        'Your score for 172 - Electronic communications and radio engineering is:\n{score_172} '
        '(Your points for admission under the first and second priority)').format(score_172=score_172)
    if MINSCOREFORBUDGET126 <= score_126:
        answer_126 += _(' You can pass on a budget!')
    else:
        answer_126 += _(' Unfortunately, you may not qualify for the budget')
    if MINSCOREFORBUDGET172 <= score_172:
        answer_172 += _(' You can pass on a budget!')
    else:
        answer_172 += _(' Unfortunately, you may not qualify for the budget')
    await message.answer(answer_126 + '\n' + answer_172, reply_markup=get_default_markup(user))
    await state.clear()
