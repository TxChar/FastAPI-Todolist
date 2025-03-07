from app.models import Task, SubTask
from app.schemas.subtask import SubTaskCreate
import datetime
from mongoengine import DoesNotExist


def get_all_subtasks():
    return SubTask.objects(is_deleted=False)


def get_subtask_by_id(subtask_id):
    return SubTask.objects(id=subtask_id, is_deleted=False).first()


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


def update_subtask_partial(subtask_id, data):
    subtask = SubTask.objects(id=subtask_id, is_deleted=False).first()
    if not subtask:
        return None
    update_data = {}
    if data.name is not None:
        update_data["set__name"] = data.name
    if data.expected_date is not None:
        update_data["set__expected_date"] = data.expected_date

    if update_data:
        update_data["set__updated_date"] = datetime.datetime.now(datetime.timezone.utc)
        subtask.update(**update_data)

    return subtask.reload()


def soft_delete_subtask(subtask_id):
    subtask = SubTask.objects(id=subtask_id, is_deleted=False).first()
    if subtask:
        subtask.update(
            set__is_deleted=True,
            set__updated_date=datetime.datetime.now(datetime.timezone.utc),
        )
        return True
    return False
