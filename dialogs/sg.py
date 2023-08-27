from aiogram.fsm.state import StatesGroup, State


class HomeSG(StatesGroup):
    home = State()
    inputTaskName = State()
    createTaskBody = State()
    editTask = State()
    setDeadline = State()
    setDoer = State()
    createdTasks = State()
