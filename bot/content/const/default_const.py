from bot.keyboards import other_menu, arch_menu, stock_menu, battle_menu, craft_menu
from bot.content import OTHER_SECT_TEXT, ARCH_SECT_TEXT, STOCK_SECT_TEXT, BATTLE_SECT_TEXT, CRAFT_TEXT


CASTLE_EMBLEMS = {'☘': 'O', '🍁': 'A', '🍆': 'F', '🦇': 'M', '🖤': 'S', '🌹': 'R', '🐢': 'T'}
CASTLE_EMBLEMS_AROUND = {'O': '☘', 'A': '🍁', 'F': '🍆', 'M': '🦇', 'S': '🖤', 'R': '🌹', 'T': '🐢'}

SECTION_LIST = {
    '⚙Другое': {'text': OTHER_SECT_TEXT, 'reply_markup': other_menu},
    '🍺Таверна': {'text': ARCH_SECT_TEXT, 'reply_markup': arch_menu},
    '🏛Штаб [AT]': {'text': STOCK_SECT_TEXT, 'reply_markup': stock_menu},
    '🔥Битва': {'text': BATTLE_SECT_TEXT, 'reply_markup': battle_menu},
    '⚒Мастерская': {'text': CRAFT_TEXT, 'reply_markup': craft_menu},
    '⚒Вернуться к верстаку': {'text': CRAFT_TEXT, 'reply_markup': craft_menu}
}

REQ = 'SELECT id, username, nickname, lvl, class, guild_tag, castle, role, trade, hb_sub, hb_show, top_loc FROM users'