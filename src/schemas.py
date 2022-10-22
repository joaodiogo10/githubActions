from pydantic import BaseModel

# This file has the pydantic models 

class BaseUser(BaseModel):
    name: str
    email: str
    address: str

class User(BaseUser):
    id: int
    
    class Config:
        orm_mode = True