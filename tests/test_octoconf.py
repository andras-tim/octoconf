# -*- coding: utf-8 -*-
import pytest

import octoconf
from tests.yaml_fake import TEST_CONFIG_YAML_PATH, get_fake_example_yaml


def octoconf_loads(yaml_used_config, used_config=None):
    yaml_content = get_fake_example_yaml(used_config=yaml_used_config)

    return octoconf.loads(
        yaml_content,
        variables={
            'BASEDIR': '/test',
        },
        used_config=used_config,
    )


def octoconf_load(used_config=None):
    with open(TEST_CONFIG_YAML_PATH) as fd:
        return octoconf.load(
            fd,
            variables={
                'BASEDIR': '/test',
            },
            used_config=used_config,
        )


@pytest.fixture
def config():
    return octoconf_load()


class TestConfigObject(object):
    def test_config_iterator(self, config):
        assert 'App' in config
        assert 'VALUE_WITH_VARIABLE' in config.App

    def test_config_key_getter(self, config):
        assert 'VALUE_WITH_VARIABLE' in config['App']

    def test_magic_attribute_not_exits_exception(self, config):
        with pytest.raises(AttributeError) as excinfo:
            config.not_exited_attribute

        assert '\'ConfigObject\' object has no attribute \'not_exited_attribute\'' == str(excinfo.value)

    def test_config_validity(self):
        config = octoconf_loads(yaml_used_config='DevelopmentConfig')
        assert {
            'DebugId': 'Development',
            'App': {
                'VALUE_WITH_VARIABLE': '/test/my_res',
                'UTF8_VALUE': u'Több hűtőházból kértünk színhúst',
            },
            'Flask': {
                'SERVER_NAME': '0.0.0.0:8000',
                'STATIC_FOLDER': '/test',
                'DEBUG': True,
                'TESTING': False,
            },
            'SqlAlchemy': {
                'SQLALCHEMY_DATABASE_URI': 'sqlite:///test/app.sqlite',
            },
        } == config.get_dict()

    def test_str_dump_validity(self):
        config = octoconf_loads(yaml_used_config='DevelopmentConfig')
        expected_config = """{'App': {'UTF8_VALUE': %s,
         'VALUE_WITH_VARIABLE': '/test/my_res'},
 'DebugId': 'Development',
 'Flask': {'DEBUG': True,
           'SERVER_NAME': '0.0.0.0:8000',
           'STATIC_FOLDER': '/test',
           'TESTING': False},
 'SqlAlchemy': {'SQLALCHEMY_DATABASE_URI': 'sqlite:///test/app.sqlite'}}""" % repr(u'Több hűtőházból kértünk színhúst')
        assert expected_config == str(config)

    def test_can_set_existed_value_by_key(self, config):
        config.Flask['STATIC_FOLDER'] = '/new_path'
        assert config.Flask.STATIC_FOLDER == '/new_path'

    def test_can_set_not_existed_value_by_key(self, config):
        config.Flask['NEW_PROPERTY'] = '/new_path'
        assert 'NEW_PROPERTY' in config.Flask
        assert config.Flask.NEW_PROPERTY == '/new_path'

    def test_can_not_set_existed_value_by_attr(self, config):
        config.Flask.STATIC_FOLDER = '/new_path'
        assert config.Flask.STATIC_FOLDER == '/test'

    def test_can_not_set_not_existed_value_by_attr(self, config):
        config.Flask.NEW_PROPERTY = '/new_path'
        assert 'NEW_PROPERTY' not in config.Flask


class TestOctoconfConfigSelector(object):
    data_for_used_config = (
        ('ProductionConfig', 'Production'),
        ('DevelopmentConfig', 'Development'),
        ('TestingConfig', 'Testing'),
    )

    @pytest.mark.parametrize('yaml_used_config,debug_id', data_for_used_config)
    def test_used_config(self, yaml_used_config, debug_id):
        config = octoconf_loads(yaml_used_config)
        assert debug_id == config.DebugId

    data_for_overridden_used_config = (
        ('ProductionConfig', 'DevelopmentConfig', 'Development'),
        ('DevelopmentConfig', 'TestingConfig', 'Testing'),
        ('TestingConfig', 'ProductionConfig', 'Production'),
    )

    @pytest.mark.parametrize('yaml_used_config,used_config,debug_id', data_for_overridden_used_config)
    def test_overridden_used_config(self, yaml_used_config, used_config, debug_id):
        config = octoconf_loads(yaml_used_config, used_config=used_config)
        assert debug_id == config.DebugId


class TestOctoconfInheritance(object):
    def test_single_level_inheritance(self, config):
        assert 'VALUE_WITH_VARIABLE' in config.App
        assert 'SqlAlchemy' in config

    def test_multi_level_inheritance(self):
        config = octoconf_loads(yaml_used_config='DependencyTopConfig')
        assert 'DependencyTop' == config.DebugId
        assert {
            1: 'Top',
            2: 'Middle',
            3: 'Bottom',
        } == config.DependencyLevel.get_dict()

    def test_single_level_circular_dependency_in_inheritance(self):
        with pytest.raises(octoconf.CircularDependencyError) as excinfo:
            octoconf_loads(yaml_used_config='MinimalCircularConfig')

        assert 'Circular dependency detected in YAML! ref_stack=[' \
               '\'MinimalCircularConfig\', ' \
               '\'MinimalCircularConfig\'' \
               ']' == str(excinfo.value)

    def test_multi_level_circular_dependency_in__inheritance(self):
        with pytest.raises(octoconf.CircularDependencyError) as excinfo:
            octoconf_loads(yaml_used_config='MultiCircularConfigTop')

        assert 'Circular dependency detected in YAML! ref_stack=[' \
               '\'MultiCircularConfigTop\', ' \
               '\'MultiCircularConfigMiddle\', ' \
               '\'MultiCircularConfigBottom\', ' \
               '\'MultiCircularConfigTop\'' \
               ']' == str(excinfo.value)


class TestOctoconfVariables(object):
    def test_substitution(self, config):
        assert '$BASE' not in config.App.VALUE_WITH_VARIABLE
        assert '/test/my_res' == config.App.VALUE_WITH_VARIABLE
