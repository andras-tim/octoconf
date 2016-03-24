import os

from octoconf.octoconf import DEFAULT_CONFIG_SELECTOR


def __read_fake_example_yaml():
    with open(TEST_CONFIG_YAML_PATH) as fd:
        lines = fd.read().strip().splitlines()

    lines[0] = '%s: {used_config}' % DEFAULT_CONFIG_SELECTOR
    return '\n'.join(lines)


TEST_CONFIG_YAML_PATH = os.path.join(os.path.dirname(__file__), '..', 'examples', 'test_config.yml')
__test_config_yaml_template = __read_fake_example_yaml()


def get_fake_example_yaml(used_config='ProductionConfig'):
    """
    :type used_config: str
    :rtype: str
    """
    return __test_config_yaml_template.format(used_config=used_config)
