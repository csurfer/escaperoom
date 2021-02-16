escaperoom
==========

|pypiv| |pyv| |Licence| |Thanks|

Escape rooms are a game form where the objective is to complete the mission and "escape"
from a locked room. A successful escape involves finding hidden clues and solving puzzles
spread through out the room in a pre-determined amount of time.

Virtual escape rooms, take this experience and put it online for groups of people not
geographically co-located to still enjoy it as a group. These have become popular
especially now given the pandemic and stay at home orders.

This package provides a simple command to take a escape room configuration and host it
as a virtual experience for you and your family/friends to enjoy.

Features
--------

* Simple CLI interface.

* No complicated setup.

* No coding knowledge required.

* Design your own escape room experience for your friends and family to enjoy!

Setup
-----

Using pip
~~~~~~~~~

.. code:: bash

    pip install escaperoom

Directly from the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/csurfer/escaperoom.git
    python escaperoom/setup.py install

Usage
-----

Pre-requisites:

1. Have your escaperoom configuration ready. Something along the lines of `examplecampaigns`_.

Help text
~~~~~~~~~

.. code:: bash

    escaperoom --help

Validation
~~~~~~~~~~

JSON file provided is validated against the `jsonschema`_ file for type and key correctness.

.. code:: bash

    escaperoom validation <path_to_json_file>

Running/Hosting the escape room
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    # To run with default host and port.
    escaperoom run <path_to_json_file>
    # To run with specific host and port.
    escaperoom run <path_to_json_file> --host <customhost> --port <customport>

Configuration
-------------

This is the only detail you need to worry about. A JSON file in a specific format contains
details of the escape room you want to host and this section throws light on the different
components of the configuration file.

Each configuration file has two main components.

story
  (required) A narrative to start your experience with. A tale of mystery and thrill.

puzzles
  (required) List of puzzles designed by you which is what your friends would solve during the event.

story
~~~~~

Story itself has following components.

title
  (required) An interesting title to your story.

text
  (required) Narrative of the story or text of the story.

images
  (optional) Set of images you might want to show to have a dramatic effect. NOTE: Each image should either
  be a URL or absolute path to an image stored on your device.

puzzles
~~~~~~~

Each puzzle in the list of puzzles has the following components.

title
  (required) An interesting title to your story.

text
  (required) Narrative of the story or text of the story.

images
  (optional) Set of images you might want to show to have a dramatic effect. NOTE: Each image should either
  be a URL or absolute path to an image stored on your device.

hints
  (optional) Set of hints you might want to give to your friends to help them understand/solve the
  puzzles you have set.

answer
  (requied) Answer to your puzzle. Keep it as a word or a number to avoid confusions.

JSONSchema Validation
~~~~~~~~~~~~~~~~~~~~~

You can find some example campaigns in `examplecampaigns`_. We use https://python-jsonschema.readthedocs.io/en/stable/
to validate the correctness of the config file. The schema we validate it against can be found at `jsonschema`_.


Contributing
------------

Bug Reports and Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please use `issue tracker`_ for reporting bugs or feature requests.

Development
~~~~~~~~~~~

Pull requests are most welcome. New and fun campaigns are always eagerly awaited.


Buy the developer a cup of coffee!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you found this package fun/useful you can buy me a cup of coffee using

|Donate|

.. |Donate| image:: https://www.paypalobjects.com/webstatic/en_US/i/btn/png/silver-pill-paypal-44px.png
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=3BSBW7D45C4YN&lc=US&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted

.. |Thanks| image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/csurfer

.. _issue tracker: https://github.com/csurfer/escaperoom/issues

.. |Licence| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/csurfer/escaperoom/master/LICENSE

.. |pypiv| image:: https://img.shields.io/pypi/v/escaperoom.svg
   :target: https://pypi.python.org/pypi/escaperoom

.. |pyv| image:: https://img.shields.io/pypi/pyversions/escaperoom.svg
   :target: https://pypi.python.org/pypi/escaperoom

.. _examplecampaigns: https://github.com/csurfer/escaperoom/tree/main/escaperoom/example_campaigns

.. _jsonschema: https://github.com/csurfer/escaperoom/blob/main/escaperoom/config.schema
