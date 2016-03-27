import pytest

import octoconf
from tests.common import substitute_yaml


@pytest.fixture
def tricky_single_level_overlapped_yaml():
    return substitute_yaml("""
        Fruit:
          size: 1
          color: 2
          weight: 3

        Orange:
          {_base_}: Fruit
          color: 14
          price: 15
          bundle: 16

        Tangerine:
          {_base_}: Orange
          weight: 27
          bundle: 28
          country: 29
        """)


def test_no_side_effects_for_non_inherited_ascending(tricky_single_level_overlapped_yaml):
    config = octoconf.loads(tricky_single_level_overlapped_yaml, used_config='Fruit')
    assert {
        'size': 1,
        'color': 2,
        'weight': 3,
    } == config.get_dict()


def test_single_level_overlapping_in_single_level_inheritance(tricky_single_level_overlapped_yaml):
    config = octoconf.loads(tricky_single_level_overlapped_yaml, used_config='Orange')
    assert {
        'size': 1,
        'color': 14,
        'weight': 3,
        'price': 15,
        'bundle': 16,
    } == config.get_dict()


def test_single_level_overlapping_in_multi_level_inheritance(tricky_single_level_overlapped_yaml):
    config = octoconf.loads(tricky_single_level_overlapped_yaml, used_config='Tangerine')
    assert {
        'size': 1,
        'color': 14,
        'weight': 27,
        'price': 15,
        'bundle': 28,
        'country': 29,
    } == config.get_dict()


@pytest.fixture
def multi_level_overlapped_yaml():
    return substitute_yaml("""
        SmallFruits:
          Apple:
            SmallApple:
              count: 1
          Kiwi:
            SmallKiwi:
              count: 2
            count: 3

        MediumFruits:
          {_base_}: SmallFruits
          Apple:
            SmallApple:
              size: 14
          Kiwi:
            count: 15
        """)


def test_multi_level_overlapping(multi_level_overlapped_yaml):
    config = octoconf.loads(multi_level_overlapped_yaml, used_config='MediumFruits')
    assert {
        'Apple': {
            'SmallApple': {
                'count': 1,
                'size': 14,
            },
        },
        'Kiwi': {
            'SmallKiwi': {
                'count': 2,
            },
            'count': 15,
        }
    } == config.get_dict()


def test_single_level_inplace_circular_dependency_detection():
    yaml = substitute_yaml("""
        Fruit:
          {_base_}: Fruit
        """)

    with pytest.raises(octoconf.CircularDependencyError) as excinfo:
        octoconf.loads(yaml, used_config='Fruit')

    assert 'circular dependency detected; ref_chain=[' \
           '\'Fruit\', ' \
           '\'Fruit\'' \
           ']' == str(excinfo.value)


def test_multi_level_inplace_circular_dependency_detection():
    yaml = substitute_yaml("""
        Fruit:
          {_base_}: Fruit

        Orange:
          {_base_}: Fruit

        Tangerine:
          {_base_}: Orange
        """)

    with pytest.raises(octoconf.CircularDependencyError) as excinfo:
        octoconf.loads(yaml, used_config='Tangerine')

    assert 'circular dependency detected; ref_chain=[' \
           '\'Tangerine\', ' \
           '\'Orange\', ' \
           '\'Fruit\', ' \
           '\'Fruit\'' \
           ']' == str(excinfo.value)


def test_multi_level_circular_dependency_detection():
    yaml = substitute_yaml("""
        Fruit:
          {_base_}: Tangerine

        Orange:
          {_base_}: Fruit

        Tangerine:
          {_base_}: Orange
        """)

    with pytest.raises(octoconf.CircularDependencyError) as excinfo:
        octoconf.loads(yaml, used_config='Tangerine')

    assert 'circular dependency detected; ref_chain=[' \
           '\'Tangerine\', ' \
           '\'Orange\', ' \
           '\'Fruit\', ' \
           '\'Tangerine\'' \
           ']' == str(excinfo.value)
