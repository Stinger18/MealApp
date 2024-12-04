from pydantic import BaseModel, ConfigDict

class PantryItem(BaseModel):
    id: int
    ownerId: int
    name: str
    quantity: str|int
    date_added: str

    model_config = ConfigDict(from_attributes=True)
