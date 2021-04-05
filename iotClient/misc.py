from typing import Callable, List, Any


def callMany(fs: List[Callable]) -> Callable:
    def closure(*args, **kwargs) -> List[Any]:
        return [ f(*args, **kwargs)  for f in fs ]

    return closure
