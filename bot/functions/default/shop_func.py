from aiogram.types import Message
import time, random, re

from bin.cash_var import users_cash as uc
from bin.main_var import main_client
from bin.config import CW_BOT_ID

from bot.content import GOLD_TEXT


# /open_shop
async def open_shop(mes: Message):
    #journal_log(mes)
    if not uc.select(**{'id': mes.from_user.id, 'guild_tag': 'AT'}):
        await mes.answer('Доступ запрещён.')
        return

    load = await mes.answer('Попробую открыть, подожди./⏳')
    await load.edit_text('Попробую открыть, подожди../⌛')
    await load.edit_text('Попробую открыть, подожди.../⏳')

    await main_client.connect()
    async with main_client.conversation(CW_BOT_ID) as conv:
        time.sleep(float(str(random.uniform(1, 3))[0:4]))
        await conv.send_message('/myshop_open')
        answer = await conv.get_response()
    await main_client.disconnect()

    if "It's OPEN now." in answer.message:
        txt = 'Попробую открыть, подожди.../⏳\nУспех! Заходи!'
    else:
        txt = 'Попробую открыть, подожди.../⏳\nПровал! Подожди около 5 минут...'
    await load.edit_text(txt)


# /gold
async def gold(mes: Message):
    #journal_log(mes)
    if not uc.select(**{'id': mes.from_user.id, 'guild_tag': 'AT'}):
        await mes.answer('Доступ запрещён.')
        return

    load = await mes.answer('Запрашиваю, подожди./⏳')
    await load.edit_text('Запрашиваю, подожди../⌛')
    await load.edit_text('Запрашиваю, подожди.../⏳')

    await main_client.connect()
    conv_answer_list = {}
    async with main_client.conversation(CW_BOT_ID) as conv:
        for i, req in enumerate(['/ws_MYdnt', '/ws_MYdnt_stand']):
            time.sleep(float(str(random.uniform(1, 3))[0:4]))
            await conv.send_message(req)
            conv_answer_list[str(i)] = await conv.get_response()
    await main_client.disconnect()

    mana = re.search(r'\w*/\w+', conv_answer_list.get('0').message).group(0)
    cost = re.search(r'Steel mold, 15💧 (\d+)', conv_answer_list.get('1').message).group(1)
    rand_price = str(random.randint(1, 999))
    open = 'Открыто✅' if 'Studio is открыто.' in conv_answer_list.get('0').message else 'Закрыто🚫'

    await load.edit_text(GOLD_TEXT.format(cost, rand_price, open, mana))


# /change_cost
async def change_cost(mes: Message):
    #journal_log(mes)
    if not uc.select(**{'id': mes.from_user.id, 'guild_tag': 'AT'}):
        await mes.answer('Доступ запрещён.')
        return

    load = await mes.answer('Меняю цену, подожди./⏳')
    await load.edit_text('Меняю цену, подожди../⌛')
    await load.edit_text('Меняю цену, подожди.../⏳')

    cc = re.search(r'(\d+)', mes.text[4:]).group(1)

    if not 1 < int(cc) < 1000:
        await load.edit_text('Недоступная цена.')
        return

    await main_client.connect()
    async with main_client.conversation(CW_BOT_ID) as conv:
        time.sleep(float(str(random.uniform(1, 3))[0:4]))
        await conv.send_message('/s_695_add 27 ' + cc)
        cc_report = await conv.get_response()
    await main_client.disconnect()

    if 'Steel mold, 15💧 {}💰'.format(cc) in cc_report.message:
        txt = 'Меняю цену, подожди.../⌛\nУспех! Установленная цена {}💰!'.format(cc)
    else:
        txt = 'Меняю цену, подожди.../⌛\nПровал! Что-то не так.'

    await load.edit_text(txt)