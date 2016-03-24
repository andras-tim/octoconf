from .octoconf import Octoconf as _Octoconf, ConfigObject, CircularDependencyError

load = _Octoconf.load
loads = _Octoconf.loads
