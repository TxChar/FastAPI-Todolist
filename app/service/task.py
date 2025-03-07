from app.models.task import Task, SubTask
from app.schemas.task import TaskCreate, SubTaskCreate
import datetime


def get_all_main_tasks():
    return Task.objects(is_deleted=False)


def get_main_task_by_id(task_id):
    return Task.objects(id=task_id, is_deleted=False).first()


def create_task(data: TaskCreate):
    subtasks = [
        SubTask(**sub.model_dump()).save() for sub in data.subtasks
    ]  # สร้าง SubTasks ก่อน
    task = Task(
        name=data.name,
        status=data.status,
        expected_date=data.expected_date,
        created_date=datetime.datetime.now(datetime.timezone.utc),
        subtasks=subtasks,
    )
    task.save()
    return task


def update_task_status(task_id, status_update):
    task = Task.objects(id=task_id).first()
    if not task:
        return False
    task.update(
        set__status=status_update.status,
        set__updated_date=datetime.datetime.now(datetime.timezone.utc),
    )
    return True


def update_task_partial(task_id, data):
    task = Task.objects(id=task_id, is_deleted=False).first()
    if not task:
        return None
    update_data = {}
    if data.name is not None:
        update_data["set__name"] = data.name
    if data.expected_date is not None:
        update_data["set__expected_date"] = data.expected_date

    if update_data:
        update_data["set__updated_date"] = datetime.datetime.now(datetime.timezone.utc)
        task.update(**update_data)

    return task.reload()


def soft_delete_task(task_id):
    task = Task.objects(id=task_id, is_deleted=False).first()
    if task:
        task.update(
            set__is_deleted=True,
            set__updated_date=datetime.datetime.now(datetime.timezone.utc),
        )
        return True
    return False
