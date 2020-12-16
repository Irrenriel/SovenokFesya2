from aiogram.dispatcher import FSMContext
from aiogram.types import Message
import random, asyncio, re
from datetime import datetime, timedelta

from bin.cash_var import users_cash as uc
from bin.config import CW_BOT_ID, ADMIN, GUILD_MASTER
from bin.main_var import main_client

from bot.content import START_MAIN_MENU_TEXT, START_HEADER_TEXT, START_INVITE_TEXT, HERO_PARSE, CASTLE_EMBLEMS
from bot.states import start_states
from bot.keyboards import start_menu, pub_pin_keyboard

# /start
async def start_func(mes: Message, state: FSMContext):
    #await journal_log(mes)
    if mes.chat.type != 'private':
        return
    if uc.select_id(mes.from_user.id):
    # if already registered
        news = mes.db.check('SELECT info FROM settings WHERE name = "news"', [])[0]
        await mes.answer(START_MAIN_MENU_TEXT.format(random.choice(START_HEADER_TEXT), news), reply_markup=start_menu)
        await state.finish()
    else:
        for el in START_INVITE_TEXT:
            await mes.answer(el)
            await asyncio.sleep(0.5)
        await start_states.Q1.set()


async def start_q1(mes: Message, state: FSMContext):
    #await journal_log(mes)
    if mes.chat.type != 'private':
        return
    if mes.forward_from is None or mes.forward_from.id != CW_BOT_ID or "🎉Достижения: /ach" not in mes.text:
        await mes.answer('Требуется переслать /hero из @ChatWarsBot!')
        return
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Этому /hero больше 30 секунд. Пришли новый!')
        return
    await hero_analyz(mes)

    # All is OK
    await mes.answer('Хорошо, всё в порядке. Добро пожаловать, {}!'.format(mes.from_user.username))
    news = mes.db.check('SELECT info FROM settings WHERE name = "news"', [])[0]
    await mes.answer(START_MAIN_MENU_TEXT.format(random.choice(START_HEADER_TEXT), news), reply_markup=start_menu)
    await state.finish()


async def hero_refresh(mes: Message):
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Этому /hero больше 30 секунд. Пришли новый!')
        return

    await hero_analyz(mes)
    await mes.answer('Информация успешно обновлена!')


async def hero_analyz(mes: Message):
    # Сбор данных
    parse = re.search(HERO_PARSE, mes.text)
    for emblem in list(CASTLE_EMBLEMS):
        if parse.group('castle') == emblem:
            castle = CASTLE_EMBLEMS.get(emblem)
            break
        else:
            castle = 'ERROR'

    if uc.select_id(mes.from_user.id):
        mes.db.query('UPDATE users SET username = ?, nickname = ?, lvl = ?, class = ?, guild_tag = ?, castle = ? WHERE id = ?',
                     [mes.from_user.username, parse.group('nickname'), int(parse.group('lvl')),
                      parse.group('class'), parse.group('guild_tag'), castle, mes.from_user.id])
    else:
        mes.db.query('INSERT INTO users (id, username, nickname, lvl, class, guild_tag, castle) values (?,?,?,?,?,?,?)',
                     [mes.from_user.id, mes.from_user.username, parse.group('nickname'), parse.group('lvl'),
                      parse.group('class'), parse.group('guild_tag'), castle])

    # Автоназначение Командира и Админа по умолчанию
    if mes.chat.id == ADMIN:
        mes.db.query('UPDATE users SET role = 2 WHERE id = ?', [ADMIN])
    elif mes.chat.id == GUILD_MASTER:
        mes.db.query('UPDATE users SET role = 3 WHERE id = ?', [GUILD_MASTER])

    # Update cash
    uc.loading()

