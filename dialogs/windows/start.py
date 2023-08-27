from operator import itemgetter

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Back, Calendar, Select, Column, Row
from aiogram_dialog.widgets.text import Format, Const

from dialogs import sg
from dialogs.events.start import del_msg, input_task_name, del_unexp_msg, set_deadline, task_select, \
    create_task_text, edit_task_text, set_doer
from dialogs.getters.start import get_start, get_task, get_created_tasks

home_win = Window(
    Format('Hi *{name}*✌️'),
    Format('Your referrer is {referrer}', 'referrer'),
    Const('Your tasks:', 'my_tasks'),
    Column(Select(Format('{item[1]}'), 'my_tasks', itemgetter(0), 'my_tasks', on_click=task_select)),
    Row(
        Cancel(on_click=del_msg),
        SwitchTo(Const('Created Tasks'), 'created_tasks', sg.HomeSG.createdTasks, when='has_created'),
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
    Format('**Deadline:** {task.deadline}', 'deadline'),
    Format('**Creator: {creator}**', 'creator'),
    Format('**Doer: {doer}**', 'doer'),
    Format('\n*{task.name}*\n{task.body}\n\n**For change content input text:**', 'task'),
    Row(
        SwitchTo(Const('Back'), 'go_home', sg.HomeSG.home, when=~F['creator']),
        SwitchTo(Const('Back'), 'to_created_tasks', sg.HomeSG.createdTasks, when='creator'),
        SwitchTo(Const('Set doer'), 'set_doer', sg.HomeSG.setDoer, when=~F['creator']),
        SwitchTo(Const('Set deadline'), 'set_deadline', sg.HomeSG.setDeadline),
    ),
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

doer_set_win = Window(
    Const('Input doer username or id'),
    MessageInput(set_doer),
    state=sg.HomeSG.setDoer,
)

created_tasks_win = Window(
    Const('Created tasks:', 'created_tasks'),
    Column(
        Select(Format('{item[1]}'), 'created_tasks', itemgetter(0), 'created_tasks', on_click=task_select)
    ),
    SwitchTo(Const('Back'), 'go_home', sg.HomeSG.home),
    MessageInput(del_unexp_msg),
    state=sg.HomeSG.createdTasks,
    getter=get_created_tasks,
)
