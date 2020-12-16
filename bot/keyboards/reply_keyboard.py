from aiogram.types import ReplyKeyboardMarkup


# Custom Keyboard
def ReplyKeyboard(*args: str, row_width: int = 3):
    return ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=row_width).add(*args)

# /start
start_menu = ReplyKeyboard('🏛Холл', '🍺Таверна', '🏛Штаб [AT]', '🔥Битва', '⚙Другое')

# ⚙Другое
other_menu = ReplyKeyboard('💠Патчноут', 'ℹПомощь', 'Вернуться↩')

# 📜Архив
arch_menu = ReplyKeyboard('🔱...', '👥Участники', 'Вернуться↩')

# 📦Склад
stock_menu = ReplyKeyboard('⚒Мастерская', '⚖Биржа', '🎉Праздники', 'Вернуться↩', row_width=2)

# ⚒Мастерская
craft_menu = ReplyKeyboard('⚒Irrenriel', '📦Обновить сток гильдии', 'Вернуться↩', row_width=2)
interface_menu = ReplyKeyboard('🏅Герой', '🏰Замок', '⚒Вернуться к верстаку', row_width=2)
interface_castle_menu = ReplyKeyboard('🛎Аукцион', '⚖Биржа', '🏅Герой', '⚒Вернуться к верстаку', row_width=2)
interface_inv_menu = ReplyKeyboard('🎒Рюкзак', '📦Ресурсы', '⚗Алхимия', '⚒Крафт', '🏷Снаряжение', '🏅Герой', '⚒Вернуться к верстаку', row_width=3)
int_menu = ReplyKeyboard('🏅Герой', '⚒Вернуться к верстаку', row_width=1)

# 🔥Битва
battle_menu = ReplyKeyboard('📯Создать пин', 'Вернуться↩', row_width=1)