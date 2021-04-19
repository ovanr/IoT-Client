from __future__ import annotations

from ..cmddt     import Cmd
from ..command   import AbstractCommand
from ..configdt  import Devconf

from .confupdatedt   import Confupdateopt 

def mergeDictR(primary: dict, secondary: dict) -> dict:
    newDict = {} 
    for (k,v) in primary.items():
        if isinstance(v, dict):
            newDict[k] = mergeDictR(v, secondary[k])
        else:
            newDict[k] = v
    
    for (k,v) in secondary.items():
        if k not in primary:
            newDict[k] = v
    
    return newDict

class ConfUpdate(AbstractCommand):
    config: Confupdateopt
    origConf: Devconf

    def __init__(self, confPath: str, origConf: Devconf):
        super().__init__("ConfUpdate")
        self.confPath = confPath
        self.origConf = origConf
    
    def perform(self, cmd: Cmd) -> bool:
        if not cmd.conf_update.perform:
            return False
        print("Performing configuration update")

        d = cmd.conf_update.new_conf.to_dict()
        newDict = mergeDictR(d, self.origConf.to_dict())

        with open(self.confPath, "w+") as f:
            f.write(Devconf().from_dict(newDict).to_json())
        
        return True
