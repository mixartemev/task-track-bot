import asyncio
import logging

from aiogram.filters import CommandStart
from aiogram_dialog import setup_dialogs
from dialogs.dialogs import start_dlg
from dialogs.events.start import start
from handlers import user_set_status, del_unexp_msg

from loader import dp, bt, db_init

logging.basicConfig(level=logging.INFO)

# dialogs
dp.message.register(start, CommandStart())
dp.include_router(start_dlg)
setup_dialogs(dp)

# aiogram
dp.my_chat_member.register(user_set_status)  # change user.status blocked/active
dp.message.register(del_unexp_msg)  # del all others messages


async def main():
    await db_init(True)
    await dp.start_polling(bt)


if __name__ == '__main__':
    asyncio.run(main())
