from aiogram.dispatcher.middlewares import BaseMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import types
import asyncio, sqlite3


class Middleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db
        super(Middleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        message.db = self.db

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        callback_query.db = self.db

    async def on_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        inline_query.db = self.db


class SQLite_db():
    '''
    This class make a 'req' requests to sqlite database with 'args' arguments.
    '''
    def __init__(self, db):
        self.con = sqlite3.connect(db, check_same_thread=False)

    def check(self, req, args=None):
        if args is None:
            args = []
        cur = self.con.cursor()
        cur.execute(req, args)
        res = cur.fetchone()
        cur.close()
        return res

    def checkall(self, req, args=None):
        if args is None:
            args = []
        cur = self.con.cursor()
        cur.execute(req, args)
        res = cur.fetchall()
        cur.close()
        return res

    def query(self, req, args=None):
        if args is None:
            args = []
        cur = self.con.cursor()
        cur.execute(req, args)
        self.con.commit()
        cur.close()

    def querymany(self, req, args=None):
        if args is None:
            args = []
        cur = self.con.cursor()
        cur.executemany(req, args)
        self.con.commit()
        cur.close()


class Scheduler_ex():
    def __init__(self, loop):
        self.loop = loop
        self.scheduler = AsyncIOScheduler({'apscheduler.executors.default': {'class': 'apscheduler.executors.pool:ThreadPoolExecutor','max_workers': '100'}})
        self.scheduler.start()

    def afs(self, func, params: dict, call=None):
        def result(res):
            if call:
                call(res.result())
        asyncio.ensure_future(func(**params), loop=self.loop).add_done_callback(result)

    def add_job(self, hours, minutes, seconds, args, id):
        self.scheduler.add_job(self.afs, trigger='interval', hours=hours, minutes=minutes, seconds=seconds, args=args, id=str(id))

    def add_job_for_pins(self, hour:int, minute:int, args:list, id=None):
        self.scheduler.add_job(self.afs, trigger='cron', hour=hour, minute=minute, args=args, id=id)

    def remove_job(self, id):
        self.scheduler.remove_job(str(id))

    def get_job(self, id):
        res = self.scheduler.get_job(str(id))
        return res