from __future__ import annotations

from typing     import List, Dict, Union, NamedTuple
from abc        import abstractmethod, ABC

from .cmddt     import Cmdin, Cmd

class AbstractCommand(ABC):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def perform(self, cmd: Cmd) -> bool:
       pass 

class CommandManager():
    registeredCommands: List[AbstractCommand]

    def __init__(self):
        self.registeredCommands = []

    def __add__(self, cmd: AbstractCommand) -> CommandManager:
        self.registeredCommands.append(cmd)
        return self
    
    def __iter__(self):
        return self.registeredCommands
    
    def performCommands(self, cmds: Cmdin) -> int:
        performed = 0
        for c in cmds.cmds:
            actions = map(lambda r: r.perform(c), self.registeredCommands)
            performed += len(list(filter(lambda x:x, actions)))

        return performed
