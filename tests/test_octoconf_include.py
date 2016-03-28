import pytest
import textwrap

import octoconf
from tests.common import substitute_yaml, patch_open_read


class TestPathOfIncludedFile(object):
    def assert_load(self, main_includes, included_files, include_cwd=None):
        """
        :type main_includes: list
        :type included_files: dict
        :type include_cwd: str or None
        """
        __tracebackhide__ = True

        indented_includes = '\n'.join(['  - {}'.format(include)
                                       for include in main_includes])

        yaml = substitute_yaml(textwrap.dedent("""
            {_default_}: Fruits
            {_include_}:
            {main_includes}

            Fruits:
              orange: 1
            """), main_includes=indented_includes)

        with patch_open_read(included_files):
            config = octoconf.loads(yaml, include_cwd=include_cwd)

        assert {'orange': 1} == config.get_dict()

    def test_include_absolute(self):
        self.assert_load(
            main_includes=['/root/alpha.yml'],
            included_files={
                '/root/alpha.yml': '',
            })

    def test_include_relative_from_cwd(self):
        self.assert_load(
            main_includes=['alpha.yml'],
            included_files={
                'alpha.yml': '',
            })

    def test_include_relative_from_subdir_in_cwd(self):
        self.assert_load(
            main_includes=['subdir/alpha.yml'],
            included_files={
                'subdir/alpha.yml': '',
            })

    def test_include_relative_from_custom_absolute_path(self):
        self.assert_load(
            main_includes=['alpha.yml'],
            include_cwd='/root',
            included_files={
                '/root/alpha.yml': '',
            })

    def test_include_relative_from_subdir_in_custom_absolute_path(self):
        self.assert_load(
            main_includes=['subdir/alpha.yml'],
            include_cwd='/root',
            included_files={
                '/root/subdir/alpha.yml': '',
            })

    def test_include_relative_from_custom_relative_path(self):
        self.assert_load(
            main_includes=['alpha.yml'],
            include_cwd='custom_subdir',
            included_files={
                'custom_subdir/alpha.yml': '',
            })

    def test_include_relative_from_subdir_in_custom_relative_path(self):
        self.assert_load(
            main_includes=['subdir/alpha.yml'],
            include_cwd='custom_subdir',
            included_files={
                'custom_subdir/subdir/alpha.yml': '',
            })

    def test_change_cwd_to_included_file_path(self):
        self.assert_load(
            main_includes=['fruits/alpha.yml'],
            included_files={
                'fruits/alpha.yml': substitute_yaml('{_include_}: beta.yml'),
                'fruits/beta.yml': substitute_yaml('{_include_}: small/gamma.yml'),
                'fruits/small/gamma.yml': '',
            })

    def test_change_cwd_to_included_file_path_with_custom_absolute_path(self):
        self.assert_load(
            main_includes=['fruits/alpha.yml'],
            include_cwd='/root',
            included_files={
                '/root/fruits/alpha.yml': substitute_yaml('{_include_}: beta.yml'),
                '/root/fruits/beta.yml': substitute_yaml('{_include_}: small/gamma.yml'),
                '/root/fruits/small/gamma.yml': '',
            })

    def test_change_cwd_to_included_file_path_with_custom_relative_path(self):
        self.assert_load(
            main_includes=['fruits/alpha.yml'],
            include_cwd='custom_subdir',
            included_files={
                'custom_subdir/fruits/alpha.yml': substitute_yaml('{_include_}: beta.yml'),
                'custom_subdir/fruits/beta.yml': substitute_yaml('{_include_}: small/gamma.yml'),
                'custom_subdir/fruits/small/gamma.yml': '',
            })

    def test_includes_from_multiple_yaml(self):
        self.assert_load(
            main_includes=['alpha.yml', 'beta.yml'],
            included_files={
                'alpha.yml': '',
                'beta.yml': '',
            })

    def test_multi_level_includes_from_multiple_yaml(self):
        self.assert_load(
            main_includes=['alpha.yml', 'beta.yml'],
            included_files={
                'alpha.yml': substitute_yaml("""
                    {_include_}:
                      - gamma.yml
                      - delta.yml
                    """),
                'beta.yml': '',
                'gamma.yml': '',
                'delta.yml': '',
            })

    def test_multi_level_includes_same_file(self):
        self.assert_load(
            main_includes=['alpha.yml', 'beta.yml', 'gamma.yml'],
            included_files={
                'alpha.yml': substitute_yaml('{_include_}: beta.yml'),
                'beta.yml': '',
                'gamma.yml': substitute_yaml('{_include_}: beta.yml'),
            })

    def test_single_level_inplace_circular_include_detection(self):
        with pytest.raises(octoconf.CircularIncludeError) as excinfo:
            self.assert_load(
                main_includes=['alpha.yml'],
                include_cwd='/root',
                included_files={
                    '/root/alpha.yml': substitute_yaml('{_include_}: alpha.yml'),
                })

        assert 'circular include detected; ref_chain=[' \
               '\'/root/alpha.yml\', ' \
               '\'/root/alpha.yml\'' \
               ']' == str(excinfo.value)

    def test_multi_level_inplace_circular_include_detection(self):
        with pytest.raises(octoconf.CircularIncludeError) as excinfo:
            self.assert_load(
                main_includes=['alpha.yml'],
                include_cwd='/root',
                included_files={
                    '/root/alpha.yml': substitute_yaml('{_include_}: beta.yml'),
                    '/root/beta.yml': substitute_yaml('{_include_}: beta.yml'),
                })

        assert 'circular include detected; ref_chain=[' \
               '\'/root/alpha.yml\', ' \
               '\'/root/beta.yml\', ' \
               '\'/root/beta.yml\'' \
               ']' == str(excinfo.value)

    def test_multi_level_circular_include_detection(self):
        with pytest.raises(octoconf.CircularIncludeError) as excinfo:
            self.assert_load(
                main_includes=['alpha.yml'],
                include_cwd='/root',
                included_files={
                    '/root/alpha.yml': substitute_yaml('{_include_}: beta.yml'),
                    '/root/beta.yml': substitute_yaml('{_include_}: gamma.yml'),
                    '/root/gamma.yml': substitute_yaml('{_include_}: alpha.yml'),
                })

        assert 'circular include detected; ref_chain=[' \
               '\'/root/alpha.yml\', ' \
               '\'/root/beta.yml\', ' \
               '\'/root/gamma.yml\', ' \
               '\'/root/alpha.yml\'' \
               ']' == str(excinfo.value)


