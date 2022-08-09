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
"""rpki_aspa_test_data.data module."""

from __future__ import annotations

import json
import logging
import pathlib
from typing import Iterable, Iterator, Literal, Optional, Tuple, TypedDict

import jsonschema

import yaml

from . import resources

log = logging.getLogger(__name__)

AfiName = Literal["ipv4", "ipv6"]
Afi = Literal[4, 6]


class ProviderSpec(TypedDict):
    """Type definition for 'ProviderAS' object specification."""

    provider_asid: int
    afi_limit: Optional[AfiName]


class Provider:
    """Input data for 'ProviderAS' objects."""

    def __init__(self, provider_asid: int,
                 afi_limit: Optional[AfiName] = None):
        """Initialise 'Provider' object from spec."""
        self._provider_asid = provider_asid
        self._afi_limit = afi_limit

    @property
    def provider_asid(self) -> int:
        """Get 'providerASID' field value."""
        return self._provider_asid

    @property
    def afi_limit(self) -> Optional[Afi]:
        """Get 'afiLimit' field value."""
        if (a := self._afi_limit) is None:
            return None
        else:
            afi_map: dict[AfiName, Afi] = {"ipv4": 4, "ipv6": 6}
            return afi_map[a]


class Case:
    """Test case definition data."""

    def __init__(self,
                 name: str,
                 valid: bool,
                 customer_asid: int,
                 providers: Iterable[ProviderSpec],
                 desc: Optional[str] = None) -> None:
        """Initialise 'Case' object from spec."""
        self._name = name
        self._valid = valid
        self._desc = desc
        self._customer_asid = customer_asid
        self._providers = [Provider(**p) for p in providers]

    @property
    def name(self) -> str:
        """Get 'Case' name."""
        return self._name

    @property
    def valid(self) -> bool:
        """Get 'Case' validity."""
        return self._valid

    @property
    def customer_asid(self) -> int:
        """Get 'customerASID' field value."""
        return self._customer_asid

    @property
    def providers(self) -> list[Tuple[int, Optional[Afi]]]:
        """Get 'providers' field value."""
        return [(p.provider_asid, p.afi_limit)
                for p in self._providers]

    @property
    def ca_name(self) -> str:
        """Construct CA commonName for test case."""
        return f"ca-case-{self.name}-{self.valid}".lower()


class Cases:
    """Set of test case definitions."""

    def __init__(self, cases: Iterable[Case]) -> None:
        """Initialise 'Cases' object from spec."""
        self._cases = cases

    @classmethod
    def load(cls, path: pathlib.Path, *extra_paths: pathlib.Path) -> Cases:
        """Load and validate 'Cases' object from yaml spec file."""
        with resources().joinpath("cases-schema.json").open() as f:
            schema = json.load(f)
        jsonschema.Draft7Validator.check_schema(schema)
        validator = jsonschema.Draft7Validator(schema)
        cases = []
        for p in [path] + list(extra_paths):
            with open(p) as f:
                data = yaml.safe_load(f)
            errors = list(validator.iter_errors(data))
            if errors:
                for e in errors:
                    log.error(e)
                raise RuntimeError(f"Failed to validate test cases spec '{p}'")
            cases += [Case(**d) for d in data]
        return cls(cases)

    def __iter__(self) -> Iterator[Case]:
        """Get an iterator over test cases."""
        return (case for case in self._cases)
