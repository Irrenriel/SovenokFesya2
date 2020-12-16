from aiogram.types import Message
import asyncio

from bin.main_var import bot
from bin.cash_var import users_cash as uc


async def loc_del(mes: Message):
    #journal_log(mes)
    if not uc.check_perm_role(mes.from_user.id, [2, 3, 4]):
        await mes.answer('Доступ запрещён.')
        return
    if len(mes.text) < 8:
        await mes.answer('/l_del [location_code]')
        return

    code = mes.text[7:]
    if not mes.db.checkall('SELECT * FROM loc WHERE code = ?', [code]):
        await mes.answer('Невозможно. Такой локации нет в базе.')
        return

    mes.db.query('DELETE FROM loc WHERE code = ?', [code])
    mes.db.query('DELETE FROM loc_buff_info WHERE code = ?', [code])
    mes.db.query('DELETE FROM al_guild_info WHERE code = ?', [code])

    chats = mes.db.checkall('SELECT id FROM chats WHERE delete_loc_ntf = 1', [])
    answer = f'Локация с кодом <code>{code}</code> была удалена!\n\nУдаливший: @{mes.from_user.username}'

    if not chats:
        await mes.answer('Done!')
        return

    for chat in chats:
        try:
            await bot.send_message(chat[0], answer)
        except:
            pass
        await asyncio.sleep(0.3)
    await mes.answer('Done!')