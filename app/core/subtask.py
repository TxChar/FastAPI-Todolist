from app.models import Task, SubTask
from app.schemas.subtask import SubTaskCreate
import datetime
from mongoengine import DoesNotExist


def get_all_subtasks():
    return SubTask.objects()


def get_subtask_by_id(subtask_id):
    return SubTask.objects(id=subtask_id).first()


def create_subtask(data: SubTaskCreate):
    subtask = SubTask(
        name=data.name,
        status=data.status,
        expected_date=data.expected_date,
        created_date=datetime.datetime.now(datetime.timezone.utc),
        updated_date=datetime.datetime.now(datetime.timezone.utc),
    )
    subtask.save()
    return subtask


def update_subtask_status(subtask_id, status_update):
    subtask = SubTask.objects(id=subtask_id).first()
    if not subtask:
        return False
    subtask.update(
        set__status=status_update.status,
        set__updated_date=datetime.datetime.now(datetime.timezone.utc),
    )
    return True


def add_subtask_to_main_task(task_id: str, subtask_id: str):
    try:
        main_task = Task.objects.get(id=task_id)
        subtask = SubTask.objects.get(id=subtask_id)
    except DoesNotExist:
        return None

    existing_subtask_ids = {str(sub.id) for sub in main_task.subtasks}
    if str(subtask.id) in existing_subtask_ids:
        return None

    main_task.subtasks.append(subtask)
    main_task.save()

    return main_task
