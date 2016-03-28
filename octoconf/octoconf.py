import os
import string
import yaml
from collections import Mapping
from pprint import pformat

YamlLoader = yaml.Loader
if 'CLoader' in dir(yaml):
    YamlLoader = yaml.CLoader

DEFAULT_CONFIG_SELECTOR = 'USED_CONFIG>'
BASE_CONFIG_SELECTOR = '<BASE'
INCLUDE_FILE_SPECIFIER = '<INCLUDE'


class CircularDependencyError(Exception):
    pass


class UndefinedVariableError(Exception):
    pass


class CircularIncludeError(Exception):
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
        if isinstance(self.__data[name], dict):
            return ConfigObject(self.__data[name])
        else:
            return self.__data[name]

    def __setattr__(self, key, value):
        if key == '_ConfigObject__data':
            super(ConfigObject, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)

    def __iter__(self):
        for each in self.__data.keys():
            yield each

    def __getitem__(self, name):
        """
        :type name: str
        """
        return self.__getattr__(name)

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
    def load(cls, yaml_stream, variables=None, used_config=None, include_cwd=None):
        """
        Load config from YAML contained IO stream (e.g. file)

        :type yaml_stream: io.StringIO or io.TextIOWrapper
        :type variables: dict or None
        :type used_config: str or None
        :type include_cwd: str or None
        :rtype: ConfigObject
        """
        yaml_string = yaml_stream.read()
        return cls.loads(yaml_string, variables=variables, used_config=used_config, include_cwd=include_cwd)

    @classmethod
    def loads(cls, yaml_string, variables=None, used_config=None, include_cwd=None):
        """
        Load config from YAML contained string

        :type yaml_string: str
        :type variables: dict or None
        :type used_config: str or None
        :type include_cwd: str or None
        :rtype: ConfigObject
        """
        variables = variables or {}

        parsed_yaml = cls.__parse_yaml(yaml_string, variables=variables)
        populated_yaml = cls.__populate_includes(parsed_yaml, variables=variables, include_cwd=include_cwd)

        used_config = used_config or populated_yaml.get(DEFAULT_CONFIG_SELECTOR)
        if used_config is None:
            raise ValueError('used_config was not set')
        if used_config not in populated_yaml.keys():
            raise ValueError('missing used_config referred node: {!r}'.format(used_config))

        inherited_yaml = cls.__inherit_yaml(populated_yaml, used_config)

        return ConfigObject(inherited_yaml[used_config])

    @classmethod
    def __parse_yaml(cls, yaml_string, variables):
        """
        :type yaml_string: str
        :type variables: dict
        :rtype dict
        """
        substituted_yaml_string = cls.__substitute_yaml(yaml_string, variables)

        parsed_yaml = yaml.load(substituted_yaml_string, Loader=YamlLoader) or {}
        if not isinstance(parsed_yaml, dict):
            raise ValueError('bad formatted YAML; have to be dict on top level')

        return parsed_yaml

    @classmethod
    def __populate_includes(cls, parsed_yaml, variables, include_cwd=None, already_included=None):
        """
        :type parsed_yaml: dict
        :type variables: dict
        :type include_cwd: str or None
        :type already_included: list or None
        :rtype: dict
        """
        already_included = already_included or []

        # initialize list of includes
        includes = parsed_yaml.get(INCLUDE_FILE_SPECIFIER)
        if isinstance(includes, str):
            includes = [includes]

        if not includes:
            return parsed_yaml

        # build base yaml from includes
        base_yaml = {}
        for path in includes:
            already_included_stack = list(already_included)

            if include_cwd:
                path = os.path.join(include_cwd, path)
            abs_path = os.path.abspath(path)

            if abs_path in already_included_stack:
                raise CircularIncludeError('circular include detected; ref_chain={ref_chain!s}'.format(
                    ref_chain=already_included_stack + [abs_path]))

            with open(abs_path) as fd:
                included_yaml_string = fd.read()

            included_parsed_yaml = cls.__parse_yaml(included_yaml_string, variables=variables)
            already_included_stack.append(abs_path)

            included_populated_yaml = cls.__populate_includes(
                included_parsed_yaml, variables=variables,
                include_cwd=os.path.dirname(abs_path),
                already_included=already_included_stack)

            base_yaml = cls.__update_dict_recursive(base_yaml, included_populated_yaml)

        # update included base with parsed_yaml
        return cls.__update_dict_recursive(base_yaml, parsed_yaml)

    @classmethod
    def __substitute_yaml(cls, yaml_string, variables):
        """
        :type yaml_string: str
        :type variables: dict
        :rtype: str
        """
        yaml_template = string.Template(yaml_string)
        try:
            substituted_yaml = yaml_template.substitute(variables)
        except KeyError as e:
            raise UndefinedVariableError('; '.join(e.args))
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
            raise CircularDependencyError('circular dependency detected; ref_chain={ref_chain!s}'.format(
                ref_chain=parent_stack + [base_name]))

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
                base[k] = cls.__update_dict_recursive(base.get(k, {}), v)
            else:
                base[k] = update[k]
        return base
