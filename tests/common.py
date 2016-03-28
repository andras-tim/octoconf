import mock
import os

try:
    from builtins import open
    OPEN_CLASS = 'builtins.open'
except ImportError:
    from __builtin__ import open
    OPEN_CLASS = '__builtin__.open'

from octoconf.octoconf import DEFAULT_CONFIG_SELECTOR, BASE_CONFIG_SELECTOR, INCLUDE_FILE_SPECIFIER


def substitute_yaml(yaml_string, **custom_substitutions):
    """
    Substitute `_default_`, `_base_` and `_include_` with actual value.
    """
    return yaml_string.format(
        _default_=DEFAULT_CONFIG_SELECTOR,
        _base_=BASE_CONFIG_SELECTOR,
        _include_=INCLUDE_FILE_SPECIFIER,
        **custom_substitutions
    )


def patch_open_read(files):
    """
    Patch open() command and mock read() results

    :type files: dict
    """
    files = {os.path.abspath(path): content for path, content in files.items()}

    def mock_open_wrapper(path, *args, **kwargs):
        __tracebackhide__ = True

        assert path in files, 'try to open a non-mocked path\n    desired={desired!r}\n    mocked={mocked!r}'.format(
            desired=path, mocked=files.keys())

        open_mock = mock.mock_open(read_data=files[path])
        return open_mock(path, *args, **kwargs)

    return mock.patch(OPEN_CLASS, mock_open_wrapper)
