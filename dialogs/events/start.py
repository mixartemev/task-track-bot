from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import User as TgUser
from aiogram_dialog.widgets.kbd import Button

from db.models import User
from dialogs.sg import HomeSG
from handlers import user_upsert


async def start(message: Message, dialog_manager: DialogManager):
    await _check_invite_link(message)
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(HomeSG.home, mode=StartMode.RESET_STACK, show_mode=ShowMode.EDIT)


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


async def del_msg(cb: CallbackQuery, button: Button, mng: ManagerImpl):
    await cb.message.delete()