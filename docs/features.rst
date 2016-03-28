Features
========

.. contents::


Main
----

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

        config = octoconf.loads(yaml_string)
        print(config)

* Results:
    .. code-block:: python

        {
            'Small': {
                'RED': 1,
                'YELLOW': 2
            }
        }


Variables
---------

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

        config = octoconf.loads(yaml_string, variables={'VAR1': '/test1'})
        print(config)

* Results:
    .. code-block:: python

        {
            'Small': {
                'RED': 1,
                'YELLOW': 'XXX/test1XXX'
            }
        }


Inheritance
-----------

Read a multiple config contained YAML, where the selected config is inherited from another config.

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

    Order of overrides: ``Fruits`` >> ``SmallFruits`` >> ``ExtraSmallFruits``

* Reader code:
    .. code-block:: python

        import octoconf

        config = octoconf.loads(yaml_string)
        print(config)

* Results:
    .. code-block:: python

        {
            'Small': {
                'RED': 6,
                'YELLOW': 5
                'GREEN': 3,
            }
        }


Includes
--------

Read config from multiple YAML files. *The ``<INCLUDE`` directive allows one YAML string or multiple YAMLs as list*

* Example YAML files:
    * ``main.yml``
        .. code-block:: yaml

            USED_CONFIG>: Fruits
            <INCLUDE:
              - vendor/default.yml
              - extra.yml

            Fruits:
              Small:
                PURPLE: 4

    * ``vendor/default.yml``
        .. code-block:: yaml

            USED_CONFIG>: ExtraSmallFruits
            <INCLUDE: default.orig.yml

            Fruits:
              Small:
                YELLOW: 12
                GREEN: 13
                PURPLE: 14

    * ``vendor/default.orig.yml``
        .. code-block:: yaml

            Fruits:
              Small:
                RED: 21
                YELLOW: 22
                GREEN: 23
                PURPLE: 24

    * ``extra.yml``
        .. code-block:: yaml

            Fruits:
              Small:
                GREEN: 33
                PURPLE: 34

    Order of overrides: ``default.orig.yml`` >> ``default.yml`` >> ``extra.yml`` >> ``main.yml``

* Reader code:
    .. code-block:: python

        import octoconf

        config = octoconf.loads(main_yaml_string)
        print(config)

* Results:
    .. code-block:: python

        {
            'Small': {
                'RED': 21,
                'YELLOW': 12,
                'GREEN': 33,
                'PURPLE': 4,
            },
        }
