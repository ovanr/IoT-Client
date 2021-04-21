from __future__ import annotations

from ..sensor    import AbstractSensor
from ..sensordt  import Output 
from .genericdt   import Genericopt, Genericout

import subprocess
import re

class Generic(AbstractSensor):
    config: Genericopt

    def __init__(self, config: Genericopt):
        super().__init__("Generic")
        self.config = config
    
    def retrieveData(self) -> Output:
        return Output(
            generic=Genericout( 
                value=990,
                name="H1"
            )
        )
