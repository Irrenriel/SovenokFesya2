from aiogram.types import Message
import re

from bin.config import ADMIN
from bin.cash_var import users_cash as uc


# /sql
async def sql(mes: Message):
    if mes.from_user.id != ADMIN:
        return
    mode = int(re.search(r'/sql (.)', mes.text).group(1))
    poll = mes.text[7:]
    await mes.answer(await db_req(mes, mode, poll))
    uc.loading()


async def db_req(mes: Message, mode: str, poll: str):
    if mode == 1:
        req = str(mes.db.check(poll, []))
    elif mode == 2:
        req = str(mes.db.checkall(poll, []))
    elif mode == 3:
        req = str(mes.db.query(poll, []))
        req = 'Done' if req is None else 'None'
    else:
        req = 'Error'
    return req if req else 'Empty'


async def info(mes: Message):
    if mes.from_user.id != ADMIN:
        return
    if mes.reply_to_message is None:
        return

    await mes.answer(mes.reply_to_message)