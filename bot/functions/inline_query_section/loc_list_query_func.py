from bot.content import CALL_DATA_LOC_TYPE_DICT, LOC_TYPES
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from bin.cash_var import users_cash as uc

async def loc_list_query(query: InlineQuery):
    if not uc.select_id(query.from_user.id):
        return

    mes_text = CALL_DATA_LOC_TYPE_DICT.get('loc_type_cap')
    res = query.db.checkall('SELECT name, lvl, code FROM loc WHERE lvl = 99 ORDER BY name', [])
    txt = '<u><b>{}</b></u>\n\n'.format(mes_text['text'])
    for el in res:
        locs = query.db.checkall(
            'SELECT code,name,lvl,working,work_status FROM loc WHERE conqueror = ? ORDER BY lvl', [el[0]])
        if not locs: continue
        txt += '<b>{}{} ({}):</b>\n'.format('⚜🎪 ', el[0], len(locs))
        for l in locs:
            txt += '{}{} lvl.{} [{}{}]\n'.format(
                LOC_TYPES.get(l[1].split(' ')[-1], 'error'), l[1], str(l[2]), str(l[3]), l[4])
        txt += '\n'
    empty_locs = query.db.checkall('SELECT code,name,lvl FROM loc WHERE conqueror = "Forbidden Clan" ORDER BY lvl', [])
    len_el = len(empty_locs)
    txt += f'<b>🏴‍☠ Forbidden Clan ({len_el})</b>{":" if len_el else ""}\n'
    if len_el:
        for l in empty_locs:
            txt += '{}{} lvl.{}</a>\n'.format(LOC_TYPES.get(l[1].split(' ')[-1], 'error'), l[1], str(l[2]))

    results = []
    results.append(InlineQueryResultArticle(
        id=query.from_user.id,
        title='🚩Карта',
        description='Карта мира',
        input_message_content=InputTextMessageContent(message_text=txt, parse_mode='HTML')
    ))
    await query.answer(results=results, cache_time=1, is_personal=True)