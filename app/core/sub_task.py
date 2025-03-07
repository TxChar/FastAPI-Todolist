from app.models.task import MainTask, SubTask
from app.schemas.task import SubTaskCreate
import datetime
from mongoengine import DoesNotExist


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
