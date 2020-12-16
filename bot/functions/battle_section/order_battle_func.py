from aiogram.dispatcher import FSMContext
from aiogram.types import Message
import re, random, datetime, json

from bin.main_var import bot

from bot.states import battle_states
from bot.keyboards import ReplyKeyboard, start_menu, pub_pin_keyboard

from bot.content import ORDER_START_TEXT, START_MAIN_MENU_TEXT, START_HEADER_TEXT, ORDER, CALL_DATA_LOC_TYPE_DICT, \
    LOC_TYPES


async def create_pin(mes: Message):
    now = datetime.datetime.now()
    h = now.hour
    if h < 1 or h >= 17:
        n = '01'
    elif 1 <= h < 9:
        n = '09'
    elif 9 <= h < 17:
        n = '17'
    else:
        n = 'XX'
    d = ORDER.format(n=n)

    await mes.answer(ORDER_START_TEXT.format(d), reply_markup=ReplyKeyboard('Локации🗺', 'Вернуться↩'))
    await battle_states.menu_pin.set()

async def create_pin_loc_list(mes: Message):
    mes_text = CALL_DATA_LOC_TYPE_DICT.get('loc_type_cap')
    als = mes.db.checkall('SELECT name, lvl, code FROM loc WHERE lvl = 99 ORDER BY name', [])
    txt = '<u><b>{}</b></u>\n\n'.format(mes_text['text'])
    for al in als:
        # All locations of alliance
        locs = mes.db.checkall(
            'SELECT code,name,lvl,working,work_status FROM loc WHERE conqueror = ? ORDER BY lvl', [al[0]])
        if not locs:
            continue

        # String with alliance
        if al[0] == 'Alert Eyes':
            txt += f'<b>⚜🎪{al[0]} ({len(locs)}):</b> — <code>/ga_def_{al[2]}</code>\n'
        else:
            txt += f'<b>⚜🎪{al[0]} ({len(locs)}):</b> — <code>/ga_atk_{al[2]}</code>\n'
        if al[0] == 'Alert Eyes':
            for l in locs:
                c = 'None' if l[0].startswith('NoneCode') else l[0]
                txt += '{} {} lvl.{} [{}{}] — <code>/ga_def_{}</code>\n'.format(
                    LOC_TYPES.get(l[1].split(' ')[-1], 'error'), l[1], str(l[2]), str(l[3]), l[4], c)
        else:
            for l in locs:
                c = 'None' if l[0].startswith('NoneCode') else l[0]
                txt += '{} {} lvl.{} [{}{}] — <code>/ga_atk_{}</code>\n'.format(
                    LOC_TYPES.get(l[1].split(' ')[-1], 'error'), l[1], str(l[2]), str(l[3]), l[4], c)
        txt += '\n'

    empty_locs = mes.db.checkall('SELECT code,name,lvl FROM loc WHERE conqueror = "Forbidden Clan" ORDER BY lvl', [])
    len_el = len(empty_locs)
    txt += f'<b>🏴‍☠ Forbidden Clan ({len_el})</b>{":" if len_el else ""}\n'
    if len_el:
        for l in empty_locs:
            txt += '{} {} lvl.{} — <code>/ga_atk_{}</code>\n'.format(
                LOC_TYPES.get(l[1].split(' ')[-1], 'error'), l[1], str(l[2]), 'None' if l[0].startswith('NoneCode') else l[0])

    await mes.answer(txt)


async def public_pin(mes: Message):
    txt = mes.text.split('\n')
    answer = f'<b><u>Приказ от: @{mes.from_user.username}</u></b>\n'
    m = '<a href="https://t.me/share/url?url={}"><b>{}{}{}</b></a>'
    targets = ['ga_atk ', 'ga_atk_', 'ga_def ', 'ga_def_']
    tactics = {'амбер': '/t_amber', 'скала': '/t_skala', 'роза': '/t_rassvet', 'рассвет': '/t_rassvet',
               'ферма': '/t_ferma', 'торт': '/t_tortuga', 'тортуга': '/t_tortuga', 'мышь': '/t_night',
               'мыш': '/t_night', 'ночной': '/t_night'}
    for line in txt:
        for ga_move in targets:
            if ga_move in line:
                code = re.search(r'{}(\S+)'.format(ga_move), line).group(1)
                loc = mes.db.check('SELECT name, lvl FROM loc WHERE code = ?', [code])
                url = f'/{ga_move}{code}'
                x = '⚔' if 'atk' in ga_move else '🛡'
                if loc:
                    line = line.replace(url, m.format(url, x, loc[0], ' lvl.{}'.format(loc[1]) if loc[1] != 99 else ''))
                else:
                    line = line.replace(url, m.format(url, x, url, ''))
        if 'тактика' in line:
            parse = re.search(r'тактика (\S+)', line).group(1)
            tact = tactics.get(parse, 'ERROR')
            if tact != 'ERROR':
                txt = 'тактика ' + parse
                line = line.replace(txt, m.format(tact, txt, '', ''))

        answer += line + '\n'
        mes.db.query('UPDATE settings SET info = ? WHERE name = "al_pin_temp"', [answer])
    await mes.answer(answer, reply_markup=ReplyKeyboard('✅', '❌'))
    await battle_states.al_order.set()


async def pin_confirm(mes: Message, state: FSMContext):
    message = mes.db.check('SELECT info FROM settings WHERE name = "al_pin_temp"', [])[0]
    mes.db.query('UPDATE settings SET info = ? WHERE name = "al_pin_pub"', [message])
    message = message + '\nОтметились:'
    mes.db.query('UPDATE settings SET info = ? WHERE name = "al_pin"', [message])
    chats = mes.db.checkall('SELECT id FROM chats WHERE ntf_pin = 1')
    mid_dict = {}
    rand_int = str(random.randint(1000, 9999))
    mes.db.query('UPDATE settings SET info = ? WHERE name = "al_pin_num"', [rand_int])
    for chat in chats:
        try:
            x = await bot.send_message(chat[0], message, reply_markup=pub_pin_keyboard(f'pub_pin:{rand_int}'), disable_web_page_preview=True)
            await bot.pin_chat_message(chat[0], x.message_id)
            mid_dict[x.chat.id] = x.message_id
        except:
            pass
    if mid_dict:
        mid = json.dumps(mid_dict)
        mes.db.query('UPDATE settings SET info = ? WHERE name = "al_pin_mes_id"', [mid])

    news = mes.db.check('SELECT info FROM settings WHERE name = "news"', [])[0]
    await mes.answer(START_MAIN_MENU_TEXT.format(random.choice(START_HEADER_TEXT), news), reply_markup=start_menu)
    await state.finish()