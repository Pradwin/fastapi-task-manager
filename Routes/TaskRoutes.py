from fastapi import APIRouter,Depends
from database import get_db
from sqlalchemy.orm import Session
from Schemas.schemas import TaskCreate,TaskUpdate,TaskResponse
from Utils.Dependencies import get_current_user
from Crud import TaskCrud

routerTask = APIRouter()

@routerTask.post("/", response_model=TaskResponse,status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return TaskCrud.crud_create_task(task,db,current_user) 

@routerTask.get("/", response_model=list[TaskResponse],status_code=200)
def get_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    status : str|None = None,
    page: int = 1,
    limit: int = 5,
    sort : str|None = None
):
    return TaskCrud.crud_get_tasks(db,current_user,status,page,limit,sort)

@routerTask.put("/{task_id}", response_model=TaskResponse,status_code=200)
def update_task(
    task_id: str,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return TaskCrud.crud_update_task(task_id,task,db,current_user)


@routerTask.delete("/{task_id}" ,status_code=200)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return TaskCrud.crud_delete_task(task_id,db,current_user)

@routerTask.get("/overdue",status_code=200,response_model = list[TaskResponse])
def get_overdue(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return TaskCrud.get_overdue(db,current_user)