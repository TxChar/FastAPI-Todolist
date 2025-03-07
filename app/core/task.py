from app.models.task import Task, SubTask
from app.schemas.task import TaskCreate, SubTaskCreate
import datetime


def get_all_main_tasks():
    return Task.objects()


def get_main_task_by_id(task_id):
    return Task.objects(id=task_id).first()


def create_main_task(data: TaskCreate):
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
    # อัปเดต status และ updated_date
    task.update(
        set__status=status_update.status,
        set__updated_date=datetime.datetime.now(datetime.timezone.utc),
    )
    return True
    # return {"message": "Task status updated successfully", "task_id": str(task_id)}


# This function should change to update only
# is_deleted = True|False
def delete_main_task(task_id):
    task = Task.objects(id=task_id).first()
    if task:
        task.delete()
        return True
    return False


# def update_main_task(task_id, data):
#     task = Task.objects(id=task_id).first()
#     if task:
#         task.update(
#             **data.model_dump(),
#             updated_date=datetime.datetime.now(datetime.timezone.utc)
#         )
#         return task.reload()
#     return None
