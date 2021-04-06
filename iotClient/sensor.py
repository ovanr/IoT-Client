from __future__ import annotations

from typing     import List, Dict, Union, NamedTuple
from abc        import abstractmethod, ABC

from .sensordt  import Sensorout,Output

class AbstractSensor(ABC):
    name: str
    
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def retrieveData(self) -> Output:
       pass 

class SensorManager():
    registeredSensors: List[AbstractSensor]

    def __init__(self):
        self.registeredSensors = []

    def __add__(self, sensor: AbstractSensor) -> SensorManager:
        self.registeredSensors.append(sensor)
        return self
    
    def __iter__(self):
        return self.registeredSensors

    def retrieveAllData(self) -> Sensorout:
        return Sensorout(
            [ s.retrieveData() for s in self.registeredSensors ]
        )
