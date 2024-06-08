from aiogram.fsm.state import StatesGroup, State

from utils.helper import get_weight_of_sciences


class AskQuestion(StatesGroup):
    message = State()


class OrderCall(StatesGroup):
    phone_number = State()


class CalculateNMTscore(StatesGroup):
    iteration = State()
    subjects = State()
    scores = State()
    OU = State()  # only 172

    @staticmethod
    async def calculate_score(data):
        # find k1, k2, k3, k4 in nmt_24_126 or nmt_24_172
        subjects = data['subjects']
        p = data['scores']
        k1_126 = get_weight_of_sciences(subjects['1'], 126)
        k2_126 = get_weight_of_sciences(subjects['2'], 126)
        k3_126 = get_weight_of_sciences(subjects['3'], 126)
        k4_126 = get_weight_of_sciences(subjects['4'], 126)
        k1_172 = get_weight_of_sciences(subjects['1'], 172)
        k2_172 = get_weight_of_sciences(subjects['2'], 172)
        k3_172 = get_weight_of_sciences(subjects['3'], 172)
        k4_172 = get_weight_of_sciences(subjects['4'], 172)
        score_for_126 = ((k1_126 * float(p['1']) + k2_126 * float(p['2']) + k3_126 * float(p['3']) + k4_126 * float(
            p['4'])) / (k1_126 + k2_126 + k3_126 + k4_126)) * 1.07
        score_for_172 = ((k1_172 * float(p['1']) + k2_172 * float(p['2']) + k3_172 * float(p['3']) + k4_172 * float(
            p['4'])) / (k1_172 + k2_172 + k3_172 + k4_172) + float(data['OU'])) * 1.07 * 1.02
        if score_for_126 > 200:
            score_for_126 = 200
        if score_for_172 > 200:
            score_for_172 = 200
        return format(score_for_126, '.3f'), format(score_for_172, '.3f')


class AnswerQuestion(StatesGroup):
    user_id = State()
    answer = State()
