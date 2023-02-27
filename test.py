from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, constr

class Host(BaseModel):
    url: str
    dc: int

class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: list[int] = []
    instance: Optional[Host] = None


external_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3'],
    'instance': Host(url='https://www.azna.gr', dc=5)
}
user = User(**external_data)

print(user.dict())
