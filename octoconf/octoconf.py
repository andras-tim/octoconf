import string
import yaml
from collections import Mapping
from pprint import pformat
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


DEFAULT_CONFIG_SELECTOR = 'USED_CONFIG>'
BASE_CONFIG_SELECTOR = '<BASE'


class CircularDependencyError(Exception):
    pass


class ConfigObject(object):
    def __init__(self, data):
        """
        :type data: dict
        """
        self.__data = data

    def __check(self, name):
        """
        :type name: str
        """
        if name not in self.__data.keys():
            raise AttributeError('{!r} object has no attribute {!r}'.format(self.__class__.__name__, name))

    def __getattr__(self, name):
        """
        :type name: str
        """
        self.__check(name)
        if type(self.__data[name]) == dict:
            return ConfigObject(self.__data[name])
        else:
            return self.__data[name]

    def __iter__(self):
        for each in self.__data.keys():
            yield each

    def __getitem__(self, name):
        """
        :type name: str
        """
        self.__check(name)
        return self.__data[name]

    def __setitem__(self, name, value):
        """
        :type name: str
        """
        self.__data[name] = value

    def __str__(self):
        return pformat(self.__data)

    def get_dict(self):
        """
        :rtype: dict
        """
        return self.__data


class Octoconf(object):
    @classmethod
    def load(cls, yaml_stream, variables=None, used_config=None):
        """
        Load config from YAML contained IO stream (e.g. file)

        :type yaml_stream: StringIO
        :type variables: dict or None
        :type used_config: str or None
        :rtype: ConfigObject
        """
        yaml_string = yaml_stream.read()
        return cls.loads(yaml_string, variables=variables, used_config=used_config)

    @classmethod
    def loads(cls, yaml_string, variables=None, used_config=None):
        """
        Load config from YAML contained string

        :type yaml_string: str
        :type variables: dict or None
        :type used_config: str or None
        :rtype: ConfigObject
        """
        variables = variables or {}

        loader = yaml.Loader
        if 'CLoader' in dir(yaml):
            loader = yaml.CLoader

        substituted_yaml_string = cls.__substitute_yaml(yaml_string, variables)
        parsed_yaml = yaml.load(substituted_yaml_string, Loader=loader)

        used_config = used_config or parsed_yaml[DEFAULT_CONFIG_SELECTOR]
        inherited_yaml = cls.__inherit_yaml(parsed_yaml, used_config)

        return ConfigObject(inherited_yaml[used_config])

    @classmethod
    def __substitute_yaml(cls, yaml_string, variables):
        """
        :type yaml_string: str
        :type variables: dict
        :rtype: str
        """
        yaml_template = string.Template(yaml_string)
        substituted_yaml = yaml_template.substitute(variables)
        return substituted_yaml

    @classmethod
    def __inherit_yaml(cls, parsed_yaml, config_name, parent_stack=None):
        """
        :type parsed_yaml: dict
        :type config_name: str
        :type parent_stack: list or None
        :rtype: dict
        """
        if not parent_stack:
            parent_stack = []
        parent_stack.append(config_name)

        # Has it base?
        if BASE_CONFIG_SELECTOR not in parsed_yaml[config_name].keys():
            return parsed_yaml

        # Skipping circular-dependency
        base_name = parsed_yaml[config_name][BASE_CONFIG_SELECTOR]
        if base_name in parent_stack:
            raise CircularDependencyError('Circular dependency detected in YAML! ref_stack={!s}'.format(
                                          str(parent_stack + [base_name])))
        del parsed_yaml[config_name][BASE_CONFIG_SELECTOR]

        # Get full config with inherited base config
        parsed_yaml = cls.__inherit_yaml(parsed_yaml, base_name, parent_stack)

        # Set base_config based current config
        parsed_yaml[config_name] = cls.__update_dict_recursive(parsed_yaml[base_name], parsed_yaml[config_name])

        return parsed_yaml

    @classmethod
    def __update_dict_recursive(cls, base, update):
        """
        :type base: dict
        :type update: dict or Mapping
        :rtype: dict
        """
        for k, v in update.items():
            if isinstance(v, Mapping):
                r = cls.__update_dict_recursive(base.get(k, {}), v)
                base[k] = r
            else:
                base[k] = update[k]
        return base
