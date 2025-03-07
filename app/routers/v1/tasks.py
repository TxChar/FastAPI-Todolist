from fastapi import APIRouter, HTTPException
from app.core.task import (
    create_main_task,
    get_all_main_tasks,
    get_main_task_by_id,
    update_task_status,
    delete_main_task,
)
from app.core.sub_task import (
    create_sub_task,
    add_sub_task_to_main_task,
)
from app.schemas.task import (
    MainTaskCreate,
    MainTaskResponse,
    UpdateTaskStatus,
    SubTaskResponse,
)
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[MainTaskResponse])
def get_all_tasks():
    tasks = get_all_main_tasks()
    return [
        MainTaskResponse(
            id=str(task.id),
            name=task.name,
            status=task.status,
            sub_tasks=[
                SubTaskResponse(
                    id=str(sub_task.id),  # แปลง ObjectId เป็น string
                    name=sub_task.name,
                    status=sub_task.status,
                )
                for sub_task in task.sub_tasks
            ],
        )
        for task in tasks
    ]


@router.get("/{task_id}", response_model=MainTaskResponse)
def get_task(task_id: str):
    task = get_main_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return MainTaskResponse(
        id=str(task.id),
        name=task.name,
        status=task.status,
        sub_tasks=[
            SubTaskResponse(
                id=str(sub_task.id),  # แปลง ObjectId เป็น string
                name=sub_task.name,
                status=sub_task.status,
            )
            for sub_task in task.sub_tasks
        ],
    )


@router.post("/create", response_model=MainTaskResponse)
def create_task(task_data: MainTaskCreate):
    task = create_main_task(task_data)
    return MainTaskResponse(
        id=str(task.id), name=task.name, status=task.status, sub_tasks=task.sub_tasks
    )


@router.patch("/status/{task_id}")
def update_status(task_id: str, status_update: UpdateTaskStatus):

    if not update_task_status(task_id, status_update):
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task status updated successfully", "task_id": str(task_id)}


@router.delete("/delete/{task_id}")
def delete_task(task_id: str):
    if delete_main_task(task_id):
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}/add_subtask/{sub_task_id}", response_model=MainTaskResponse)
def add_sub_task(task_id: str, sub_task_id: str):
    updated_task = add_sub_task_to_main_task(task_id, sub_task_id)
    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail="MainTask or SubTask not found or SubTask already exists",
        )

    return MainTaskResponse(
        id=str(updated_task.id),
        name=updated_task.name,
        status=updated_task.status,
        sub_tasks=[
            SubTaskResponse(
                id=str(sub_task.id),
                name=sub_task.name,
                status=sub_task.status,
            )
            for sub_task in updated_task.sub_tasks
        ],
    )
