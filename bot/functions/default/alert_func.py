from aiogram.types import Message
import asyncio

from bin.cash_var import users_cash as uc
from bin.main_var import bot


# /say
async def say(mes: Message):
    #journal_log(mes)
    if not uc.check_perm_role(mes.from_user.id, [2, 3]):
        await mes.answer('Доступ запрещён.')
        return
    if len(mes.text) < 6:
        await mes.answer('Необходимо ввести: /say [текст объявления].')
        return

    txt = mes.text[5:]
    for uid in uc.select_guild_tag('AT'):
        try:
            await bot.send_message(uid, txt)
        except:
            pass
        await asyncio.sleep(0.3)

    await mes.answer(f'<b>Объявление успешно объявлено</b>:\n{txt}')


# /news
async def news(mes: Message):
    #journal_log(mes)
    if not uc.check_perm_role(mes.from_user.id, [2, 3]):
        await mes.answer('Доступ запрещён.')
        return
    if len(mes.text) < 7:
        await mes.answer('Необходимо ввести: /news [текст новости].')
        return

    news = mes.text[6:]
    mes.db.query('UPDATE settings SET info = ? WHERE var = "news"', [news])
    await mes.answer(f'<b>Установлена новость:</b>\n{news}')