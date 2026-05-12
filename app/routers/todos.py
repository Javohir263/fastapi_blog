from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/todos", tags=["Todos"])


# -------------------
# MODEL
# -------------------
class Todo(BaseModel):
    title: str
    completed: bool = False


# -------------------
# DATABASE (TEMP)
# -------------------
todos_db = []
todo_id = 1


# -------------------
# GET ALL
# -------------------
@router.get("/")
def get_todos():
    return {"todos": todos_db}


# -------------------
# CREATE
# -------------------
@router.post("/")
def create_todo(todo: Todo):
    global todo_id

    data = todo.model_dump()
    data["id"] = todo_id
    todo_id += 1

    todos_db.append(data)
    return data


# -------------------
# UPDATE
# -------------------
@router.put("/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    for i, t in enumerate(todos_db):
        if t["id"] == todo_id:
            updated = todo.model_dump()
            updated["id"] = todo_id
            todos_db[i] = updated
            return updated

    raise HTTPException(status_code=404, detail="Todo topilmadi")


# -------------------
# DELETE
# -------------------
@router.delete("/{todo_id}")
def delete_todo(todo_id: int):
    for i, t in enumerate(todos_db):
        if t["id"] == todo_id:
            todos_db.pop(i)
            return {"xabar": "O'chirildi"}

    raise HTTPException(status_code=404, detail="Todo topilmadi")