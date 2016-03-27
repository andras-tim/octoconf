# pylint: disable=misplaced-comparison-constant,redefined-outer-name,no-self-use

import pytest

import octoconf


def test_substitute_variables():
    yaml = """
        Fruits:
          path: /home/$USER/foo
          ${size}Size: 42
        """
    config = octoconf.loads(yaml, variables={'USER': 'test', 'size': 'small'}, used_config='Fruits')

    assert {
        'path': '/home/test/foo',
        'smallSize': 42,
    } == config.get_dict()


def test_can_define_variable_without_use():
    yaml = """
        Fruits:
          Banana: b
        """
    config = octoconf.loads(yaml, variables={'notUsedVariable': 42}, used_config='Fruits')

    assert {
        'Banana': 'b',
    } == config.get_dict()


def test_can_not_use_variable_without_define():
    yaml = """
        Fruits:
          Kiwi: ${notDefinedVariable}
        """

    with pytest.raises(octoconf.UndefinedVariableError) as excinfo:
        octoconf.loads(yaml, used_config='notDefinedVariable')

    assert 'notDefinedVariable' == str(excinfo.value)
