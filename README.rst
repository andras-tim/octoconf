|Logo|

octoconf
========

|PyPi| |Build| |DependencyStatus2| |CodeQuality| |Coverage| |License|

Multi-profile supported, flexible config library for Python 2 & 3.


Features
--------

* Allow multiple config profiles in one YAML file
* Allow include multiple YAML files
* Overridable profile selection from code for special use-cases (e.g. config for testing)
* Inheritable config profiles, what makes profile merges by dictionaries. (the native YAML bookmarking is also available)
* Can use variables in the config file


Installation
------------

``pip install octoconf``


Config format
-------------

An **octoconf** config file is pure YAML file with some reserved keywords:

* ``USED_CONFIG>: <node_name>`` in the file root
    you can specify the name of default config profile

* ``<INCLUDE: <yml_path(s)>`` in the file root
    this octoconf file(s) will be included

* ``<BASE: <node_name>`` in the 2nd level
    this will used for making (merge based) inheritance between profiles

*The profile nodes should be on 1st level!*


Usage
-----

* You can load config from string with ``loads()``:
    .. code-block:: python

        import octoconf

        config = octoconf.loads(yaml_string)
        print(config)

* Or directly from StringIO (e.g. from file) with ``load()``:
    .. code-block:: python

        import octoconf

        with open('config.yml') as fd:
            config = octoconf.load(fd)
        print(config)


Please check the `features docs <docs/features.rst>`__ for explain **octoconf**'s features.


Examples YAML files
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    USED_CONFIG>: UserConfig
    <INCLUDE: vendor.defaults.yml


    # This config overrides the production preset (from vendor.defaults.yml file)
    UserConfig:
      <BASE: ProductionConfig

      App:
        TITLE: "Amazing Foobar"

      Flask:
        SQLALCHEMY_DATABASE_URI: "sqlite:///${SERVER}/app.sqlite"


For more examples, please check the `examples <https://github.com/andras-tim/octoconf/tree/master/examples>`__ directory.


Bugs
----

Bugs or suggestions? Visit the `issue tracker <https://github.com/andras-tim/octoconf/issues>`__.


.. |Logo| image:: https://raw.githubusercontent.com/andras-tim/octoconf/master/img/logo_100.png
    :target: https://raw.githubusercontent.com/andras-tim/octoconf/master/img/logo.png

.. |Build| image:: https://travis-ci.org/andras-tim/octoconf.svg?branch=master
    :target: https://travis-ci.org/andras-tim/octoconf/branches
    :alt: Build Status
.. |DependencyStatus1| image:: https://gemnasium.com/andras-tim/octoconf.svg
    :target: https://gemnasium.com/andras-tim/octoconf
    :alt: Dependency Status
.. |DependencyStatus2| image:: https://requires.io/github/andras-tim/octoconf/requirements.svg?branch=master
    :target: https://requires.io/github/andras-tim/octoconf/requirements/?branch=master
    :alt: Server Dependency Status
.. |PyPi| image:: https://img.shields.io/pypi/dm/octoconf.svg
    :target: https://pypi.python.org/pypi/octoconf
    :alt: Python Package
.. |License| image:: https://img.shields.io/badge/license-GPL%203.0-blue.svg
    :target: https://github.com/andras-tim/octoconf/blob/master/LICENSE
    :alt: License

.. |CodeQuality| image:: https://api.codacy.com/project/badge/grade/2f707d3bf0f84a43a1dca6b8789eaba2
    :target: https://www.codacy.com/app/andras-tim/octoconf
    :alt: Code Quality
.. |CodeClimate| image:: https://codeclimate.com/github/andras-tim/octoconf/badges/gpa.svg
    :target: https://codeclimate.com/github/andras-tim/octoconf/coverage
    :alt: Code Climate
.. |Coverage| image:: https://coveralls.io/repos/andras-tim/octoconf/badge.svg?branch=master&service=github
    :target: https://coveralls.io/r/andras-tim/octoconf?branch=master&service=github
    :alt: Server Test Coverage
.. |IssueStats| image:: https://img.shields.io/github/issues/andras-tim/octoconf.svg
    :target: http://issuestats.com/github/andras-tim/octoconf
    :alt: Issue Stats
