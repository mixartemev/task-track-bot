from datetime import date
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import T
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import User as TgUser
from aiogram_dialog.widgets.kbd import Button, ManagedCalendar

from db.models import User, Task
from dialogs.sg import HomeSG
from handlers import user_upsert


async def start(message: Message, dialog_manager: DialogManager):
    await _check_invite_link(message)
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(HomeSG.home, mode=StartMode.RESET_STACK, show_mode=ShowMode.EDIT)

async def task_select(callback_query: CallbackQuery, button: Button, mng: DialogManager, t: T):
    mng.dialog_data['task'] = t
    await mng.switch_to(HomeSG.editTask)

async def input_task_name(message: Message, mi: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['task_name'] = message.text
    await dialog_manager.next()

async def create_task_text(message: Message, mi: MessageInput, dialog_manager: DialogManager):
    name = dialog_manager.dialog_data['task_name']
    task = await Task.create(body=message.text, name=name, creator_id=message.from_user.id)
    dialog_manager.dialog_data['task'] = task.id
    await dialog_manager.switch_to(HomeSG.setDeadline)

async def edit_task_text(message: Message, mi: MessageInput, dialog_manager: DialogManager):
    tid = dialog_manager.dialog_data['task']
    await (await Task[tid]).update_from_dict({'body': message.text}).save()
    await del_unexp_msg(message, mi, dialog_manager)

async def set_deadline(cbq: CallbackQuery, mc: ManagedCalendar, dialog_manager: DialogManager, deadline: date):
    tid = dialog_manager.dialog_data['task']
    task = await Task[tid]
    task.deadline = deadline
    await task.save()
    await dialog_manager.switch_to(HomeSG.editTask)

async def set_doer(message: Message, mi: MessageInput, dialog_manager: DialogManager):
    tid = dialog_manager.dialog_data['task']
    task = await Task[tid]
    doer = await User[int(txt)] if (txt := message.text).isnumeric() else await User.get(name=txt.strip().replace('@', ''))
    task.doer = doer
    await task.save()
    await dialog_manager.switch_to(HomeSG.editTask)

async def _check_invite_link(msg: Message):
    me: TgUser = msg.from_user
    user, cr = await user_upsert(me)
    if msg.text and (ref_id := msg.text.replace('/start', '').strip()) and ref_id.isdigit() and (ref_id := int(ref_id)):  # logged in by invite link
        if not cr:
            rs = 'You have registered already😉'
        elif user.id == ref_id:
            rs = 'You can not to ref yourself😒'
        elif not await User.exists(id=ref_id):
            rs = f'We have not registered user {ref_id}😒'
        else:
            return await user.update_from_dict({'referrer_id': ref_id}).save()
        return await msg.answer(rs)

async def del_msg(cb: CallbackQuery, button: Button, mng: DialogManager):
    await cb.message.delete()

async def del_unexp_msg(msg: Message, _, mng: DialogManager):
    mng.show_mode = ShowMode.EDIT
    await msg.delete()
