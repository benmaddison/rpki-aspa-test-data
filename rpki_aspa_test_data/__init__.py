# Copyright (c) 2022 Ben Maddison. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""rpki_aspa_test_data package."""

from __future__ import annotations

import importlib.abc
import importlib.resources
import logging

log = logging.getLogger(__name__)


def resources() -> importlib.abc.Traversable:
    """Get a path-like object for consuming package data."""
    return importlib.resources.files("rpki_aspa_test_data")
