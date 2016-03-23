import os

from octoconf.octoconf import DEFAULT_CONFIG_SELECTOR


def __read_fake_example_yaml(filename):
    with open(os.path.join(os.path.dirname(__file__), '..', 'examples', filename)) as fd:
        lines = fd.read().strip().splitlines()

    lines[0] = '%s: {used_config}' % DEFAULT_CONFIG_SELECTOR
    return '\n'.join(lines)


__test_config_yaml = __read_fake_example_yaml('test_config.yml')


def get_fake_reader(used_config='ProductionConfig'):
    """
    :type used_config: str
    :rtype: callable
    """
    def reader(*args, **kwargs):
        return __test_config_yaml.format(used_config=used_config)

    return reader
