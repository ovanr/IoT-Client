from typing import Callable, List, Any

def getHostName() -> str:
    with open("/etc/hostname", "r") as f:
        return f.read().replace("\n", "")

def callMany(fs: List[Callable]) -> Callable:
    def closure(*args, **kwargs) -> List[Any]:
        return [ f(*args, **kwargs) for f in fs ]

    return closure
