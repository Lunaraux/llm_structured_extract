from pydantic import BaseModel


class ExtractTask(BaseModel):
    text: str
    schema: str = "user_info"
