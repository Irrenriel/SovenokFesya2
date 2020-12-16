from aiogram.types import Message
import re, asyncio, datetime

from bin.main_var import bot
from bin.config import GUILD_MASTER
from bin.cash_var import users_cash as uc

from bot.content import NEW_LOC_INPUT_PARSE
from bot.content import LOC_TYPES


# ПРИЁМ ЛОКАЦИЙ С КВЕСТОВ
async def new_loc(mes: Message):
    if not datetime.datetime.now() - mes.forward_date < datetime.timedelta(days=2):
        return

    # Определение это локация или альянс и расфасовка в словарь
    result = re.search(NEW_LOC_INPUT_PARSE, mes.text).groupdict()
    result = {k: v for k, v in result.items() if v is not None}
    code = result.get("loc_code", result.get("head_code"))

    # Определение есть ли данная точка в БД
    if mes.db.check('SELECT * FROM loc WHERE code = ?', [code]):
        l = await mes.answer('Данная локация уже есть в базе.')
        await asyncio.sleep(2)
        await bot.delete_message(mes.chat.id, mes.message_id)
        await asyncio.sleep(8)
        await l.delete()
        return

    name = result.get("loc_name", result.get("head_name"))
    lvl = int(result.get("loc_lvl", "99"))
    type = LOC_TYPES.get(name.split(' ')[-1], '🎪 ')

    check = mes.db.check('SELECT code from loc WHERE name = ? and lvl = ?', [name, lvl])
    if check:
        if check[0].startswith('NoneCode'):
            mes.db.query('UPDATE loc SET code = ? WHERE name = ? and lvl = ?', [code, name, lvl])
        else:
            mes.db.query('INSERT INTO loc (name, lvl, code) VALUES (?,?,?)', [name, lvl, code])
    else:
        mes.db.query('INSERT INTO loc (name, lvl, code) VALUES (?,?,?)', [name, lvl, code])

    # Награда за нахождение
    top = mes.db.check('SELECT top_loc FROM users WHERE id = ?', [mes.from_user.id])
    if top:
        mes.db.query('UPDATE users SET top_loc = top_loc + 1 WHERE id = ?', [mes.from_user.id])
        uc.loading()

    # Оповещение о новой локации
    answer = type + name + ("" if lvl == 99 else " lvl. " + str(lvl))
    text = f'Обнаружена новая локация!\n\n<b>{answer}</b>\n  └ <code>{code}</code>\n\nНашедший: @{mes.from_user.username}'
    chats = mes.db.checkall('SELECT id FROM chats WHERE new_loc_ntf = 1', [])

    if not chats:
        await mes.answer('Новая локация! {}'.format(
            'Зачислен +1 балл! (/top)' if top else 'Балл не засчитан, требуется регистрация.'))
        return

    for chat in chats:
        try:
            await bot.send_message(chat[0], text)
        except:
            pass
        await asyncio.sleep(0.3)
    await mes.answer('Новая локация! {}'.format(
        'Зачислен +1 балл!' if top else 'Балл не засчитан, требуется регистрация.'))


async def new_loc_info(mes: Message):
    #journal_log(mes)
    if not uc.check_perm_role(mes.from_user.id, [2, 3, 4]):
        await mes.answer('Доступ запрещён.')
        return

    code = re.search(r'ga_use_(?P<code>.+)_', mes.text).group('code')
    if not mes.db.check('SELECT * FROM loc WHERE code = ?', [code]):
        await mes.answer('Данной локации нет в базе данных.')
        return

    cont1 = mes.text.split(' attractions:\n')
    parse = re.search(r'(?P<loc_name>\w.+) lvl\.(?P<loc_lvl>\d+)', cont1[0])
    name = parse.group('loc_name')
    lvl = int(parse.group('loc_lvl'))

    cont1 = cont1[1].split('✨')[1:]
    for el in cont1:
        bless_type = el.split('\n')[0]
        cont2 = el.replace(bless_type + '\n', '').split('🎖\n')
        for l in cont2:
            if l:
                bless_name = l.split('\n')[0][2:]
                if not mes.db.check('SELECT * FROM loc_buff_info WHERE code = ? and bless_name = ?', [code, bless_name]):
                    mes.db.query(
                        'INSERT INTO loc_buff_info (name, lvl, code, bless_type, bless_name) VALUES (?,?,?,?,?)',
                        [name, lvl, code, bless_type, bless_name])
    await mes.answer('Записал👍')