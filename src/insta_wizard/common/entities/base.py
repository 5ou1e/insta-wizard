from pydantic import BaseModel, ConfigDict


class Entity(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
