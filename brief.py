from telethon import events
import re, datetime, logging, asyncio

from bin.main_var import bot, db, ChatWarsDigest, MyTestingChannel, brief_client
from bot.classes.brief_classes import HeadquartersBrief, LocationsBrief


#logging.basicConfig(level=logging.DEBUG)#, filename='error.log', filemode='w')


@brief_client.on(events.NewMessage(func=lambda c:
'🤝Headquarters news:' in c.message.message and c.message.to_id.channel_id in [ChatWarsDigest, MyTestingChannel]))
async def brief_headquarters(mes):
    if mes.message.fwd_from is None:
        date = str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        message_id = mes.message.id
    else:
        date = str(mes.message.fwd_from.date + datetime.timedelta(hours=3))[:-6]
        message_id = mes.message.fwd_from.channel_post

    HB_operator = HeadquartersBrief(mes.message.message, date, message_id)

    for event in HB_operator._give_events_list():
        HB_operator.work(event)
    answer_mode1, answer_mode2 = HB_operator.ending()

    chats = db.checkall('SELECT id, brief_mode FROM chats WHERE brief = 1', [])
    if not chats:
        return
    for chat in chats:
        try:
            await bot.send_message(chat[0], answer_mode1 if not chat[1] else answer_mode2, disable_web_page_preview=True)
            await asyncio.sleep(0.3)
        except:
            await asyncio.sleep(0.3)


@brief_client.on(events.NewMessage(func=lambda c:
'🗺State of map:' in c.message.message and c.message.to_id.channel_id in [ChatWarsDigest, MyTestingChannel]))
async def brief_locations(mes):
    if mes.message.fwd_from is None:
        date = str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        message_id = mes.message.id
    else:
        date = str(mes.message.fwd_from.date + datetime.timedelta(hours=3))[:-6]
        message_id = mes.message.fwd_from.channel_post

    LB_operator = LocationsBrief(mes.message.message, date, message_id)
    for event in LB_operator._give_events_list():
        LB_operator.work(event)
    answer_mode1, answer_mode2 = LB_operator.ending()

    chats = db.checkall('SELECT id, brief_mode FROM chats WHERE brief = 1', [])
    if not chats:
        return
    for chat in chats:
        try:
            await bot.send_message(chat[0], answer_mode1 if not chat[1] else answer_mode2, disable_web_page_preview=True)
            await asyncio.sleep(0.3)
        except:
            await asyncio.sleep(0.3)

print('Brief is working!')

brief_client.start()
brief_client.run_until_disconnected()