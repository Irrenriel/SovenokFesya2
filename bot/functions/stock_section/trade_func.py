from aiogram.types import Message
import time, random, re

from bin.config import CW_BOT_ID
from bin.main_var import main_client
from bin.cash_var import users_cash as uc

from bot.content import TRADE_ANSWER_TEXT


async def trade(mes: Message):
    #journal_log(mes)
    if mes.chat.type != 'private':
        return
    if not uc.select(**{'id': mes.from_user.id, 'guild_tag': 'AT'}):
        await mes.answer('Доступ запрещён.')
        return

    load = await mes.answer('Запрашиваю, подожди./⏳')
    await load.edit_text('Запрашиваю, подожди../⌛')
    await load.edit_text('Запрашиваю, подожди.../⏳')

    res = uc.select_id(mes.from_user.id).get('trade')
    if not res:
        await load.edit_text(TRADE_ANSWER_TEXT.format('Пусто'))
        return

    herb_text = ''
    herb_list = res.split(' ')
    await main_client.connect()
    for el in herb_list:
        async with main_client.conversation(CW_BOT_ID) as conv:
            time.sleep(float(str(random.uniform(1, 2))[0:4]))
            await conv.send_message('/t_' + str(el))
            answer = await conv.get_response()
        try:
            cost = re.search(r'шт. по (\d+)', answer.message).group(1)
            name = re.search(r'Предложения (\D+) сейчас:', answer.message).group(1)
        except:
            x = 'В правилах введён недоступный ресурс.\nПожалуйста поменяйте правило через /gs id, либо обратитесь к @Irrenriel.'
            await load.edit_text(x)
            return

        herb_text += f'<code>{el}</code> | {name} | <a href="https://t.me/share/url?url=/wtb_{el}">{cost}💰</a>\n'
    await main_client.disconnect()
    await load.edit_text(TRADE_ANSWER_TEXT.format(herb_text))


async def gs(mes: Message):
    #journal_log(mes)
    if mes.chat.type != 'private':
        return
    if not uc.select(**{'id': mes.from_user.id, 'guild_tag': 'AT'}):
        await mes.answer('Доступ запрещён.')
        return
    if len(mes.text) < 5:
        await mes.answer('/gs [id] [id] [id] ...')
        return

    if len(mes.text) == 5 and mes.text[4:].startswith('0'):
        mes.db.query('UPDATE users SET trade = ? WHERE id = ?', ['', mes.from_user.id])
        await mes.answer('Правила очищены!')
    else:
        mes.db.query('UPDATE users SET trade = ? WHERE id = ?', [mes.text[4:], mes.from_user.id])
        await mes.answer('Правила установлены!')
    uc.loading()