class TestContentOfIncludedFile(object):
    def test_select_config_from_included_file(self):
        yaml = substitute_yaml("""
            {_default_}: Vegetables
            {_include_}: alpha.yml

            Fruits:
                orange: 1
            """)

        included_files = {
            'alpha.yml': substitute_yaml("""
                Vegetables:
                    carrot: 2
                """),
        }

        with patch_open_read(included_files):
            config = octoconf.loads(yaml)

        assert {
            'carrot': 2,
        } == config.get_dict()

    def test_select_config_in_included_file(self):
        yaml = substitute_yaml("""
            {_include_}: alpha.yml

            Fruits:
                orange: 1
            """)

        included_files = {
            'alpha.yml': substitute_yaml("""
                {_default_}: Fruits
                Vegetables:
                    carrot: 2
                """),
        }

        with patch_open_read(included_files):
            config = octoconf.loads(yaml)

        assert {
            'orange': 1,
        } == config.get_dict()

    def test_select_config_from_multi_level_included_file(self):
        yaml = substitute_yaml("""
            {_default_}: Vegetables
            {_include_}: alpha.yml

            Fruits:
                orange: 1
            """)

        included_files = {
            'alpha.yml': substitute_yaml('{_include_}: beta.yml'),
            'beta.yml': substitute_yaml('{_include_}: gamma.yml'),
            'gamma.yml': substitute_yaml("""
                Vegetables:
                    carrot: 2
                """),
        }

        with patch_open_read(included_files):
            config = octoconf.loads(yaml)

        assert {
            'carrot': 2,
        } == config.get_dict()

    def test_config_overrides_the_included_config(self):
        yaml = substitute_yaml("""
            {_default_}: Fruits
            {_include_}: alpha.yml

            Fruits:
                orange: 1
                apple: 2
            """)

        included_files = {
            'alpha.yml': substitute_yaml("""
                Fruits:
                    apple: 13
                    kiwi: 14
                """),
        }

        with patch_open_read(included_files):
            config = octoconf.loads(yaml)

        assert {
            'orange': 1,
            'apple': 2,
            'kiwi': 14,
        } == config.get_dict()

    def test_config_overrides_the_included_config_on_multiple_level(self):
        yaml = substitute_yaml("""
            {_default_}: Fruits
            {_include_}: alpha.yml

            Fruits:
                apple: 1
                banana: 2
            """)

        included_files = {
            'alpha.yml': substitute_yaml("""
                {_include_}: beta.yml

                Fruits:
                    banana: 13
                    kiwi: 14
                """),
            'beta.yml': substitute_yaml("""
                Fruits:
                    kiwi: 25
                    orange: 26
                """),
        }

        with patch_open_read(included_files):
            config = octoconf.loads(yaml)

        assert {
            'apple': 1,
            'banana': 2,
            'kiwi': 14,
            'orange': 26,
        } == config.get_dict()

    def test_include_overrides_the_previous_included_configs(self):
        yaml = substitute_yaml("""
            {_default_}: Fruits
            {_include_}:
              - alpha.yml
              - beta.yml
            """)

        included_files = {
            'alpha.yml': substitute_yaml("""
                Fruits:
                    apple: 1
                    banana: 2
                """),
            'beta.yml': substitute_yaml("""
                Fruits:
                    banana: 13
                    kiwi: 14
                """),
        }

        with patch_open_read(included_files):
            config = octoconf.loads(yaml)

        assert {
            'apple': 1,
            'banana': 13,
            'kiwi': 14,
        } == config.get_dict()
