from fastapi import FastAPI, Depends, status, Response, HTTPException
from task import schemas, models
from task.database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import update
import time

app = FastAPI()

models.Base.metadata.create_all(engine)

available_robots = 10

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# view app information
@app.get("/ReadMe")
async def information():
 return {"Greeting":"Hello user", "App Goal": "This app manages tasks for our robots", "Information": "Each task has the following properties","ID": "A unique ID for each task", "Name": "datatype:str # name of the task", "Required_time": "datatype:float # time required to complete task in minutes", "Status": "datatype:enum # 0:reservation, 1:in progress, 2:completion", "Creation_time": "Log the time when task was created", "Start_time": "Log the time when the task was started or sent to 'in progress' status"}

@app.post('/Create new robot_task', status_code=status.HTTP_201_CREATED)
def create(request: schemas.RobotTask, db: Session = Depends(get_db)):
    global available_robots
    if(available_robots > 0):
        new_robot_task = models.RobotTask(name=request.name, required_time=request.required_time, status=1, creation_time=float(f'{time.time():.2f}'), start_time=float(f'{time.time():.2f}'))
        db.add(new_robot_task)
        db.commit()
        db.refresh(new_robot_task)
        available_robots = available_robots-1
        print(available_robots)
        return new_robot_task
         
    else:
        new_robot_task = models.RobotTask(name=request.name, required_time=request.required_time, status=0, creation_time=float(f'{time.time():.2f}'), start_time=0.0)
        db.add(new_robot_task)
        db.commit()
        db.refresh(new_robot_task)
        print(available_robots)
        return new_robot_task

@app.get('/Display all robot_task', response_model=List[schemas.ShowRobotTask])
def display_all(db: Session = Depends(get_db)):
    robot_tasks = db.query(models.RobotTask).all()
    if not robot_tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"No robot tasks found.")
    return robot_tasks

@app.get('/Search robot_task/{id}', status_code=200, response_model=schemas.ShowRobotTask)
def search(id, response: Response, db: Session = Depends(get_db)):
    robot_task = db.query(models.RobotTask).filter(models.RobotTask.id == id).first()
    if not robot_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Robot task with the ID {id} isn't available.")
    return robot_task

@app.delete('/Delete robot_task/{id}', status_code=200)
def delete(id, db: Session = Depends(get_db)):
    robot_task = db.query(models.RobotTask).filter(models.RobotTask.id == id)
    if not robot_task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Robot task with the ID {id} isn't available.")
    robot_task.delete(synchronize_session=False)
    db.commit()    
    return 'Deleted successfully'

@app.put('/Update robot_task/{id}', status_code = status.HTTP_202_ACCEPTED)
def change_info(id, request: schemas.RobotTask, db: Session = Depends(get_db)):
    robot_task = db.query(models.RobotTask).filter(models.RobotTask.id == id)
    if not robot_task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Robot task with the ID {id} isn't available.")
    robot_task.update(request.dict())
    db.commit()
    return 'Updated successfully'

@app.post('/Reserve robot_task/{id}', status_code=status.HTTP_202_ACCEPTED)
def reserve_task(id, db: Session = Depends(get_db)):
    robot_task = db.query(models.RobotTask).filter(models.RobotTask.id == id)
    if not robot_task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Robot task with the ID {id} isn't available.")
    new_status = {"status": 0}
    robot_task.update(new_status)
    db.commit()
    return f'Changed status of Task {id} to reservation'

@app.post('/Run robot_task/{id}', status_code=status.HTTP_202_ACCEPTED)
def run_task(id, db: Session = Depends(get_db)):
    robot_task = db.query(models.RobotTask).filter(models.RobotTask.id == id)
    if not robot_task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Robot task with the ID {id} isn't available.")
    new_status = {"status": 1, "start_time": float(f'{time.time():.2f}')}
    robot_task.update(new_status)
    db.commit()
    return f'Changed status of Task {id} to in progress'

@app.post('/End robot_task/{id}', status_code=status.HTTP_202_ACCEPTED)
def end_task(id, db: Session = Depends(get_db)):
    robot_task = db.query(models.RobotTask).filter(models.RobotTask.id == id)
    if not robot_task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Robot task with the ID {id} isn't available.")
    new_status = {"status": 2}
    robot_task.update(new_status)
    db.commit()
    return f'Changed status of Task {id} to completion'