from __future__ import annotations

from ..cmddt     import Cmd
from ..command   import AbstractCommand

from .rebootdt   import Rebootopt 

from typing      import Dict

import subprocess

class Reboot(AbstractCommand):
    config: Rebootopt

    def __init__(self):
        super().__init__("Reboot")

    def perform(self, cmd: Cmd) -> bool:
        if not cmd.reboot.perform:
            return False
        
        return subprocess.run(["sudo", "poweroff"]).returncode == 0

