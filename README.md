# KeePass

## Access KeePass database using [Python.NET][1]
There is a Python library [pykeepass][2] which is a Python implementation for KeePass database. This is a pure Python implementation referring to [KeePassXC][4] project.

The orginal KeePass library is implemented in C# for .NET Framework. I modified it slightly to target .NET standard 2.0 as [KPCLib][5] project. It is possible to use [KPCLib][5] and [Python.NET][1] to access KeePass database.

We can refer to this article [How to call a dynamic library][3] to use [KPCLib][5] in Python.

To install the required packages, you can run the following command on Windows.

`C:\> pip install -r requirements.txt`

or, the following command on Linux.

`$ pip3 install -r requirements.txt`

On Windows 10, we have .NET runtime already. On Linux, we need to install .NET runtime and Mono. Below is my test environment on Linux. You can also use my docker image [docker-mono][8].

## Test environment
- Ubuntu 18.04
- [.NET 5.0][7]
- [Python.NET][6] - 2.5.2
- [KPCLib][5] - 1.1.9

```
$ dotnet --info
.NET SDK (reflecting any global.json):
 Version:   5.0.103
 Commit:    9effbc8ad5

Runtime Environment:
 OS Name:     ubuntu
 OS Version:  18.04
 OS Platform: Linux
 RID:         ubuntu.18.04-x64
 Base Path:   /usr/share/dotnet/sdk/5.0.103/

Host (useful for support):
  Version: 5.0.3
  Commit:  eae88cc11b

.NET SDKs installed:
  5.0.103 [/usr/share/dotnet/sdk]

.NET runtimes installed:
  Microsoft.AspNetCore.App 5.0.3 [/usr/share/dotnet/shared/Microsoft.AspNetCore.App]
  Microsoft.NETCore.App 5.0.3 [/usr/share/dotnet/shared/Microsoft.NETCore.App]

To install additional .NET runtimes or SDKs:
  https://aka.ms/dotnet-download
```

```
$ mono -V
Mono JIT compiler version 6.12.0.107 (tarball Thu Dec 10 05:22:56 UTC 2020)
Copyright (C) 2002-2014 Novell, Inc, Xamarin Inc and Contributors. www.mono-project.com
        TLS:           __thread
        SIGSEGV:       altstack
        Notifications: epoll
        Architecture:  amd64
        Disabled:      none
        Misc:          softdebug 
        Interpreter:   yes
        LLVM:          yes(610)
        Suspend:       hybrid
        GC:            sgen (concurrent by default)

```

## Build KPCLib

```
$ git clone https://github.com/passxyz/KPCLib.git
$ dotnet build
$ dotnet publish
```


[1]: http://pythonnet.github.io/
[2]: https://github.com/libkeepass/pykeepass
[3]: https://github.com/pythonnet/pythonnet/wiki/How-to-call-a-dynamic-library
[4]: https://github.com/keepassxreboot/keepassxc
[5]: https://github.com/passxyz/KPCLib
[6]: https://github.com/pythonnet/pythonnet
[7]: https://dotnet.microsoft.com/download/dotnet/5.0
[8]: https://hub.docker.com/r/shugaoye/docker-mono
