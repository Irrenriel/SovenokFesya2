from aiogram.types import Message
from aiogram.types import CallbackQuery

from bot.keyboards.inline_keyboard import InlineKeyboard


async def journal(mes: Message):
    if mes.text == '/j':
        res = mes.db.checkall('SELECT id, time, username, txt FROM journal ORDER BY time DESC LIMIT 15', [])
        txt = '<b>Журнал действий: Общий</b>\n'
    else:
        user = mes.text[3:]
        res = mes.db.checkall('SELECT id, time, username, txt FROM journal WHERE username = ? ORDER BY time DESC LIMIT 15', [user])
        txt = f'<b>Журнал действий: @{user}</b>\n'

    if not res:
        txt += 'История пуста, либо данного пользователя нет.'
        await mes.answer(txt)
        return

    notes = len(res)
    for element in res:
        txt += f'[<i>{element[1]}</i>] @{element[2]}: "{element[3]}"\n'
    page = 1
    arg = 'all' if user is None else user
    keyboard = [('<', f'j_page:{arg}:{page - 1}'), (str(page), f'j_page:{arg}:{page}'), ('>', f'j_page:{arg}:{page+1}'),
                ('Закрыть', 'j_cancel')]
    await mes.answer(txt, reply_markup=await InlineKeyboard(keyboard))


async def journal_pages(call: CallbackQuery):
    await call.answer(cache_time=1)
    if call.data.split(':')[1] == 'all':
        res = call.db.checkall('SELECT id, time, username, txt FROM journal ORDER BY time DESC', [])
        txt = '<b>Журнал действий: Общий</b>\n'
    else:
        user = call.data.split(':')[1]
        res = call.db.checkall('SELECT id, time, username, txt FROM journal WHERE username = ? ORDER BY time DESC', [user])
        txt = f'<b>Журнал действий: @{user}</b>\n'

    notes = len(res)
    n = int(call.data[11:]) * 15
    if res[n-15:n]:
        for element in res[n-15:n]:
            txt += f'[<i>{element[1]}</i>] @{element[2]}: "{element[3]}"\n'
    else:
        txt += 'История пуста, либо данного пользователя нет.'
    pages = list(range(int(notes / 15) + 2))[1:]
    if (notes % 15) == 0:
        pages = pages[:-1]
    if len(pages) > 1:
        j_keyboard = InlineKeyboardMarkup(row_width=5)
        for page in pages:
            if call.data[7:].startswith('all'):
                j_keyboard.insert(InlineKeyboardButton(str(page), callback_data='j_page:all:' + str(page)))
            else:
                j_keyboard.insert(InlineKeyboardButton(str(page), callback_data='j_page:'+ user +':' + str(page)))
        j_keyboard.add(InlineKeyboardButton('Закрыть', callback_data='cancel'))
        await call.message.edit_text(txt, reply_markup=j_keyboard)
    else:
        await call.message.edit_text(txt)