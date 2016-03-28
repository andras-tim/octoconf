# pylint: disable=misplaced-comparison-constant,redefined-outer-name,no-self-use
import mock
import os

from octoconf.octoconf import DEFAULT_CONFIG_SELECTOR, BASE_CONFIG_SELECTOR, INCLUDE_FILE_SPECIFIER

__OPEN_REF = None


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
        __tracebackhide__ = True  # pylint: disable=unused-variable

        assert path in files, 'try to open a non-mocked path\n    desired={desired!r}\n    mocked={mocked!r}'.format(
            desired=path, mocked=files.keys())

        open_mock = mock.mock_open(read_data=files[path])
        return open_mock(path, *args, **kwargs)

    return mock.patch(__get_open_ref(), mock_open_wrapper)


def __get_open_ref():
    """
    :rtype str
    """
    # pylint: disable=import-error,redefined-builtin,unused-import,unused-variable
    global __OPEN_REF

    if __OPEN_REF:
        return __OPEN_REF

    try:
        from builtins import open
        __OPEN_REF = 'builtins.open'
    except ImportError:
        from __builtin__ import open
        __OPEN_REF = '__builtin__.open'

    return __OPEN_REF
