from typing import Annotated, Union, Any
from pydantic import BaseModel, field_validator

class Some:
    @staticmethod
    def make_str(value: Any) -> str:
        return str(value)

class TgAccount(BaseModel):
    name: str
    id: Union[str, int]

    @field_validator('id', mode='before')
    def convert_id_to_str(cls, value: Union[str, int]) -> str:
        return Some.make_str(value)

# Пример использования
a = TgAccount(name="<NAME>", id=123)  # Передаем число
print(a)  # id='123'

b = TgAccount(name="<NAME>", id="456")  # Передаем строку
print(b)  # id='456'