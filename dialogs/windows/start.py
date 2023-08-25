from aiogram_dialog import Window
# from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Format

from dialogs import sg
from dialogs.events.start import del_msg
# from dialogs.events.start import del_unexp_msg
from dialogs.getters.start import get_start

# class Cancel(BaseCancel):
#

home_win = Window(
    Format('Hi *{name}*✌️\nYour status is {status}'),
    Format('Your referrer is @{referrer}', 'referrer'),
    Cancel(on_click=del_msg),
    # MessageInput(del_unexp_msg),
    state=sg.HomeSG.home,
    getter=get_start,
)
