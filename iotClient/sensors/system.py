from __future__ import annotations

from ..sensor    import AbstractSensor
from ..sensordt  import Output 
from .systemdt   import Systemopt, Systemout

from vcgencmd    import Vcgencmd

import subprocess
import re

class System(AbstractSensor):
    config: Systemopt

    def __init__(self, config: Systemopt):
        super().__init__("System")
        self.config = config

    @property
    def voltage(self) -> float:
        v = Vcgencmd().measure_volts("sdram_p")
        if isinstance(v, float):
            return v 

        return 0.00
    
    @property
    def wifiSignal(self) -> float:
        p = subprocess.run(["iwconfig"], capture_output=True)
        if p.returncode != 0 or not p.stdout:
            return 0.00
        
        try:
            lines = p.stdout.decode('utf-8').splitlines() 
            m = re.search(r"Signal level=([-0-9]+)", lines[5])        
            return float(m.group(1))
        except: 
            return 0.00 
    
    def retrieveData(self) -> Output:
        return Output(
            system=Systemout( 
                voltage=self.voltage,
                wifi_signal=self.wifiSignal
            )
        )
