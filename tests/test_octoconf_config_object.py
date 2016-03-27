# pylint: disable=misplaced-comparison-constant,redefined-outer-name,no-self-use

import pytest

from octoconf import ConfigObject


@pytest.fixture
def config():
    return ConfigObject({
        'Fruits': {
            'Apple': 'a',
            'Banana': 'b'
        },
        'Sizes': [
            'small',
            'large',
        ],
        'count': 42
    })


def test_can_iterate(config):
    assert 3 == len(tuple(config))
    assert {'Fruits', 'Sizes', 'count'} == set(config)

    assert 'Fruits' in config
    assert 'Sizes' in config
    assert 'count' in config


def test_can_get_existing_nodes_by_key(config):
    assert isinstance(config['Fruits'], ConfigObject)
    assert ['small', 'large'] == config['Sizes']
    assert 42 == config['count']


def test_can_get_existing_nodes_by_attr(config):
    assert isinstance(config.Fruits, ConfigObject)
    assert ['small', 'large'] == config.Sizes
    assert 42 == config.count


def test_can_get_nested_existing_nodes(config):
    assert 'a' == config['Fruits']['Apple']
    assert 'a' == config['Fruits'].Apple
    assert 'a' == config.Fruits['Apple']
    assert 'a' == config.Fruits.Apple


def test_can_not_get_not_existing_nodes(config):
    with pytest.raises(AttributeError) as excinfo:
        print(config['Avocado'])

    assert '\'ConfigObject\' object has no attribute \'Avocado\'' == str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        print(config.Avocado)

    assert '\'ConfigObject\' object has no attribute \'Avocado\'' == str(excinfo.value)


def test_can_change_existing_nodes_by_key(config):
    config['count'] = 100

    assert {'Fruits', 'Sizes', 'count'} == set(config)

    assert 100 == config['count']
    assert 100 == config.count


def test_can_change_existing_nodes_by_attr(config):
    config.count = 100

    assert {'Fruits', 'Sizes', 'count'} == set(config)

    assert 100 == config['count']
    assert 100 == config.count


def test_can_create_nodes_by_key(config):
    config['new'] = 'new_value'

    assert {'Fruits', 'Sizes', 'count', 'new'} == set(config)

    assert 'new_value' == config['new']
    assert 'new_value' == config.new


def test_can_create_nodes_by_attr(config):
    config.new = 'new_value'

    assert {'Fruits', 'Sizes', 'count', 'new'} == set(config)

    assert 'new_value' == config['new']
    assert 'new_value' == config.new


def test_dict_representation(config):
    assert {
        'Fruits': {
            'Apple': 'a',
            'Banana': 'b'
        },
        'Sizes': [
            'small',
            'large',
        ],
        'count': 42
    } == config.get_dict()


def test_string_representation():
    # FYI: the enumeration is not defined in a dict, therefore there will be used one child element in dicts
    config = ConfigObject({
        'Fruits': {
            'Apple': 'a',
        },
    })

    assert '{\'Fruits\': {\'Apple\': \'a\'}}' == str(config)
