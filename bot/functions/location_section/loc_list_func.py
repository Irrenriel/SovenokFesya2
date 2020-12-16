from aiogram.types import CallbackQuery
from aiogram.types import Message

from bin.cash_var import users_cash as uc

from bot.keyboards import loc_keyboard
from bot.content import CALL_DATA_LOC_TYPE_DICT, LOC_TYPES, LOC_LIST_TEXT


async def loc_list(mes: Message):
    #journal_log(mes)
    if not uc.select_id(mes.from_user.id):
        await mes.answer('Доступ запрещён.')
        return

    als_len = len(mes.db.checkall('SELECT * FROM loc WHERE lvl = 99', []))
    mines_len = len(mes.db.checkall('SELECT * FROM loc WHERE name LIKE "%Mine%"', []))
    ruins_len = len(mes.db.checkall('SELECT * FROM loc WHERE name LIKE "%Ruins%"', []))
    forts_len = len(mes.db.checkall('SELECT * FROM loc WHERE name IN ("Fort", "Tower", "Outpost")', []))
    last_update = mes.db.check('SELECT info FROM settings WHERE name = "last_l_check"', [])[0]

    txt = LOC_LIST_TEXT.format(ruins_len, mines_len, forts_len, als_len, last_update)
    await mes.answer(txt, reply_markup=loc_keyboard)


async def loc_type(call: CallbackQuery):
    await call.answer(cache_time=2)
    mes_text = CALL_DATA_LOC_TYPE_DICT.get(call.data)

    # 🚩Карта
    if call.data == 'loc_type_cap':
        als = call.db.checkall('SELECT name, lvl, code FROM loc WHERE lvl = 99 ORDER BY name', [])
        txt = '<u><b>{}</b></u>\n\n'.format(mes_text['text'])
        for al in als:
            # All locations of alliance
            locs = call.db.checkall(
                'SELECT code,name,lvl,working,work_status FROM loc WHERE conqueror = ? ORDER BY lvl', [al[0]])
            if not locs:
                continue

            # String with alliance
            txt += f'<b>⚜🎪<a href="https://t.me/share/url?url=/l_info%20{al[2]}">{al[0]}</a> ({len(locs)}):</b>\n'
            for l in locs:
                txt += '{} <a href="https://t.me/share/url?url=/l_info%20{}">{} lvl.{}</a> [{}{}]\n'.format(
                    LOC_TYPES.get(l[1].split(' ')[-1], 'error'), l[0], l[1], str(l[2]), str(l[3]), l[4])
            txt += '\n'

        empty_locs = call.db.checkall('SELECT code,name,lvl FROM loc WHERE conqueror = "Forbidden Clan" ORDER BY lvl', [])
        len_el = len(empty_locs)
        txt += f'<b>🏴‍☠ Forbidden Clan ({len_el})</b>{":" if len_el else ""}\n'
        if len_el:
            for l in empty_locs:
                txt += '{} <a href="https://t.me/share/url?url=/l_info%20{}">{} lvl.{}</a>\n'.format(
                    LOC_TYPES.get(l[1].split(' ')[-1], 'error'), l[0], l[1], str(l[2]))

        await call.message.edit_text(txt, reply_markup=loc_keyboard)
        return

    # 🎪Альянсы
    if call.data == 'loc_type_al':
        res = call.db.checkall('SELECT name, lvl, code FROM loc WHERE lvl = 99 ORDER BY name', [])

    # 🏷Руины & 📦Шахты
    elif call.data == 'loc_type_ruins' or call.data == 'loc_type_mines':
        res = call.db.checkall('SELECT name, lvl, code FROM loc WHERE name LIKE {} ORDER BY lvl'.format(mes_text['parse']), [])

    # 🎖Форты
    elif call.data == 'loc_type_forts':
        res = call.db.checkall('SELECT name, lvl, code FROM loc WHERE name IN {} ORDER BY lvl'.format(mes_text['parse']), [])

    txt = '<u><b>{}</b></u>\n\n'.format(mes_text['text'])
    for i, el in enumerate(res):
        num, type, name = i + 1, mes_text['type'], str(el[0])
        lvl, code = '' if not mes_text['parse'] else ' lvl.' + str(el[1]), str(el[2])
        txt += f'<b>{num}){type}{name}{lvl}</b> — <code>{code}</code>\n\n'
    await call.message.edit_text(txt, reply_markup=loc_keyboard)