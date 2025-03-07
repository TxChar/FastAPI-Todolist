from app.models.task import MainTask, SubTask
from app.schemas.task import MainTaskCreate, SubTaskCreate
import datetime


def create_main_task(data: MainTaskCreate):
    sub_tasks = [
        SubTask(**sub.model_dump()).save() for sub in data.sub_tasks
    ]  # สร้าง SubTasks ก่อน
    task = MainTask(
        name=data.name,
        status=data.status,
        expected_date=data.expected_date,
        created_date=datetime.datetime.now(datetime.timezone.utc),
        sub_tasks=sub_tasks,
    )
    task.save()
    return task


def get_all_main_tasks():
    return MainTask.objects()


def get_main_task_by_id(task_id):
    return MainTask.objects(id=task_id).first()


def update_main_task(task_id, data):
    task = MainTask.objects(id=task_id).first()
    if task:
        task.update(
            **data.model_dump(),
            updated_date=datetime.datetime.now(datetime.timezone.utc)
        )
        return task.reload()
    return None


def delete_main_task(task_id):
    task = MainTask.objects(id=task_id).first()
    if task:
        task.delete()
        return True
    return False
