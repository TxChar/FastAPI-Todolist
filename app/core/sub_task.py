from app.models.task import MainTask, SubTask
from app.schemas.sub_task import SubTaskCreate, UpdateSubTaskStatus
import datetime
from mongoengine import DoesNotExist


def get_all_subtasks():
    return SubTask.objects()


def get_subtask_by_id(subtask_id):
    return SubTask.objects(id=subtask_id).first()


def create_sub_task(data: SubTaskCreate):
    sub_task = SubTask(
        name=data.name,
        status=data.status,
        expected_date=data.expected_date,
        created_date=datetime.datetime.now(datetime.timezone.utc),
        updated_date=datetime.datetime.now(datetime.timezone.utc),
    )
    sub_task.save()
    return sub_task


def update_sub_task_status(subtask_id, status_update):
    subtask = SubTask.objects(id=subtask_id).first()
    if not subtask:
        return False
    subtask.update(
        set__status=status_update.status,
        set__updated_date=datetime.datetime.now(datetime.timezone.utc),
    )
    return True


def add_sub_task_to_main_task(task_id: str, sub_task_id: str):
    try:
        main_task = MainTask.objects.get(id=task_id)
        sub_task = SubTask.objects.get(id=sub_task_id)
    except DoesNotExist:
        return None

    existing_sub_task_ids = {str(sub.id) for sub in main_task.sub_tasks}
    if str(sub_task.id) in existing_sub_task_ids:
        return None

    main_task.sub_tasks.append(sub_task)
    main_task.save()

    return main_task
