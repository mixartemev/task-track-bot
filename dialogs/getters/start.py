from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, ShowMode
from aiogram.types import User as TgUser

from db.models import User, Task

def _make_user_link(user: User|None) -> str|None:
    if user:
        return f'[{user.name}]({user.id})' if ' ' in user.name or user.name[0].isupper() else '@'+user.name
    return None

async def get_start(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data.clear()
    tgu: TgUser = dialog_manager.event.from_user
    user: User = await User.get(id=tgu.id).prefetch_related('my_tasks', 'referrer')
    tasks = [(task.id, task.name) for task in user.my_tasks]
    return {
        'name': tgu.full_name,
        'referrer': _make_user_link(user.referrer),
        'my_tasks': tasks,
        'has_created': await Task.exists(creator=user, doer_id__not=tgu.id),
    }

async def get_created_tasks(dialog_manager: DialogManager, **kwargs):
    tgu: TgUser = dialog_manager.event.from_user
    user: User = await User.get(id=tgu.id).prefetch_related('created_tasks')
    tasks = [(task.id, task.name) for task in user.created_tasks if task.doer_id != tgu.id]
    return {'created_tasks': tasks}


async def get_task(dialog_manager: DialogManager, event_from_user: TgUser, **kwargs):
    task = await Task[dialog_manager.dialog_data['task']]
    me = event_from_user.id
    return {
        'deadline': task.deadline,
        'doer': _make_user_link(await User[task.doer_id]) if task.doer_id != me else None,
        'creator': _make_user_link(await User[task.creator_id]) if task.creator_id != me else None,
        'task': task,
    }


async def get_deeplink(dialog_manager: DialogManager, _: FSMContext):
    user = dialog_manager.event.from_user
    data = dialog_manager.current_context().dialog_data
    return {
        'nick': data["opponent_nick"],
        'link': f'https://t.me/InfiniChatBot?start={user.id}',
    }
