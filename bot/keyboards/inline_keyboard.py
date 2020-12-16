from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Custom Keyboard
def InlineKeyboard(args: list, row_width: int = 5):
    return InlineKeyboardMarkup(row_width=row_width).add(*[InlineKeyboardButton(text=l[0], callback_data=l[1]) for l in args])

# 💠Патчноут
patchnote_keyboard = InlineKeyboard(
    [('v1.0', 'v10'), ('v1.1', 'v11'), ('v1.2', 'v12'), ('v1.3', 'v13'), ('v1.3.3', 'v133'),
     ('v1.4', 'v14'), ('v2.0', 'v20'), ('v2.1', 'v21'), ('Закрыть', 'cancel')])

# /l_list
loc_keyboard = InlineKeyboard(
    [('🏷', 'loc_type_ruins'), ('📦', 'loc_type_mines'), ('🎖', 'loc_type_forts'), ('🎪', 'loc_type_al'),
    ('🚩','loc_type_cap'), ('Закрыть', 'cancel')])


# ⚒Мастерская
stock_keyboard = InlineKeyboard([('📦', 'craft:res'), ('🔩', 'craft:parts'), ('📜', 'craft:rec')], 3)


# /c_id
def crafting_keyboard(req: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='Забрать всё', url=f'https://t.me/share/url?url={req}'),
        InlineKeyboardButton(text='Пингануть', callback_data='ntf_craft'))


def ntf_craft_keyboard(req: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='Забрать всё', url=f'https://t.me/share/url?url={req}'))


def pub_pin_keyboard(req: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='📣Опубликовать', switch_inline_query=req))

# /settings
def settings_keyboard(res: tuple):
    delete_loc_ntf = ('Вкл✅', 'dln:off') if res[0] else ('Откл❌', 'dln:on')
    new_loc_ntf = ('Вкл✅', 'nln:off') if res[1] else ('Откл❌', 'nln:on')
    brief = ('Вкл✅', 'brf:off') if res[2] else ('Откл❌', 'brf:on')
    brief_mode = ('Вкл✅', 'brfm:off') if res[3] else ('Откл❌', 'brfm:on')
    return InlineKeyboard([delete_loc_ntf, new_loc_ntf, brief, brief_mode, ('Закрыть', 's_cancel')], 4)