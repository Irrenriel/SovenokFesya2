from aiogram.types import CallbackQuery
from aiogram.types import Message

from bin.cash_var import users_cash as uc

from bot.keyboards import settings_keyboard
from bot.content import SETTINGS_TEXT, HELP_NEW_CHAT_ID_TEXT


async def new_chat_id(mes: Message):
    if mes.chat.type != 'supergroup':
        return
    if mes.db.check('SELECT * FROM chats WHERE id = ?', [mes.chat.id]):
        return

    mes.db.query('INSERT INTO chats (id) VALUES (?)', [mes.chat.id])
    await mes.answer(HELP_NEW_CHAT_ID_TEXT)


async def settings(mes: Message):
    if mes.chat.type != 'supergroup':
        return
    if not mes.db.check('SELECT * FROM chats WHERE id = ?', [mes.chat.id]):
        await mes.answer('Данного чата нет в базе. Пригласите бота по новой в чат или обратитесь к @Irrenriel.')
        return
    if not uc.check_perm_role(mes.from_user.id, [2, 3, 4]):
        await mes.answer('Доступ запрещён.')
        return

    d = {0: 'Откл❌', 1: 'Вкл✅'}
    result = mes.db.check('SELECT delete_loc_ntf, new_loc_ntf, brief, brief_mode FROM chats WHERE id = ?', [mes.chat.id])
    answer = SETTINGS_TEXT.format(d.get(result[0]), d.get(result[1]), d.get(result[2]), d.get(result[3]))
    await mes.answer(answer, reply_markup=settings_keyboard(result))


async def settings_v(call: CallbackQuery):
    await call.answer(cache_time=2)
    if not call.db.check('SELECT * FROM users WHERE id = ?', [call.from_user.id]) or not uc.check_perm_role(call.from_user.id, [2, 3, 4]):
        await call.answer('Доступ запрещён.')
        return

    c = {'dln:on': ['delete_loc_ntf', True],
         'dln:off': ['delete_loc_ntf', False],
         'nln:on': ['new_loc_ntf', True],
         'nln:off': ['new_loc_ntf', False],
         'brf:on': ['brief', True],
         'brf:off': ['brief', False],
         'brfm:on': ['brief_mode', True],
         'brfm:off': ['brief_mode', False]}
    call.db.query('UPDATE chats SET {} = ? WHERE id = ?'.format(c.get(call.data)[0]), [c.get(call.data)[1], call.message.chat.id])

    d = {0: 'Откл❌', 1: 'Вкл✅'}
    result = call.db.check('SELECT delete_loc_ntf, new_loc_ntf, brief, brief_mode FROM chats WHERE id = ?', [call.message.chat.id])
    answer = SETTINGS_TEXT.format(d.get(result[0]), d.get(result[1]), d.get(result[2]), d.get(result[3]))
    await call.message.edit_text(answer, reply_markup=settings_keyboard(result))