from aiogram.types import Message

from bin.cash_var import users_cash as uc

from bot.content import LOC_TYPES, AL_INFO_TEXT, LOC_INFO_TEXT, AL_HISTORY_TEXT, AL_CAPTURE_TEXT


async def loc_info(mes: Message):
    #journal_log(mes)
    if not uc.check_perm_role(mes.from_user.id, [2, 3, 4]):
        await mes.answer('Доступ запрещён.')
        return
    if len(mes.text) < 9:
        await mes.answer('/l_info [code]')
        return

    code = mes.text[8:]
    loc = mes.db.check('SELECT code,name,lvl,conqueror FROM loc WHERE code = ?', [code])
    pattern = mes.db.check('SELECT code,name,lvl,conqueror FROM loc WHERE name LIKE ?', [code + '%'])

    if loc or pattern:
        answer = await loc_info_answer(mes, loc if loc else pattern)
    else:
        answer = 'Данной локации нет в базе данных.'
    await mes.answer(answer, disable_web_page_preview=True)


async def loc_info_answer(mes: Message, loc: list):
    code, name, lvl, conqueror = loc[0], loc[1], loc[2], loc[3]
    if lvl == 99:
        guilds = mes.db.checkall('SELECT guild_emoji, guild_tag FROM al_guild_info WHERE code = ?', [loc[0]])
        guilds = ','.join(['{}[{}]'.format(l[0], l[1]) for l in guilds]) if guilds else 'Нет данных'

        capture_locs = mes.db.checkall('SELECT code,name,lvl FROM loc WHERE conqueror = ? ORDER BY lvl LIMIT 5', [name])
        capture_locs_num = len(mes.db.checkall('SELECT code,name,lvl FROM loc WHERE conqueror = ?', [name]))
        capture_locs = '\n'.join(['<a href="https://t.me/share/url?url=/l_info%20{}"><b>{}{} lvl.{}</b></a>'.format(
            l[0], LOC_TYPES.get(l[1].split(' ')[-1], 'error'), l[1], str(l[2])) for l in \
            capture_locs]) if capture_locs else 'Нет данных'
        capture_locs += '\n...' if capture_locs_num > 5 else ''

        loc_history = mes.db.checkall('SELECT time, url, txt FROM loc_history WHERE code = ? ORDER BY -url LIMIT 5', [code])
        loc_history_num = len(loc_history)
        loc_history = '\n\n'.join(['[{}]\n{}'.format(
            '<a href="https://t.me/ChatWarsDigest/{}">{}</a>'.format(str(l[1]),l[0]), l[2]) for l in loc_history])
        loc_history = loc_history if loc_history else 'Нет данных'
        loc_history += '\n...' if loc_history_num > 5 else ''

        answer = AL_INFO_TEXT.format(name, code, guilds, code, capture_locs_num, capture_locs, code, loc_history)

    else:
        buffs = mes.db.checkall('SELECT bless_type, bless_name FROM loc_buff_info WHERE code = ?', [code])
        conq_code = mes.db.check('SELECT code FROM loc WHERE name = ?', [conqueror])
        conqueror = '<a href="https://t.me/share/url?url=/l_info%20{}"><b>🎪{}</b></a>'.format(conq_code[0], conqueror)\
            if conq_code else 'Нет данных'

        answer = LOC_INFO_TEXT.format(LOC_TYPES.get(loc[1].split(' ')[-1], 'error'), name, str(lvl), code, conqueror,
                                      (await buff_f(buffs)))
    return answer


async def l_history(mes: Message):
    if not uc.check_perm_role(mes.from_user.id, [2, 3, 4]):
        await mes.answer('Доступ запрещён.')
        return
    if len(mes.text) < 12:
        await mes.answer('/l_history [code]')
        return

    code = mes.text[11:]
    loc = mes.db.check('SELECT name,lvl,conqueror FROM loc WHERE code = ?', [code])

    if not loc:
        await mes.answer('Данной локации нет в базе данных.')
        return
    if loc[1] != 99:
        await mes.answer('Информация доступна только по альянсам.')
        return

    loc_history = mes.db.checkall('SELECT time, url, txt FROM loc_history WHERE code = ? ORDER BY -url LIMIT 20', [code])
    loc_history = '\n\n'.join(['[{}]\n{}'.format(
        '<a href="https://t.me/ChatWarsDigest/{}">{}</a>'.format(str(l[1]), l[0]), l[2]) for l in loc_history])
    loc_history = loc_history if loc_history else 'Нет данных'

    await mes.answer(AL_HISTORY_TEXT.format(code, loc_history), disable_web_page_preview=True)


async def l_capture(mes: Message):
    if not uc.check_perm_role(mes.from_user.id, [2, 3, 4]):
        await mes.answer('Доступ запрещён.')
        return
    if len(mes.text) < 12:
        await mes.answer('/l_capture [code]')
        return

    code = mes.text[11:]
    loc = mes.db.check('SELECT name,lvl,conqueror FROM loc WHERE code = ?', [code])

    if not loc:
        await mes.answer('Данной локации нет в базе данных.')
        return
    if loc[1] != 99:
        await mes.answer('Информация доступна только по альянсам.')
        return

    capture_locs = mes.db.checkall('SELECT code,name,lvl FROM loc WHERE conqueror = ? ORDER BY lvl LIMIT 20', [loc[0]])
    capture_locs = '\n'.join(['<a href="https://t.me/share/url?url=/l_info%20{}"><b>{}{} lvl.{}</b></a>'.format(
        l[0], LOC_TYPES.get(l[1].split(' ')[-1], 'error'), l[1], str(l[2])) for l in \
        capture_locs]) if capture_locs else 'Нет данных'

    await mes.answer(AL_CAPTURE_TEXT.format(code, capture_locs), disable_web_page_preview=True)


async def buff_f(buffs: list):
    text = ''
    b = {}
    for key, value in buffs:
        b.setdefault(key, []).append(value)

    for key, value in b.items():
        last = value.pop()
        text += '    <b>' + key + '</b><i>'
        pre_list = '</i>\n      ├ <i>'.join(value)
        text += '</i>\n      ├ <i>' + pre_list if pre_list else ""
        text += '</i>\n      └ <i>' + last + "</i>\n"
    return text if text else 'Нет данных'