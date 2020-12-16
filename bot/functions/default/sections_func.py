from aiogram.types import Message

from bot.states import battle_states, craft_states
from bot.content import SECTION_LIST
from bin.cash_var import users_cash as uc


# ⚙Другое | 📜Архив
async def sections(mes: Message):
    #journal_log(mes)
    if not uc.select_id(mes.from_user.id):
        await mes.answer('Доступ запрещён.')
        return

    await mes.answer(**SECTION_LIST.get(mes.text))


async def at_hq(mes: Message):
    if not uc.select(**{'id': mes.from_user.id, 'guild_tag': 'AT'}):
        await mes.answer('Доступ запрещён.')
        return

    await mes.answer(**SECTION_LIST.get(mes.text))


# 🔥Битва
async def battle(mes: Message):
    #journal_log(mes)
    if mes.chat.type != 'private':
        return
    if not uc.check_perm_role(mes.from_user.id, [2, 3, 4]):
        await mes.answer('Доступ запрещён.')
        return
    await mes.answer(**SECTION_LIST.get(mes.text))
    await battle_states.menu.set()


# ⚒Мастерская
async def craft(mes: Message):
    #journal_log(mes)
    if mes.chat.type != 'private':
        return
    if not uc.select_id(mes.from_user.id) or not uc.check_perm_role(mes.from_user.id, [2, 3]):
        await mes.answer('Доступ запрещён.')
        return

    await mes.answer(**SECTION_LIST.get(mes.text))
    await craft_states.Q1.set()