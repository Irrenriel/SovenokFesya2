from aiogram.types import Message

from bin.cash_var import users_cash as uc

from bot.content import HELP_COM_TEXT, HELP_MEMBER_TEXT


# ℹПомощь
async def help(mes: Message):
    #journal_log(mes)
    if mes.chat.type != 'private':
        return
    if not uc.select_id(mes.from_user.id):
        await mes.answer('Доступ запрещён.')
        return

    res = uc.select_id(mes.from_user.id).get('role')
    answer = {1: HELP_MEMBER_TEXT, 2: HELP_COM_TEXT, 3: HELP_COM_TEXT, 4: HELP_MEMBER_TEXT}
    await mes.answer(answer.get(res[0], 'Error'))