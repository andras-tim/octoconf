# -*- coding: utf-8 -*-
import pytest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import octoconf
from tests.common import substitute_yaml


@pytest.fixture
def minimal_yaml():
    return substitute_yaml("""
        {_default_}: Orange

        Orange:
          orange: 12
        """)


@pytest.fixture
def utf8_yaml():
    return substitute_yaml("""
        Orange:
          utf8: Több hűtőházból kértünk színhúst
        """)


def test_load_string(minimal_yaml):
    config = octoconf.loads(yaml_string=minimal_yaml)

    assert {'orange': 12} == config.get_dict()


def test_load_empty_string():
    with pytest.raises(ValueError) as excinfo:
        octoconf.loads('')

    assert 'used_config was not set' == str(excinfo.value)


def test_load_non_profile_based_string():
    with pytest.raises(ValueError) as excinfo:
        octoconf.loads('kiwi')

    assert 'bad formatted YAML; have to be dict on top level' == str(excinfo.value)


def test_load_strem(minimal_yaml):
    fd = StringIO(minimal_yaml)
    config = octoconf.load(yaml_stream=fd)
    fd.close()

    assert {'orange': 12} == config.get_dict()


def test_load_utf8_character_contained_string(utf8_yaml):
    config = octoconf.loads(utf8_yaml, used_config='Orange')

    assert {'utf8': u'Több hűtőházból kértünk színhúst'} == config.get_dict()
    assert '{{\'utf8\': {!r}}}'.format(u'Több hűtőházból kértünk színhúst') == str(config)
