from pydantic import BaseModel

class ExampleModel(BaseModel):
    message: str = "Hello from shared.models!" 