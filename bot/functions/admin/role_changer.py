from aiogram.types import Message

from bin.config import ADMIN
from bin.cash_var import users_cash as uc


async def reg_as(mes: Message):
    if mes.from_user.id != ADMIN:
        return
    if mes.reply_to_message is None:
        await mes.answer('Error')
        return
    if not uc.select_id(mes.reply_to_message.from_user.id):
        await mes.answer('Not in database')
        return

    mes.db.query('UPDATE users SET role = ? WHERE id = ?', [mes.text[8:], mes.reply_to_message.from_user.id])
    uc.loading()