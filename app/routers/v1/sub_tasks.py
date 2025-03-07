from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.sub_task import SubTaskCreate, SubTaskResponse, UpdateSubTaskStatus
from app.core.sub_task import (
    get_all_subtasks,
    get_subtask_by_id,
    create_sub_task,
    update_sub_task_status,
)

router = APIRouter(prefix="/subtasks", tags=["subtasks"])


@router.get("/", response_model=List[SubTaskResponse])
def get_all_subtask():
    sub_tasks = get_all_subtasks()
    return [
        SubTaskResponse(
            id=str(sub_task.id),
            name=sub_task.name,
            status=sub_task.status,
        )
        for sub_task in sub_tasks
    ]


@router.get("/{subtask_id}", response_model=SubTaskResponse)
def get_subtask(subtask_id: str):
    subtask = get_subtask_by_id(subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="SubTask not found")
    return SubTaskResponse(id=str(subtask_id), name=subtask.name, status=subtask.status)


@router.post("/create", response_model=SubTaskResponse)
def create_subtask(sub_task_data: SubTaskCreate):
    sub_task = create_sub_task(sub_task_data)
    return SubTaskResponse(
        id=str(sub_task.id), name=sub_task.name, status=sub_task.status
    )


@router.patch("/status/{subtask_id}")
def update_status(subtask_id: str, status_update: UpdateSubTaskStatus):
    sub_task = update_sub_task_status(subtask_id, status_update)
    if not sub_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "message": "SubTask status updated successfully",
        "sub_task_id": str(subtask_id),
    }
