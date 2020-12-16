from aiogram.types import Message

from bin.cash_var import users_cash as uc

from bot.content import ROLES_TEXT


async def roles(mes: Message):
    if mes.chat.type != 'private':
        return
    if not uc.select_id(mes.from_user.id):
        await mes.answer('Доступ запрещён.')
        return

    guild_tag = uc.select_id(mes.from_user.id).get('guild_tag')
    s = '🏅{} | [{}] | <b>{}</b>'

    members_result = uc.select_guild_tag(guild_tag)
    com_pool, mem_pool = [], []
    for m in members_result:
        role = m.get('role')
        if role in [3, 4]:
            req = s.format(str(m.get('lvl')), m.get('class'), m.get('nickname'))
            com_pool.append(Member(req, m.get('lvl')))
        elif role in [1, 2]:
            req = s.format(str(m.get('lvl')), m.get('class'), m.get('nickname'))
            mem_pool.append(Member(req, m.get('lvl')))
    c_answer = '\n'.join([com.req for com in sorted(com_pool, key=lambda l: -l.lvl)]) if com_pool else ''
    m_answer = '\n'.join([mem.req for mem in sorted(mem_pool, key=lambda l: -l.lvl)]) if mem_pool else ''
    await mes.answer(ROLES_TEXT.format(guild_tag, c_answer, m_answer))


class Member:
    def __init__(self, req, lvl):
        self.req = req
        self.lvl = lvl
    def __repr__(self):
        return self.req