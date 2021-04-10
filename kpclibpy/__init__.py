#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
__all__ = (
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
)

__copyright__ = "Copyright 2021 Roger Ye"

import importlib_metadata

try:
    metadata = importlib_metadata.metadata("kpclibpy")


    __title__ = metadata["name"]
    __summary__ = metadata["summary"]
    __uri__ = metadata["home-page"]
    __version__ = metadata["version"]
    __author__ = metadata["author"]
    __email__ = metadata["author-email"]
    __license__ = metadata["license"]
except ModuleNotFoundError:
    __version__ = "1.1.5.dev0"
    print("Debug build ", __version__)