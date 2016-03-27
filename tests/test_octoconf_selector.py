import pytest

import octoconf
from tests.common import substitute_yaml


def get_yaml(used_config):
    yaml = """
        {_default_}: {used_config}

        Apple:
          letter: A

        Banana:
          letter: B
        """
    return substitute_yaml(yaml, used_config=used_config)


missing_config_selector_yaml = """
    Cherry:
      letter: C
    """


def test_raise_when_config_selector_is_missing_from_yaml_and_load():
    with pytest.raises(ValueError) as excinfo:
        octoconf.loads(missing_config_selector_yaml)

    assert 'used_config was not set' == str(excinfo.value)


def test_load_when_config_selector_is_set_at_load_only():
    config = octoconf.loads(missing_config_selector_yaml, used_config='Cherry')
    assert {'letter': 'C'} == config.get_dict()


@pytest.mark.parametrize('used_config_in_yaml,expected_config', (
    ('Apple', {'letter': 'A'}),
    ('Banana', {'letter': 'B'}),
))
def test_default_config_selection(used_config_in_yaml, expected_config):
    yaml = get_yaml(used_config=used_config_in_yaml)
    config = octoconf.loads(yaml)
    assert expected_config == config.get_dict()


@pytest.mark.parametrize('used_config_in_yaml,used_config_at_load,expected_config', (
    ('Apple', 'Apple', {'letter': 'A'}),
    ('Apple', 'Banana', {'letter': 'B'}),
    ('Banana', 'Apple', {'letter': 'A'}),
    ('Banana', 'Banana', {'letter': 'B'}),
))
def test_overridden_config_selection(used_config_in_yaml, used_config_at_load, expected_config):
    yaml = get_yaml(used_config=used_config_in_yaml)
    config = octoconf.loads(yaml, used_config=used_config_at_load)
    assert expected_config == config.get_dict()


def test_raise_when_referred_config_is_not_exist():
    yaml = get_yaml(used_config='Melon')
    with pytest.raises(ValueError) as excinfo:
        octoconf.loads(yaml)

    assert 'missing used_config referred node: \'Melon\'' == str(excinfo.value)
