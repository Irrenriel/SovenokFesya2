from aiogram import executor, filters
from bin.main_var import dp, loop
import logging

from bin.config import CW_BOT_ID, ADMIN
from bin.cash_var import users_cash as uc
from bot.states import start_states, craft_states, battle_states
from bot.functions import *


# Logging
#logging.basicConfig(level=logging.DEBUG, filename='error.log', filemode='w')


# Handlers
'''<<<-----   ADMIN   ----->>>'''
# /sql
dp.register_message_handler(sql, commands=['sql'])

# /inf
dp.register_message_handler(info, commands=['inf'])

# /reg_as
dp.register_message_handler(reg_as, commands=['reg_as'])

# Mana drink
dp.register_message_handler(mana_start, commands=['mana_start'])
dp.register_message_handler(mana_stop, commands=['mana_stop'])

# /j
#dp.register_message_handler(journal_func.journal, commands=['j'])

# Закрыть Инлайн Клавиатуру
dp.register_callback_query_handler(callback_cancel, lambda c: c.from_user.id == ADMIN, text='j_cancel')
dp.register_callback_query_handler(callback_cancel, lambda c: uc.check_perm_role(c.from_user.id, [2, 3, 4]),text='s_cancel')

# New chat id
dp.register_message_handler(new_chat_id, content_types='new_chat_members')

# /settings
dp.register_message_handler(settings_func.settings, commands=['settings'])
dp.register_callback_query_handler(settings_func.settings_v,
								   text=['dln:on', 'dln:off', 'nln:on', 'nln:off', 'brf:on', 'brf:off', 'brfm:on', 'brfm:off'])
'''------------------------------------------------------------------------------------------------------------------'''

'''<<<-----   DEFAULT   ----->>>'''
# /start | 🏛Холл | Вернуться↩
dp.register_message_handler(start_func, commands=['start'])
dp.register_message_handler(start_func, filters.Text(equals=['🏛Холл', 'Вернуться↩'], ignore_case=True), state='*')
dp.register_message_handler(start_q1, state=start_states.Q1)

# /say | /news
dp.register_message_handler(say, commands=['say'])
dp.register_message_handler(news, commands=['news'])

# ⚙Другое | 🍺Таверна
dp.register_message_handler(sections, lambda c: c.text in ['⚙Другое', '🍺Таверна'] and c.chat.type == 'private')

# 🏛Штаб [AT]
dp.register_message_handler(sections, lambda c: c.text == '🏛Штаб [AT]' and c.chat.type == 'private')

# /hero
dp.register_message_handler(hero_refresh, lambda c: "🎉Достижения: /ach" in c.text and c.forward_from.id == CW_BOT_ID)

# Закрыть Инлайн Клавиатуру
dp.register_callback_query_handler(callback_cancel, text='cancel')

# Shop trigger
dp.register_message_handler(open_shop, commands=['open_shop'])
dp.register_message_handler(gold, commands=['gold'])
dp.register_message_handler(change_cost, filters.RegexpCommandsFilter(regexp_commands=['cc_[0-9]+']))

# /top
dp.register_message_handler(top, commands=['top'])
'''------------------------------------------------------------------------------------------------------------------'''

'''<<<-----   🗺LOCATION SECTION   ----->>>'''
# New Location Input
dp.register_message_handler(new_loc, lambda c:
"То remember the route you associated it with simple combination:" in c.text and c.forward_from.id == CW_BOT_ID)

# Delete Location from Database
dp.register_message_handler(loc_del, commands=['l_del'])

# /l_list
dp.register_message_handler(loc_list, commands=['l_list'])
dp.register_callback_query_handler(loc_type, text=['loc_type_ruins', 'loc_type_mines', 'loc_type_forts',
												   'loc_type_al', 'loc_type_cap'])

# /l_check
dp.register_message_handler(loc_check_f, commands=['l_check', 'l_chk'])

# /l_info
dp.register_message_handler(loc_info, commands=['l_info'])
dp.register_message_handler(new_loc_info, lambda c: "attractions:" in c.text and c.forward_from.id == CW_BOT_ID)

# /l_history
dp.register_message_handler(l_history, commands=['l_history'])

# /l_capture
dp.register_message_handler(l_capture, commands=['l_capture'])

# /l_miss
dp.register_message_handler(loc_miss, commands=['l_miss'])
'''------------------------------------------------------------------------------------------------------------------'''

