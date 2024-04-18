from typing import Optional

from pydantic import BaseModel
from pydantic import Field

class RunRequest(BaseModel):
    script:str
    session_id:str
    timeout:int=300
    keyword:Optional[str]=None
    output:bool=True

class RunResponse(BaseModel):
    result:str
    session_id:str
    


