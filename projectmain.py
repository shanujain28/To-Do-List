import dotenv
import os
import mysql.connector
from fastapi import FastAPI, HTTPException, status, Depends
from mysql.connector import errorcode
from pydantic import BaseModel, Field
from typing import List

dotenv.load_dotenv()
app = FastAPI()

class Task(BaseModel):
    task: str = Field(..., min_length=1, description="Task cannot be empty you must write a task")
    done: bool

class TaskResponse(BaseModel):
    task_id: int
    task: str
    done: bool

class TaskUpdate(BaseModel):
    task: str = Field(None, min_length=1, description="Task cannot be empty provide  a new task")

    done: bool = Field(None)

try:
    cnx = mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DB'],
    )
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password please check ")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist or  not accessible")

    else:
        print(err)

async def authenticate(api_key: str):
    cursor.execute("SELECT * FROM api_keys WHERE api_key = %s", (api_key,))
    api_key_data = cursor.fetchone()
    if not api_key_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden: Invalid API key"
        )

@app.get("/tasks", response_model=List[TaskResponse])
async def read_tasks(api_key: str = Depends(authenticate)):
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return [{"task_id": task[0], "task": task[1], "done": task[2]} for task in tasks]

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: Task, api_key: str = Depends(authenticate)):
    add_task = ("INSERT INTO tasks  (task, done) VALUES (%s, %s)")         
    data_task = (task.task, task.done)
    cursor.execute(add_task, data_task)
    cnx.commit()
    task_id = cursor.lastrowid
    return {"task_id": task_id, "task": task.task, "done": task.done}

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskUpdate, api_key: str = Depends(authenticate)):
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    existing_task = cursor.fetchone()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.task is not None or task.done is not None:
        update_task = ("UPDATE tasks SET task = COALESCE(%s, task), done = COALESCE(%s, done) WHERE task_id = %s")
        data_task = (task.task, task.done, task_id)
        cursor.execute(update_task, data_task)
        cnx.commit()
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    updated_task = cursor.fetchone()
    return {"task_id": updated_task[0], "task": updated_task[1], "done": updated_task[2]}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, api_key: str = Depends(authenticate)):
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    task = cursor.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
    cnx.commit()
    return {"task_id": task_id, "message": "Task deleted successfully"}

@app.on_event("shutdown the app To-do-list")
def shutdown_event():
    cursor.close()
    cnx.close()
