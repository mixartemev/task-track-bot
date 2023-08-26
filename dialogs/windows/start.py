from operator import itemgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Back, Calendar, Select, Column, Row
from aiogram_dialog.widgets.text import Format, Const

from dialogs import sg
from dialogs.events.start import del_msg, input_task_name, del_unexp_msg, set_deadline, task_select, \
    create_task_text, edit_task_text
from dialogs.getters.start import get_start, get_task

home_win = Window(
    Format('Hi *{name}*✌️'),
    Format('Your referrer is @{referrer}', 'referrer'),
    Const('Your tasks:', 'tasks'),
    Column(Select(Format('{item[1]}'), 'tasks', itemgetter(0), 'tasks', on_click=task_select)),
    Row(
        Cancel(on_click=del_msg),
        SwitchTo(Const('+ New Task'), 'new_task', sg.HomeSG.inputTaskName),
    ),
    MessageInput(del_unexp_msg),
    state=sg.HomeSG.home,
    getter=get_start,
)


task_name_input_win = Window(
    Const('Input task name:'),
    Back(),
    MessageInput(input_task_name),
    state=sg.HomeSG.inputTaskName,
)

task_body_create_win = Window(
    Const('Input task text:'),
    Back(),
    MessageInput(create_task_text),
    state=sg.HomeSG.createTaskBody,
)

task_edit_win = Window(
    Format('*{task.name}*\n{task.body}\n\nFor change content input text:', 'task'),
    SwitchTo(Const('Back'), 'to_task_edit', sg.HomeSG.home),
    MessageInput(edit_task_text),
    state=sg.HomeSG.editTask,
    getter=get_task,
)

deadline_set_win = Window(
    Const('When deadline?'),
    Calendar('deadline', set_deadline),
    MessageInput(del_unexp_msg),
    state=sg.HomeSG.setDeadline,
)
