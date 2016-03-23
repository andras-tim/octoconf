|Logo|

octoconf
========

|PyPi| |Build| |DependencyStatus2| |CodeQuality| |Coverage| |License|

Multi-profile supported, flexible config library for Python 2 & 3.


Features
--------

* Allow multiple config profiles in one YAML file
* Overridable profile selection from code for special use-cases (e.g. config for testing)
* Inheritable config profiles, what makes profile merges by dictionaries. (the native YAML bookmarking is also available)
* Can use variables in the config file


Installation
------------

``pip install octoconf``


Config format
-------------

An **octoconf** YAML file have two restricted keywords:

* ``USED_CONFIG>: <node_name>`` in the file root
    you can specify the name of default config profile

* ``<BASE: <node_name>`` in the 2nd level
    this will used for making (merge based) inheritance between profiles

*The profile nodes should be on 1st level!*


Usage
-----
There is an example YAML for demonstration

.. code-block:: yaml

    USED_CONFIG>: Fruits

    Fruits:
      RED: 1
      YELLOW: $VAR1/2

    SmallFruits:
      <BASE: Fruits
      RED: 3

    ExtraSmallFruits:
      <BASE: SmallFruits
      RED: 4



Basic case
~~~~~~~~~~

Read a multiple config contained YAML, and get profile which was selected by default.

* Example YAML:
    .. code-block:: yaml

        USED_CONFIG>: Fruits

        Fruits:
          Small:
            RED: 1
            YELLOW: 2

        Vegetables:
          Big:
            RED: 3
            YELLOW: 4

* Reader code:
    .. code-block:: python

        import octoconf

        yaml = octoconf.read('/test/foo.yaml')
        print(yaml)

* Results:
    .. code-block:: python

        {
            'Small': {
                'RED': 1,
                'YELLOW': 2
            }
        }


Variables
~~~~~~~~~

Read a YAML file which contains variables.

* Example YAML:
    .. code-block:: yaml

        USED_CONFIG>: Fruits

        Fruits:
          Small:
            RED: 1
            YELLOW: XXX${VAR1}XXX

        Vegetables:
          GREEN: 2

* Reader code:
    .. code-block:: python

        import octoconf

        yaml = octoconf.read('/test/foo.yaml', variables={'VAR1': '/test1'})
        print(yaml)

* Results:
    .. code-block:: python

        {
            'Small': {
                'RED': 1,
                'YELLOW': 'XXX/test1XXX'
            }
        }


Inheritance
~~~~~~~~~~~

Read a multiple config contained YAML, where the selected config is inherited from another config.

``ExtraSmallFruits`` >> ``SmallFruits`` >> ``Fruits``

* Example YAML:
    .. code-block:: yaml

        USED_CONFIG>: ExtraSmallFruits

        Fruits:
          Small:
            RED: 1
            YELLOW: 2
            GREEN: 3

        SmallFruits:
          <BASE: Fruits
          Small:
            RED: 4
            YELLOW: 5

        ExtraSmallFruits:
          <BASE: SmallFruits
          Small:
            RED: 6

* Reader code:
    .. code-block:: python

        import octoconf

        yaml = octoconf.read('/test/foo.yaml')
        print(yaml)

* Results:
    .. code-block:: python

        {
            'Small': {
                'RED': 6,
                'YELLOW': 5
                'GREEN': 3,
            }
        }


More example
~~~~~~~~~~~~

Please check the `examples <https://github.com/andras-tim/octoconf/tree/master/examples>`__ directory.


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
