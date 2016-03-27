# Pytest config for this test directory
import pytest
from pytest_pep8 import Pep8Item


def pytest_itemcollected(item):
    """
    :type item: _pytest.main.Node
    """
    if item.get_marker('skip'):
        __skip_item(item)


def pytest_collection_modifyitems(items):
    """
    :type items: list[_pytest.main.Node]
    """
    if __has_only_marked_item(items):
        __skip_not_only_marked_items(items)


def __has_only_marked_item(items):
    """
    :type items: list[_pytest.main.Node]
    :rtype: bool
    """
    for item in items:
        if item.get_marker('only'):
            return True
    return False


def __skip_not_only_marked_items(items):
    """
    :type items: list[_pytest.main.Node]
    """
    for item in items:
        if not isinstance(item, Pep8Item) and not item.get_marker('only'):
            __skip_item(item, reason='Skipped by only mark(s)')


def __skip_item(item, reason=None):
    """
    :type item: _pytest.main.Node
    :type reason: str or None
    """
    item.add_marker(pytest.mark.skipif(True, reason=reason))
