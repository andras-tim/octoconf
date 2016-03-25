from octoconf.octoconf import DEFAULT_CONFIG_SELECTOR, BASE_CONFIG_SELECTOR


def substitute_yaml(yaml_string, **custom_substitutions):
    """
    Substitute `_default_` and `_base_` with actual value.
    """
    return yaml_string.format(
        _default_=DEFAULT_CONFIG_SELECTOR,
        _base_=BASE_CONFIG_SELECTOR,
        **custom_substitutions
    )