'''<<<-----   💠OTHER SECTION   ----->>>'''
# 💠Патчноут
dp.register_message_handler(patchnote_func.patchnote, filters.Text(equals='💠Патчноут', ignore_case=True))
dp.register_callback_query_handler(patchnote_func.patchnote_v, text=['v10', 'v11', 'v12', 'v13', 'v133', 'v14', 'v20', 'v21'])

# ℹПомощь
dp.register_message_handler(help, filters.Text(equals='ℹПомощь', ignore_case=True))
'''------------------------------------------------------------------------------------------------------------------'''

'''<<<-----   📦STOCK SECTION   ----->>>'''
# ⚒Мастерская
dp.register_message_handler(craft, filters.Text(equals='⚒Мастерская', ignore_case=True))
dp.register_callback_query_handler(craft_func.inline_stock, text_contains='craft:', state=craft_states.Q1)

# /res_add
dp.register_message_handler(craft_func.res_add, commands=['res_add'], state=craft_states.Q1)

# /res_edit
dp.register_message_handler(craft_func.res_edit, commands=['res_edit'], state=craft_states.Q1)

# 📦Обновить сток гильдии
dp.register_message_handler(guild_stock_refresh, filters.Text(equals='📦Обновить сток гильдии', ignore_case=True),
                            state=craft_states.Q1)

# ⚒Irrenriel
dp.register_message_handler(irren_interface, filters.Text(equals='⚒Irrenriel', ignore_case=True), state=craft_states.Q1)
dp.register_message_handler(craft, filters.Text(equals='⚒Вернуться к верстаку', ignore_case=True), state=craft_states.Q2)
dp.register_message_handler(irren_interface_adv, state=craft_states.Q2)

# /c_id
dp.register_message_handler(crafting, filters.RegexpCommandsFilter(regexp_commands=['c_.+']), state=craft_states.Q1)

# Notification craft
dp.register_callback_query_handler(ntf_craft, text= ['ntf_craft'], state=craft_states.Q1)

# /g_deposit & /g_receive
dp.register_message_handler(g_receive_and_deposit, lambda c: c.text.startswith('/g_deposit') or '/g_receive' in c.text,
                            state=craft_states.Q1)

# ⚖Биржа
dp.register_message_handler(trade, filters.Text(equals='⚖Биржа', ignore_case=True))

# /gs [id] ...
dp.register_message_handler(gs, commands=['gs'])
'''------------------------------------------------------------------------------------------------------------------'''


'''<<<-----   📜ARCHIVE SECTION   ----->>>'''
# 👥Участники
dp.register_message_handler(roles, filters.Text(equals='👥Участники', ignore_case=True))

# 🎉Праздники
#dp.register_message_handler(hb_func.hb, filters.Text(equals='🎉Праздники', ignore_case=True))

# Подписка на оповещения праздников
#dp.register_callback_query_handler(hb_func.hb_sub, lambda c: c.data.startswith('sub:'))

# Отобразить все или ближайшие праздники
#dp.register_callback_query_handler(hb_func.hb_show, lambda c: c.data.startswith('show:'))
'''------------------------------------------------------------------------------------------------------------------'''


'''<<<-----   🔥BATTLE SECTION   ----->>>'''
# 🔥Битва
dp.register_message_handler(battle, filters.Text(equals='🔥Битва', ignore_case=True))

# 🔥Битва - 📯Дать пин
dp.register_message_handler(create_pin, filters.Text(equals='📯Создать пин', ignore_case=True), state=battle_states.menu)
dp.register_message_handler(create_pin_loc_list, filters.Text(equals='Локации🗺', ignore_case=True), state=battle_states.menu_pin)
dp.register_message_handler(public_pin, filters.Text, state=battle_states.menu_pin)

# Confirm & Decline
dp.register_message_handler(pin_confirm, filters.Text(equals='✅'), state=battle_states.al_order)
dp.register_message_handler(start_func, filters.Text(equals='❌'), state=battle_states.al_order)
'''------------------------------------------------------------------------------------------------------------------'''


'''<<<-----   INLINE QUERY SECTION   ----->>>'''
# Quality Craft
dp.register_inline_handler(quality_craft, text_contains='qc ')

# Loc List
dp.register_inline_handler(loc_list_query, text_contains='ll')

# Public Pin
dp.register_inline_handler(pub_pinnn, text_contains='pub_pin:')
'''------------------------------------------------------------------------------------------------------------------'''



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop)