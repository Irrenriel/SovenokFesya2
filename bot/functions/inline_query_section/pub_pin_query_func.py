from aiogram.types import InlineQuery, InlineQueryResultArticle, InputMessageContent, InputTextMessageContent
import json, asyncio

from bin.main_var import bot
from bin.cash_var import users_cash as uc

from bot.content import CASTLE_EMBLEMS_AROUND
from bot.keyboards import pub_pin_keyboard


async def pub_pinnn(query: InlineQuery):
    pin_id = query.db.check('SELECT info FROM settings WHERE name = "al_pin_num"')[0]
    data_pid = query.query[8:]
    if pin_id != data_pid:
        return

    user = uc.select_id(query.from_user.id)
    if user:
        guild_tag = user.get('guild_tag')
        castle = CASTLE_EMBLEMS_AROUND.get(user.get('castle'))
        d = f'🔹{castle}[{guild_tag}]'
        pin_order = query.db.check('SELECT info FROM settings WHERE name = "al_pin"')[0]

        if d not in pin_order:
            pin_order = pin_order + '\n' + d
            query.db.query('UPDATE settings SET info = ? WHERE name = "al_pin"', [pin_order])

            x = query.db.check('SELECT info FROM settings WHERE name = "al_pin_mes_id"')[0]
            al_pin_mid_dict = json.loads(x)
            keyboard = pub_pin_keyboard(f'pub_pin:{data_pid}')
            for mid in al_pin_mid_dict.items():
                try:
                    await bot.edit_message_text(pin_order, int(mid[0]), int(mid[1]), reply_markup=keyboard)
                    await asyncio.sleep(0.3)
                except:
                    pass

    txt = query.db.check('SELECT info FROM settings WHERE name = "al_pin_pub"')[0]
    results = []
    results.append(InlineQueryResultArticle(
        id='1',
        title='📯Приказ',
        description='Опубликовать приказ',
        input_message_content=InputTextMessageContent(message_text=txt)
    ))
    await query.answer(results=results, cache_time=1, is_personal=True)