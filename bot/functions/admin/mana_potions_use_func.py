from aiogram.types import Message
import asyncio, random

from bin.config import ADMIN, CW_BOT_ID
from bin.main_var import main_client, scheduler



async def mana_start(mes: Message):
    #journal_log(mes)
    if mes.from_user.id != ADMIN:
        return
    if scheduler.get_job('eating_id'):
        await mes.answer('Уже запущено.')
        return


    potions_list = ['/use_p13', '/use_p14', '/use_p15']
    await main_client.connect()
    await mes.answer('Начал пить ману.')
    for potion in potions_list:
        await main_client.send_message(CW_BOT_ID, potion)
        await asyncio.sleep(float(str(random.uniform(2, 5))[0:4]))
    await main_client.disconnect()
    scheduler.add_job(hours=0, minutes=30, seconds=0, id='eating_id', args=[eat_scheduler, {'mes': mes}])


async def mana_stop(mes: Message):
    #journal_log(mes)
    if mes.from_user.id != ADMIN:
        return
    if not scheduler.get_job('eating_id'):
        await mes.answer('Процесс не запущен.')
        return
    scheduler.remove_job('eating_id')
    await mes.answer('Перестаю пить ману.')


async def eat_scheduler(mes):
    potions_list = ['/use_p13', '/use_p14', '/use_p15']
    await main_client.connect()
    for potion in potions_list:
        await main_client.send_message(CW_BOT_ID, potion)
        await asyncio.sleep(float(str(random.uniform(2, 5))[0:4]))
    await main_client.disconnect()
