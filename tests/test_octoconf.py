# -*- coding: utf-8 -*-
import pytest

import octoconf
from tests.yaml_fake import get_fake_reader


class TestOctoconf(object):
    def octoconf_read(self, yaml_used_config, used_config=None):
        fake_reader = get_fake_reader(used_config=yaml_used_config)

        return octoconf.read(
            '/test/foo.yaml',
            variables={
                'BASEDIR': '/test',
            },
            used_config=used_config,
            reader=fake_reader
        )

    @pytest.fixture
    def yaml(self):
        return self.octoconf_read(yaml_used_config='DevelopmentConfig')

    data_for_used_config = (
        ('ProductionConfig', 'Production'),
        ('DevelopmentConfig', 'Development'),
        ('TestingConfig', 'Testing'),
    )

    @pytest.mark.parametrize('yaml_used_config,debug_id', data_for_used_config)
    def test_used_config(self, yaml_used_config, debug_id):
        yaml = self.octoconf_read(yaml_used_config)
        assert debug_id == yaml.DebugId

    data_for_overridden_used_config = (
        ('ProductionConfig', 'DevelopmentConfig', 'Development'),
        ('DevelopmentConfig', 'TestingConfig', 'Testing'),
        ('TestingConfig', 'ProductionConfig', 'Production'),
    )

    @pytest.mark.parametrize('yaml_used_config,used_config,debug_id', data_for_overridden_used_config)
    def test_overridden_used_config(self, yaml_used_config, used_config, debug_id):
        yaml = self.octoconf_read(yaml_used_config, used_config=used_config)
        assert debug_id == yaml.DebugId

    def test_yaml_iterator(self, yaml):
        assert 'App' in yaml
        assert 'VALUE_WITH_VARIABLE' in yaml.App

    def test_yaml_key_getter(self, yaml):
        assert 'VALUE_WITH_VARIABLE' in yaml['App']

    def test_single_level_inheritance(self, yaml):
        assert 'VALUE_WITH_VARIABLE' in yaml.App
        assert 'SqlAlchemy' in yaml

    def test_multi_level_inheritance(self):
        yaml = self.octoconf_read(yaml_used_config='DependencyTopConfig')
        assert 'DependencyTop' == yaml.DebugId
        assert {
            1: 'Top',
            2: 'Middle',
            3: 'Bottom',
        } == yaml.DependencyLevel.get_dict()

    def test_single_level_circular_dependency_in_inheritance(self):
        with pytest.raises(octoconf.CircularDependencyError) as excinfo:
            self.octoconf_read(yaml_used_config='MinimalCircularConfig')

        assert 'Circular dependency detected in YAML! ref_stack=[' \
            '\'MinimalCircularConfig\', ' \
            '\'MinimalCircularConfig\'' \
            ']' == str(excinfo.value)

    def test_multi_level_circular_dependency_in__inheritance(self):
        with pytest.raises(octoconf.CircularDependencyError) as excinfo:
            self.octoconf_read(yaml_used_config='MultiCircularConfigTop')

        assert 'Circular dependency detected in YAML! ref_stack=[' \
            '\'MultiCircularConfigTop\', ' \
            '\'MultiCircularConfigMiddle\', ' \
            '\'MultiCircularConfigBottom\', ' \
            '\'MultiCircularConfigTop\'' \
            ']' == str(excinfo.value)

    def test_magic_attribute_not_exits_exception(self, yaml):
        with pytest.raises(AttributeError) as excinfo:
            yaml.not_exited_attribute

        assert '\'ConfigObject\' object has no attribute \'not_exited_attribute\'' == str(excinfo.value)

    def test_substitution(self, yaml):
        assert '$BASE' not in yaml.App.VALUE_WITH_VARIABLE
        assert '/test/my_res' == yaml.App.VALUE_WITH_VARIABLE

    def test_yaml_validity(self):
        yaml = self.octoconf_read(yaml_used_config='DevelopmentConfig')
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
        } == yaml.get_dict()

    def test_str_dump_validity(self):
        yaml = self.octoconf_read(yaml_used_config='DevelopmentConfig')
        expected_yaml = """{'App': {'UTF8_VALUE': %s,
         'VALUE_WITH_VARIABLE': '/test/my_res'},
 'DebugId': 'Development',
 'Flask': {'DEBUG': True,
           'SERVER_NAME': '0.0.0.0:8000',
           'STATIC_FOLDER': '/test',
           'TESTING': False},
 'SqlAlchemy': {'SQLALCHEMY_DATABASE_URI': 'sqlite:///test/app.sqlite'}}""" % repr(u'Több hűtőházból kértünk színhúst')
        assert expected_yaml == str(yaml)

    def test_can_set_existed_value_by_key(self, yaml):
        yaml.Flask['STATIC_FOLDER'] = '/new_path'
        assert yaml.Flask.STATIC_FOLDER == '/new_path'

    def test_can_not_set_existed_value_by_attr(self, yaml):
        yaml.Flask.STATIC_FOLDER = '/new_path'
        assert yaml.Flask.STATIC_FOLDER == '/test'

    def test_can_set_not_existed_value_by_key(self, yaml):
        yaml.Flask['NEW_PROPERTY'] = '/new_path'
        assert 'NEW_PROPERTY' in yaml.Flask
        assert yaml.Flask.NEW_PROPERTY == '/new_path'

    def test_can_not_set_not_existed_value_by_attr(self, yaml):
        yaml.Flask.NEW_PROPERTY = '/new_path'
        assert 'NEW_PROPERTY' not in yaml.Flask
