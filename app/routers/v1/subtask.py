from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.subtask import SubTaskCreate, SubTaskResponse, UpdateSubTaskStatus
from app.core.subtask import (
    get_all_subtasks,
    get_subtask_by_id,
    create_subtask,
    update_subtask_status,
)

router = APIRouter(prefix="/subtasks", tags=["subtasks"])


@router.get("/", response_model=List[SubTaskResponse])
def get_all_subtask():
    subtasks = get_all_subtasks()
    return [
        SubTaskResponse(
            id=str(subtask.id),
            name=subtask.name,
            status=subtask.status,
        )
        for subtask in subtasks
    ]


@router.get("/{subtask_id}", response_model=SubTaskResponse)
def get_subtask(subtask_id: str):
    subtask = get_subtask_by_id(subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="SubTask not found")
    return SubTaskResponse(id=str(subtask_id), name=subtask.name, status=subtask.status)


@router.post("/create", response_model=SubTaskResponse)
def create_or_edit_subtask(subtask_data: SubTaskCreate):
    subtask = create_subtask(subtask_data)
    return SubTaskResponse(id=str(subtask.id), name=subtask.name, status=subtask.status)


@router.patch("/status/{subtask_id}")
def update_status(subtask_id: str, status_update: UpdateSubTaskStatus):
    subtask = update_subtask_status(subtask_id, status_update)
    if not subtask:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "message": "SubTask status updated successfully",
        "subtask_id": str(subtask_id),
    }
