from aiogram.types import CallbackQuery, Message

from bin.cash_var import users_cash as uc

from bot.keyboards import patchnote_keyboard
from bot.content import PATCHNOTE_TEXT, V1_0_TEXT, V1_1_TEXT, V1_2_TEXT, V1_3_TEXT, V1_3_3_TEXT, V1_4_TEXT, V2_0_TEXT, \
    V2_1_TEXT

# 💠Патчноут
async def patchnote(mes: Message):
    #journal_log(mes)
    if mes.chat.type != 'private':
        return
    if not uc.select_id(mes.from_user.id):
        await mes.answer('Доступ запрещён.')
        return
    await mes.answer(PATCHNOTE_TEXT, reply_markup=patchnote_keyboard)


async def patchnote_v(call: CallbackQuery):
    await call.answer(cache_time=2)
    answer = {'v10': V1_0_TEXT, 'v11': V1_1_TEXT, 'v12': V1_2_TEXT, 'v13': V1_3_TEXT, 'v133': V1_3_3_TEXT,
              'v14': V1_4_TEXT, 'v20': V2_0_TEXT, 'v21': V2_1_TEXT}
    await call.message.edit_text(answer.get(call.data, 'Error'), reply_markup=patchnote_keyboard)


async def callback_cancel(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.delete()