from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, ShowMode
from aiogram.types import User as TgUser

from db.models import User, Task


async def get_start(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data.clear()
    tgu: TgUser = dialog_manager.event.from_user
    user: User = await User.get(id=tgu.id).prefetch_related('my_tasks', 'referrer')
    tasks = [(task.id, task.name) for task in user.my_tasks]
    return {
        'name': tgu.full_name,
        'referrer': user.referrer,
        'tasks': tasks,
    }


async def get_task(dialog_manager: DialogManager, **kwargs):
    task = await Task[dialog_manager.dialog_data['task']]
    return {'task': task}


async def get_deeplink(dialog_manager: DialogManager, _: FSMContext):
    user = dialog_manager.event.from_user
    data = dialog_manager.current_context().dialog_data
    return {
        'nick': data["opponent_nick"],
        'link': f'https://t.me/InfiniChatBot?start={user.id}',
    }
