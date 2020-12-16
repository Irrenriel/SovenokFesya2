from aiogram.types import CallbackQuery
from aiogram.types import Message
import time, re

from bin.config import CW_BOT_ID
from bin.main_var import main_client, bot

from bot.states.default_states import craft_states
from bot.keyboards import stock_keyboard, crafting_keyboard, ntf_craft_keyboard, interface_menu, \
    interface_castle_menu, int_menu, interface_inv_menu


class GuildStock:
    guild_pool = {}
    guild_res_pool = {}
    guild_parts_pool = {}
    guild_rec_pool = {}
    def pools_input(self, sr: list):
        stock_res = sr[0].split('\n')[1:]
        stock_parts = sr[1].split('\n')[1:]
        stock_rec = sr[2].split('\n')[1:]

        # Resourses
        for el in stock_res:
            l = re.search(r'(\d+) (\D+) x (\d+)', el)
            self.guild_res_pool[l.group(1)] = [l.group(2), l.group(3)]
            self.guild_pool[l.group(1)] = [l.group(2), l.group(3)]

        # Parts
        for el in stock_parts:
            l = re.search(r'(k\d+) (\D+) x (\d+)', el)
            if not l:
                continue
            self.guild_parts_pool[l.group(1)] = [l.group(2), l.group(3)]
            self.guild_pool[l.group(1)] = [l.group(2), l.group(3)]

        # Recipes
        for el in stock_rec:
            l = re.search(r'(r\d+) (\D+) x (\d+)', el)
            if not l:
                continue
            self.guild_rec_pool[l.group(1)] = [l.group(2), l.group(3)]
            self.guild_pool[l.group(1)] = [l.group(2), l.group(3)]

guild_stock = GuildStock()

# 📦Обновить сток гильдии
async def guild_stock_refresh(mes: Message):
    #journal_log(mes)
    if mes.chat.type != 'private':
        return

    load = await mes.answer('Запрашиваю, подожди./⏳')
    await load.edit_text('Запрашиваю, подожди../⌛')
    await load.edit_text('Запрашиваю, подожди.../⏳')

    stock_result = []
    await main_client.connect()
    async with main_client.conversation(CW_BOT_ID) as conv:
        for x in ['/g_stock_res', '/g_stock_parts', '/g_stock_rec']:
            await conv.send_message(x)
            y = await conv.get_response()
            stock_result.append(y.message)
            time.sleep(1)
    await main_client.disconnect()

    guild_stock.pools_input(stock_result)
    guild_res_pool = guild_stock.guild_res_pool
    text = '<b>Сток гильдии обновлён!</b>'
    for key in guild_res_pool:
        text += f'\n<code>{key}</code> {guild_res_pool[key][0]} x {guild_res_pool[key][1]}'
    await load.edit_text(text, reply_markup=stock_keyboard)


# ⚒Irrenriel
async def irren_interface(mes: Message):
    if mes.chat.type != 'private':
        return

    await main_client.connect()
    async with main_client.conversation(CW_BOT_ID) as conv:
        await conv.send_message('🏅Герой')
        answer = await conv.get_response()
    await main_client.disconnect()

    await mes.answer(f'<b>CW:</b>\n{answer.message}', reply_markup=interface_menu)
    await craft_states.Q2.set()


async def irren_interface_adv(mes: Message):
    if mes.chat.type != 'private':
        return
    move_keyboard_dict = {'🏅Герой': interface_menu, '🏰Замок': interface_castle_menu,
                          '🛎Аукцион': interface_castle_menu, '⚖️Биржа': interface_castle_menu,
                          '/inv': interface_inv_menu}
    keyboard = move_keyboard_dict.get(mes.text, int_menu)

    await main_client.connect()
    async with main_client.conversation(CW_BOT_ID) as conv:
        await conv.send_message(mes.text)
        answer = await conv.get_response()
    await main_client.disconnect()

    await mes.answer('<b>CW:</b>\n' + answer.message, reply_markup=keyboard)


# /g_receive | /g_deposit
async def g_receive_and_deposit(mes: Message):
    if mes.chat.type != 'private':
        return

    await main_client.connect()
    async with main_client.conversation(CW_BOT_ID) as conv:
        await conv.send_message(mes.text)
        answer = await conv.get_response()
    await mes.answer('<b>CW:</b>\n' + answer.message)
    await main_client.disconnect()


