# KeePass command line application

[KPCLibPy][1] is a KeePass command application written in Python.

The original [KeePass][3] by Dominik Reichl is a .NET application written in C#. `KeePassLib` is part of KeePass which can be built as a library to support the major functions of KeePass. However, at the moment, `KeePassLib` is still built for .NET framework which can run on Windows only. I modified `KeePassLib` and extended it as a .NET Standard library - [KPCLib][2]. [KPCLib][2] stands for KeePass Portable Class Library at the time when I started the work. Portable Class Library (PCL) is replaced by .NET Standard Library nowaday.

[KPCLibPy][1] is just a Python wrapper of [KPCLib][2] using [Python.NET][4]. In this perspective, `KPCLibPy` is fully compatiable to the original KeePass, since the majority of code is  the same as KeePass.

In order to save the development effort and have a nice user interface, the Python library [python-nubia][5] from Facebook is used as the framework to support command line interface.

## Key Features
- Full compatible with the original KeePass
- .NET Standard 2.0 support with [KPCLib][2]
- Cross platform support with .NET Standard and .NET core
- Nice user interface with [python-nubia][5]
- Interactive mode that offers fish-style auto-completion

## Installation
As a developer, you can use [KPCLibPy][1] from GitHub directly.
```bash
git clone https://github.com/shugaoye/KPCLibPy.git
cd KPCLibPy
pip install -r requirements.txt
cd src
python3 ./nubia_main.py
```

![image01](https://github.com/passxyz/passxyz.github.io/raw/master/images/kpclib/kpclibpy.gif)

## Docker image
A Dockr image - [docker-mono][6] can be used on Linux or Windows 10 (WSL).


[1]: https://github.com/passxyz/KPCLibPy
[2]: https://github.com/passxyz/KPCLib
[3]: https://keepass.info/
[4]: http://pythonnet.github.io/
[5]: https://github.com/facebookincubator/python-nubia
[6]: https://github.com/shugaoye/docker-mono