from typing import List

from pydantic import BaseModel
from pydantic import Field

class GetSessionRequest(BaseModel):
    prefix:str


class GetSessionResponse(BaseModel):
    result:List[str]


