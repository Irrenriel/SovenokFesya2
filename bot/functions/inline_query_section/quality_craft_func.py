from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import random


async def quality_craft(query: InlineQuery):
    quality = ['-', '🔸E',
               '-', '🔸E', '🔸D',
               '-', '🔸E', '🔸D', '🔸C',
               '-', '🔸E', '🔸D', '🔸C', '🔸B',
               '-', '🔸E', '🔸D', '🔸C', '🔸B', '🔸A',
               '-', '🔸E', '🔸D', '🔸C', '🔸B', '🔸A', '🔸SE']
    res = random.choice(quality)
    results = []
    item = query.query[3:]
    results.append(InlineQueryResultArticle(
        id=query.from_user.id,
        title='Скрафти воображаемую шмотку с качеством!',
        input_message_content=InputTextMessageContent(message_text=f'Получился {item} с качеством {res}!')
    ))
    await query.answer(results=results, cache_time=1, is_personal=True)