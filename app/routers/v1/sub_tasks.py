from fastapi import APIRouter, HTTPException
from app.core.sub_task import create_sub_task
from app.schemas.task import SubTaskCreate, SubTaskResponse

router = APIRouter(prefix="/subtasks", tags=["subtasks"])


@router.post("/", response_model=SubTaskResponse)
def create_new_sub_task(sub_task_data: SubTaskCreate):
    sub_task = create_sub_task(sub_task_data)
    return SubTaskResponse(
        id=str(sub_task.id), name=sub_task.name, status=sub_task.status
    )
