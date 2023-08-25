from aiogram.types import ChatMemberUpdated, User as TgUser, Message

from db.models import User, UserStatus


async def del_unexp_msg(msg: Message):
    await msg.delete()


async def user_upsert(u: TgUser) -> (User, bool):
    user, is_created = await User.update_or_create({'name': u.username}, id=u.id)
    return user, is_created


async def user_set_status(my_chat_member: ChatMemberUpdated):
    u: TgUser = my_chat_member.from_user
    new_status = UserStatus[my_chat_member.new_chat_member.status]
    await User.update_or_create({'name': u.username, 'status': new_status}, id=u.id)
