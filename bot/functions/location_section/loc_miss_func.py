from aiogram.types import Message

from bin.cash_var import users_cash as uc

from bot.content import LOC_TYPES


async def loc_miss(mes: Message):
    if not uc.select_id(mes.from_user.id):
        await mes.answer('Доступ запрещён.')
        return

    res = mes.db.checkall('SELECT name, lvl FROM loc WHERE code LIKE "NoneCode%"', [])
    answer = '<b><u>🔎Разыскиваемые локации:</u></b>\n\n{}'
    txt = ''
    if not res:
        answer = answer.format('Пусто')
        await mes.answer(answer)
        return
    for i, l in enumerate(res):
        txt += '<b>{}){} {} lvl.{}</b>\n\n'.format(i+1, LOC_TYPES.get(l[0].split(" ")[-1]), l[0], l[1])
    await mes.answer(answer.format(txt))


