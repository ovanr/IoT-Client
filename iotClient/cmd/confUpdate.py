from __future__ import annotations

from ..cmddt     import Cmd
from ..command   import AbstractCommand

from .confupdatedt   import Confupdateopt 

from typing      import Dict

class ConfUpdate(AbstractCommand):
    config: Confupdateopt

    def __init__(self, confPath: str):
        super().__init__("ConfUpdate")
        self.confPath = confPath

    def perform(self, cmd: Cmd) -> bool:
        if not cmd.conf_update.perform:
            return False
        
        with open(self.confPath, "w+") as f:
            f.write(cmd.conf_update.new_conf.to_json())
        
        return True

