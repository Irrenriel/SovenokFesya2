from aiogram.types import Message

from bin.cash_var import users_cash as uc


async def top(mes: Message):
    if not uc.select_id(mes.from_user.id):
        await mes.answer('Доступ запрещён.')
        return

    req = 'SELECT nickname, class, guild_tag, top_loc FROM users WHERE top_loc != 0 ORDER BY -top_loc LIMIT 10'
    text = '<u><b>🗺Топ нашедших:</b></u>\n\n'
    users = mes.db.checkall(req)
    for i, user in enumerate(users):
        text += f'<b>{i+1}) {user[1]}[{user[2]}]{user[0]} — {user[3]}</b>\n'
    await mes.answer(text)
