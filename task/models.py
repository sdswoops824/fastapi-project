from sqlalchemy import Column, Integer, String, Enum, Float
from task.database import Base

class RobotTask(Base):
    __tablename__ = 'Robot Tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    required_time = Column(Float)
    status = Column(Integer)
    creation_time = Column(Float)
    start_time = Column(Float)