from aiogram_dialog import Dialog

from dialogs.windows import start

start_dlg = Dialog(
    start.home_win,
    start.task_name_input_win,
    start.task_body_create_win,
    start.task_edit_win,
    start.deadline_set_win,
    start.created_tasks_win,
    start.doer_set_win,
)