# /c_id
async def crafting(mes: Message):
    if mes.chat.type != 'private':
        return
    try:
        await main_client.connect()
        async with main_client.conversation(CW_BOT_ID) as conv:
            await conv.send_message(mes.text)
            answer = await conv.get_response()
        await main_client.disconnect()

        if 'Не хватает материалов для крафта' in answer.message:
            f_list = {}
            for string in answer.message.splitlines():
                parse = re.search(r'(\d+) x ([^\n$]+)', string)
                if parse is None: continue
                count = int(parse.group(1))
                name = parse.group(2)
                f_list[name] = count
            res = "select * from craft where Name in ('{}')"
            res_q = res.format("', '".join(f_list.keys()))
            res_r = mes.db.checkall(res_q, [])
            r_text = '<b>Запрос:</b>\n'
            s_text = '/g_withdraw'

            guild_pool = guild_stock.guild_pool
            guild_res_pool = guild_stock.guild_res_pool

            for item in res_r:
                try:
                    if int(f_list.get(item[1])) <= int(guild_pool.get(item[0])[1]):
                        r_text += f'✅ <code>{item[0]}</code> {item[1]} x {f_list.get(item[1])}\n'
                    else:
                        r_text += f'❌ <code>{item[0]}</code> {item[1]} x {guild_res_pool.get(item[0])[1]}/{f_list.get(item[1])}\n'
                except:
                    r_text += f'❌ <code>{item[0]}</code> {item[1]} x 0/{f_list.get(item[1])}\n'
                s_text += f' {item[0]} {f_list.get(item[1])}'

            mes.db.query('UPDATE settings SET info = ? WHERE name = "last_craft"', [r_text])
            mes.db.query('UPDATE settings SET info = ? WHERE name = "last_craft_url"', [s_text])
            await mes.answer(f'<b>CW:</b>\n{answer.message}\n\n{r_text}', reply_markup=crafting_keyboard(s_text))
        else:
            await mes.answer(f'<b>CW:</b>\n{answer.message}')

    except:
        await mes.answer('<b>Обновите сток гильдии, пожалуйста!</b>\n')


async def ntf_craft(call: CallbackQuery):
    text = call.db.check('SELECT info FROM settings WHERE name = "last_craft"', [])[0]
    url = call.db.check('SELECT info FROM settings WHERE name = "last_craft_url"', [])[0]
    chats_id = call.db.checkall('SELECT id FROM chats WHERE ntf_craft = 1', [])
    if chats_id:
        for chat_id in chats_id:
            try:
                await bot.send_message(chat_id[0], f'{text}\n@LaChaton @Lex13_q @Laniakeo',
                                       reply_markup=ntf_craft_keyboard(url))
            except:
                pass


# /res_add
async def res_add(mes: Message):
    if mes.chat.type != 'private':
        return
    if len(mes.text) < 10:
        await mes.answer('Недостаточно аргументов.\nПример: /res_add [id] [name]')
        return

    parse = re.search(r'/res_add (\S+) ([^\n$]+)', mes.text)
    if not parse:
        await mes.answer('Недостаточно аргументов.\nПример: /res_add [id] [name]')
        return
    if mes.db.check('SELECT * FROM craft WHERE id = ?', [parse.group(1)]):
        await mes.answer('Данный ресурс уже есть в базе.')
        return

    mes.db.query('insert into craft (id, name) values (?, ?)', [parse.group(1), parse.group(2)])
    await mes.answer('Ресурс <b>{}</b> c ID <code>{}</code> был успешно добавлен в базу!'.format(parse.group(2),
                                                                                                 parse.group(1)))


# /res_edit
async def res_edit(mes: Message):
    if mes.chat.type != 'private':
        return
    if len(mes.text) < 11:
        await mes.answer('Недостаточно аргументов.\nПример: /res_edit [id] [new_id] [new_name]')
        return

    parse = re.search(r'/res_edit (\S+) (\S+) ([^\n$]+)', mes.text)
    if not parse:
        await mes.answer('Недостаточно аргументов.\nПример: /res_edit [id] [new_id] [new_name]')
        return
    if not mes.db.check('SELECT * FROM craft WHERE id = ?', [parse.group(1)]):
        await mes.answer('Данного ресурса нет в базе.')
        return

    mes.db.query('UPDATE craft SET id = ?, name = ? WHERE id = ?', [parse.group(2), parse.group(3), parse.group(1)])
    await mes.answer('Обновлён ресурс <b>{}</b> c ID <code>{}</code>!'.format(parse.group(3),parse.group(2)))

async def inline_stock(call: CallbackQuery):
    await call.answer(cache_time=2)
    text = '<b>Сток гильдии обновлён!</b>'

    if call.data[6:] == 'res':
        guild_res_pool = guild_stock.guild_res_pool
        for key in guild_res_pool:
            text += '\n<code>' + str(key) + '</code> ' + str(guild_res_pool[key][0]) + ' x ' + str(guild_res_pool[key][1])
    elif call.data[6:] == 'parts':
        guild_parts_pool = guild_stock.guild_parts_pool
        for key in guild_parts_pool:
            text += '\n<code>' + str(key) + '</code> ' + str(guild_parts_pool[key][0]) + ' x ' + str(guild_parts_pool[key][1])
    elif call.data[6:] == 'rec':
        guild_rec_pool = guild_stock.guild_rec_pool
        for key in guild_rec_pool:
            text += '\n<code>' + str(key) + '</code> ' + str(guild_rec_pool[key][0]) + ' x ' + str(guild_rec_pool[key][1])

    await call.message.edit_text(text, reply_markup=stock_keyboard)