from aiogram.types import Message
import time, random, datetime, asyncio

from bin.config import CW_BOT_ID, ADMIN
from bin.main_var import main_client, bot
from bin.cash_var import users_cash as uc

from bot.content import LOC_TYPES


async def loc_check_f(mes: Message):
    #journal_log(mes)
    if not uc.check_perm_role(mes.from_user.id, [2, 3, 4]):
        await mes.answer('Доступ запрещён.')
        return

    if mes.from_user.id != ADMIN:
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d-%H-%M-%S')
        last_update = mes.db.check('SELECT info FROM settings WHERE name = "last_l_check_datetime"')

        if last_update and last_update[0]:
            lu = last_update[0].split('-')
            td = datetime.timedelta(hours=7, minutes=59)
            lu_date = datetime.datetime(year=int(lu[0]), month=int(lu[1]), day=int(lu[2]),
                                        hour=int(lu[3]), minute=int(lu[4]), second=int(lu[5]))

            if now - lu_date < td:
                l = await mes.answer(f'Не доступно! Запрещено до {lu_date + td}.\nДля экстренной проверки обратитесь к @Irrenriel.')
                await asyncio.sleep(2)
                await mes.delete()
                await asyncio.sleep(3)
                await l.delete()
                return
            else:
                mes.db.query('UPDATE settings SET info = ? WHERE name = "last_l_check_datetime"', [now_str])
        else:
            mes.db.query('UPDATE settings SET info = ? WHERE name = "last_l_check_datetime"', [now_str])

    await mes.answer('Выполняется, жди...')
    err = "Strange fog is so dense that you can't reach this place."
    text = 'Истёкшие локации!\n\n'
    req = 'SELECT code FROM loc WHERE lvl != 99' if mes.text.startswith('/l_chk') else 'SELECT code FROM loc'
    locs = mes.db.checkall(req)
    result = []

    await main_client.connect()
    for loc in locs:
        if loc[0].startswith('NoneCode'):
            continue
        async with main_client.conversation(CW_BOT_ID) as conv:
            time.sleep(float(str(random.uniform(1, 3))[0:4]))
            await conv.send_message('/ga_atk_' + loc[0])
            ga_atk_answer = await conv.get_response()

            if ga_atk_answer.message == 'Ты сейчас занят другим приключением. Попробуй позже.' or 'Ветер завывает по окрестным лугам, замки как будто вымерли. Это воины зашивают раны и латают доспехи после тяжелой битвы. Ближайшие несколько минут все учреждения и ворота замка закрыты. Жди сводки с полей в @ChatWarsDigest.':
                await mes.answer('Мы сейчас заняты другим приключением. Попробуйте позже.')
                return

            if ga_atk_answer.message == err:
                time.sleep(float(str(random.uniform(1, 3))[0:4]))
                await conv.send_message('/ga_def_' + loc[0])
                ga_def_answer = await conv.get_response()

        if ga_atk_answer.message == err and ga_def_answer.message == err:
            req = mes.db.check('SELECT name, lvl, code FROM loc WHERE code = ?', [loc[0]])
            answer = LOC_TYPES.get(req[0].split(' ')[-1], '🎪 ') + req[0] + (
                "" if req[1] == 99 else " lvl. " + str(req[1]))
            result.append('<b>{}</b>\n  └ <code>{}</code>'.format(answer, req[2]))
            mes.db.query('DELETE FROM loc WHERE code = ?', [loc[0]])
            mes.db.query('DELETE FROM loc_buff_info WHERE code = ?', [loc[0]])
            if not mes.text.startswith('/l_chk'):
                mes.db.query('DELETE FROM al_guild_info WHERE code = ?', [loc[0]])

    chats = mes.db.checkall('SELECT id FROM chats WHERE delete_loc_ntf = 1', [])
    if not chats and not result:
        await mes.answer('Done!')
        return
    for chat in chats:
        try:
            await bot.send_message(chat[0], text + '\n\n'.join(result))
        except:
            pass
        await asyncio.sleep(0.3)
    await mes.answer('Done!')
    mes.db.query('UPDATE settings SET info = ? WHERE name = "last_l_check"',
                 [str(datetime.datetime.today().strftime('%d.%m.%Y %H:%M'))])

    async with main_client.conversation(CW_BOT_ID) as conv:
        time.sleep(float(str(random.uniform(1, 3))[0:4]))
        await conv.send_message('/myshop_open')
    await main_client.disconnect()