from aiogram import Dispatcher, Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from tortoise import Tortoise
from dotenv import load_dotenv
from os import getenv as env


load_dotenv()


async def db_init(gen_sch: bool = False):
    await Tortoise.init(
        db_url=env('PG_DSN'),
        modules={"models": ["db.models"]},
    )
    if gen_sch:
        await Tortoise.generate_schemas()


sess = AiohttpSession()
bt = Bot(token=env('BT'), session=sess, parse_mode=ParseMode.MARKDOWN_V2)
storage = RedisStorage.from_url(env('REDIS_DSN'), key_builder=DefaultKeyBuilder(with_destiny=True))
dp = Dispatcher(storage=storage)