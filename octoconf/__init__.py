# pylint: disable=invalid-name

from .octoconf import (
    Octoconf as _Octoconf,
    ConfigObject,
    CircularDependencyError,
    UndefinedVariableError,
    CircularIncludeError,
)

load = _Octoconf.load
loads = _Octoconf.loads
