import pydantic
from pydantic import BaseModel
from typing import List,Any
from ksuid import ksuid

class UserModel(BaseModel):
    PK: str = ''
    user_id: str = ''
    connection_id: str

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if self.user_id == '':
            self.user_id = ksuid().__str__()
        
        self.PK = f"{self.user_id}-{self.connection_id}"