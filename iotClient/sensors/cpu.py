from __future__ import annotations

from ..sensor     import AbstractSensor
from ..sensordt  import Output 
from .cpudt      import Cpuopt, Cpuout

from typing      import Dict

import psutil

class Cpu(AbstractSensor):
    config: Cpuopt

    def __init__(self, config: Cpuopt):
        super().__init__("Cpu")
        self.config = config

    def __enter__(self) -> Cpu:
        return self

    def __exit__(self) -> None:
        # nothing to clean up
        return

    @property
    def percent(self) -> float:
        p = psutil.cpu_percent()  
        if isinstance(p, float):
            return p

        return 0.00
    
    @property
    def count(self) -> int:
        c = psutil.cpu_count()  
        if isinstance(c, int):
            return c 

        return 0
    
    @property
    def pkgTemp(self) -> float:
        t = psutil.sensors_temperatures().get('cpu_thermal', [])
        if t:
            return t[0].current
        else:
            return 0.00 
    
    def retrieveData(self) -> Output:
        return Output(
            cpu=Cpuout( 
                load=self.percent,
                count=self.count,
                pkg_temp=self.pkgTemp
            )
        )
