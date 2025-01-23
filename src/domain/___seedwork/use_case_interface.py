from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputType = TypeVar('InputType')  # Tipo genérico para o input
OutputType = TypeVar('OutputType')  

class UseCaseInterface(ABC, Generic[InputType, OutputType]):
    
    @abstractmethod
    def execute(input: InputType) -> OutputType:
        pass