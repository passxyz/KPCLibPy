KeePass command line application
================================

`KPCLibPy <https://github.com/passxyz/KPCLibPy>`__ is a KeePass command
application written in Python.

The original `KeePass <https://keepass.info/>`__ by Dominik Reichl is a
.NET application written in C#. ``KeePassLib`` is part of KeePass which
can be built as a library to support the major functions of KeePass.
However, at the moment, ``KeePassLib`` is still built for .NET framework
which can run on Windows only. I modified ``KeePassLib`` and extended it
as a .NET Standard library -
`KPCLib <https://github.com/passxyz/KPCLib>`__.
`KPCLib <https://github.com/passxyz/KPCLib>`__ stands for KeePass
Portable Class Library at the time when I started the work. Portable
Class Library (PCL) is replaced by .NET Standard Library nowadays.

`KPCLibPy <https://github.com/passxyz/KPCLibPy>`__ is just a Python
wrapper of `KPCLib <https://github.com/passxyz/KPCLib>`__ using
`Python.NET <http://pythonnet.github.io/>`__. In this perspective,
``KPCLibPy`` is fully compatible to the original KeePass, since the
majority of code is the same as KeePass.

In order to save the development effort and have a nice user interface,
the Python library
`python-nubia <https://github.com/facebookincubator/python-nubia>`__
from Facebook is used as the framework to support command line
interface.

Key Features
------------

-  Full compatible with the original KeePass
-  .NET Standard 2.0 support with
   `KPCLib <https://github.com/passxyz/KPCLib>`__
-  Cross platform support with .NET Standard and .NET core
-  Nice user interface with
   `python-nubia <https://github.com/facebookincubator/python-nubia>`__
-  Interactive mode that offers fish-style auto-completion

Installation
------------

As a developer, you can use
`KPCLibPy <https://github.com/passxyz/KPCLibPy>`__ from GitHub directly.

.. code:: bash

    git clone https://github.com/shugaoye/KPCLibPy.git
    cd KPCLibPy
    pip install -r requirements.txt
    cd src
    python3 ./nubia_main.py

For normal user, `KPCLibPy <https://github.com/passxyz/KPCLibPy>`__ can
be installed using pip.

::

    $ pip install kpclibpy
    $ keepass

|image01|

Docker image
------------

A Dockr image -
`docker-mono <https://github.com/shugaoye/docker-mono>`__ can be used on
Linux or Windows 10 (WSL).

Issues
------
On Windows platform, you may get the below error message:
::

    Unhandled exception in event loop:
    File "c:\users\kpclibpy\appdata\local\programs\python\python38-32\lib\asyncio\proactor_events.py", line 768, in _loop_self_reading
        f.result()  # may raise
    File "c:\users\kpclibpy\appdata\local\programs\python\python38-32\lib\asyncio\windows_events.py", line 808, in _poll
        value = callback(transferred, key, ov)
    File "c:\users\kpclibpy\appdata\local\programs\python\python38-32\lib\asyncio\windows_events.py", line 457, in finish_recv
        raise ConnectionResetError(*exc.args)

    Exception [WinError 995] The I/O operation has been aborted because of either a thread exit or an application request
    Press ENTER to continue...

This is an issue of prompt-toolkit. You can change prompt-toolkit to version 2.x.

.. code:: bash

    pip install -U prompt-toolkit~=2.0

.. |image01| image:: https://github.com/passxyz/passxyz.github.io/raw/master/images/kpclib/kpclibpy.gif
