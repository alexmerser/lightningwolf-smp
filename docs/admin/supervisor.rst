Supervisor
==========

Installation
------------

::

    $ apt-get install supervisor

::

    $ service supervisor restart


All programs run under Supervisor must be run in a `non-daemonising <http://supervisord.org/subprocess.html#nondaemonizing-of-subprocesses>`_
mode (sometimes also called 'foreground mode'). If, by default, the program forks and returns on startup, then you may
need to consult the program's manual to find the option to enable this mode, otherwise Supervisor will not be able to
properly determine the status of the program.

Example
-------

