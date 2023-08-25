from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager
from aiogram.types import User as TgUser

from db.models import User


async def get_start(dialog_manager: DialogManager, state: FSMContext, **kwargs):
    tgu: TgUser = dialog_manager.event.from_user
    user: User = await User[tgu.id]
    ref: User|None = user.referrer_id and (await user.referrer).name
    return {
        'name': tgu.full_name,
        'status': user.status.name,
        'referrer': ref,
    }


async def get_deeplink(dialog_manager: DialogManager, _: FSMContext):
    user = dialog_manager.event.from_user
    data = dialog_manager.current_context().dialog_data
    return {
        'nick': data["opponent_nick"],
        'link': f'https://t.me/InfiniChatBot?start={user.id}',
    }
