from fastapi import APIRouter, HTTPException
from app.service.task import (
    create_task,
    get_all_main_tasks,
    get_main_task_by_id,
    update_task_status,
    soft_delete_task,
    update_task_partial,
)
from app.service.subtask import (
    add_subtask_to_main_task,
)
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    UpdateTaskStatus,
    SubTaskResponse,
    UpdateTaskPartial,
)
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponse])
def get_all_tasks():
    tasks = get_all_main_tasks()
    return [
        TaskResponse(
            id=str(task.id),
            name=task.name,
            status=task.status,
            subtasks=[
                SubTaskResponse(
                    id=str(subtask.id),  # แปลง ObjectId เป็น string
                    name=subtask.name,
                    status=subtask.status,
                )
                for subtask in task.subtasks
            ],
        )
        for task in tasks
    ]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    task = get_main_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        id=str(task.id),
        name=task.name,
        status=task.status,
        subtasks=[
            SubTaskResponse(
                id=str(subtask.id),  # แปลง ObjectId เป็น string
                name=subtask.name,
                status=subtask.status,
            )
            for subtask in task.subtasks
        ],
    )


@router.post("/create", response_model=TaskResponse)
def create_or_edit_task(task_data: TaskCreate):
    task = create_task(task_data)
    return TaskResponse(
        id=str(task.id), name=task.name, status=task.status, subtasks=task.subtasks
    )


@router.patch("/status/{task_id}")
def update_status(task_id: str, status_update: UpdateTaskStatus):

    if not update_task_status(task_id, status_update):
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task status updated successfully", "task_id": str(task_id)}


@router.delete("/delete/{task_id}")
def delete_task(task_id: str):
    if soft_delete_task(task_id):
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}/add_subtask/{subtask_id}", response_model=TaskResponse)
def add_subtask(task_id: str, subtask_id: str):
    updated_task = add_subtask_to_main_task(task_id, subtask_id)
    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail="Task or SubTask not found or SubTask already exists",
        )

    return TaskResponse(
        id=str(updated_task.id),
        name=updated_task.name,
        status=updated_task.status,
        subtasks=[
            SubTaskResponse(
                id=str(subtask.id),
                name=subtask.name,
                status=subtask.status,
            )
            for subtask in updated_task.subtasks
        ],
    )


@router.patch("/edit/{task_id}")
def update_task(task_id: str, update_data: UpdateTaskPartial):
    updated_task = update_task_partial(task_id, update_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated successfully", "task": updated_task}
