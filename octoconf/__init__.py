from .octoconf import (
    Octoconf as _Octoconf,
    ConfigObject,
    CircularDependencyError,
    UndefinedVariableError
)

load = _Octoconf.load
loads = _Octoconf.loads
