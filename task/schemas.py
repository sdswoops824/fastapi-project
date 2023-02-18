from typing import List, Optional
from enum import Enum
from pydantic import BaseModel

class RobotTask(BaseModel):
    name: str
    required_time: float
    status: int
    creation_time: float
    start_time: float

class ShowRobotTask(BaseModel):
    id: int
    name: str
    required_time: float
    status: int
    creation_time: float
    start_time: float
    class Config():
        orm_mode = True

