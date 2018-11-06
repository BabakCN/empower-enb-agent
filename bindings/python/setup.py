#!/usr/bin/env python3
#
# Copyright (c) 2018 FBK-CreateNet
# AUTHOR: Abin Ninan Thomas
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""Setup script."""

from distutils.core import setup

setup(name="empower-enb-agent",
      version="1.0",
      description="EmPOWER Agent",
      author="Abin Ninan Thomas",
      author_email="",
      url="https://github.com/5g-empower/empower-enb-agent",
      long_description="EmPOWER Agent wrapper for LTE base stations",
      packages=['emage'])
